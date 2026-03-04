# CI Watcher

Poll GitHub check-runs for a specific commit until all checks have a conclusion (up to 20 minutes).

**Required**: The caller must obtain the full 40-character SHA via `git rev-parse HEAD` and substitute it in place of `<SHA>`. Never guess or abbreviate — a wrong SHA causes a silent 422 loop.

```bash
SHA=<SHA>  # must be the full SHA from: git rev-parse HEAD
MAX=40; i=0
while [ $i -lt $MAX ]; do
  api_err=$(mktemp)
  result=$(GH_TOKEN="$GITHUB_PERSONAL_ACCESS_TOKEN" gh api \
    repos/crook3dfingers/cert-pepper/commits/$SHA/check-runs \
    --jq '.check_runs[] | {name,status,conclusion}' 2>"$api_err")
  if [ -s "$api_err" ]; then
    echo "API error (fatal):"; cat "$api_err"; rm -f "$api_err"; exit 1
  fi
  rm -f "$api_err"
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
- API errors (e.g. 422 from a wrong SHA) are printed and cause an immediate exit 1 — they are not silently swallowed.
- Empty-response guard: skips iterations where the API returns no check runs (CI not yet registered).
- Exits non-zero on failure or timeout so the task notification signals failure correctly.
- Output "CI FAILED" with the failed check names, or "All checks passed" with the full results.

Note: use `$GITHUB_PERSONAL_ACCESS_TOKEN`, NOT `$GITHUB_TOKEN` — the latter is MCP-only.
