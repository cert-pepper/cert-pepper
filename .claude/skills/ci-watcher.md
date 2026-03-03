# CI Watcher

Poll GitHub check-runs for a specific commit until all checks have a conclusion (up to 20 minutes).

**Required**: The caller must substitute the actual commit SHA in place of `<SHA>` before running.

```bash
SHA=<SHA>
MAX=40; i=0
while [ $i -lt $MAX ]; do
  result=$(GH_TOKEN="$GITHUB_PERSONAL_ACCESS_TOKEN" gh api \
    repos/crook3dfingers/cert-pepper/commits/$SHA/check-runs \
    --jq '.check_runs[] | {name,status,conclusion}' 2>/dev/null)
  if [ -n "$result" ]; then
    pending=$(echo "$result" | jq -r 'select(.conclusion == null) | .name' 2>/dev/null)
    if [ -z "$pending" ]; then
      failed=$(echo "$result" | jq -r 'select(.conclusion == "failure") | .name' 2>/dev/null)
      if [ -n "$failed" ]; then
        echo "CI FAILED — failed checks:"; echo "$failed"
        echo "Full results:"; echo "$result"
        exit 1
      fi
      echo "All checks passed:"; echo "$result"; exit 0
    fi
  fi
  i=$((i+1)); sleep 30
done
echo "CI watcher timed out after 20 minutes"; exit 1
```

- Polls every 30 seconds, up to 40 times (20-minute hard limit).
- Empty-response guard: skips iterations where the API returns nothing (CI not yet registered).
- Exits non-zero on failure or timeout so the task notification signals failure correctly.
- Output "CI FAILED" with the failed check names, or "All checks passed" with the full results.

Note: use `$GITHUB_PERSONAL_ACCESS_TOKEN`, NOT `$GITHUB_TOKEN` — the latter is MCP-only.
