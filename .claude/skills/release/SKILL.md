---
name: release
description: Tag and push a new cert-pepper release. Use when the user says "release", "tag a release", "bump the version", or invokes /release.
argument-hint: "[patch|minor|major|x.y.z]"
allowed-tools: Bash
---

Create a new cert-pepper release. The bump type or target version is: **$ARGUMENTS**

Follow these steps exactly, stopping immediately if any step fails:

## 1. Verify clean working tree

```bash
git status --porcelain
```

If there is any output, stop and tell the user: "Working directory is not clean — commit or stash changes first."

## 2. Get current version

```bash
git describe --tags --abbrev=0 2>/dev/null || echo "none"
```

Strip the leading `v` to get the current version number (e.g. `v0.3.0` → `0.3.0`). If no tags exist, use `0.0.0` as the base.

## 3. Compute next version

Parse the current version as `MAJOR.MINOR.PATCH`.

- If `$ARGUMENTS` is `patch` or empty: increment PATCH, reset nothing.
- If `$ARGUMENTS` is `minor`: increment MINOR, set PATCH to 0.
- If `$ARGUMENTS` is `major`: increment MAJOR, set MINOR and PATCH to 0.
- If `$ARGUMENTS` looks like a version number (`x.y.z` or `vx.y.z`): use it directly (strip any leading `v`).

## 4. Confirm with user

Tell the user exactly what you are about to do:

> Ready to release **v{new_version}** (current: v{current_version}).
> This will create an annotated tag, push to origin, and create a GitHub Release.
> Proceed?

Wait for confirmation. Do not proceed until confirmed.

## 5. Create the annotated tag

```bash
git tag -a v{new_version} -m "v{new_version}"
```

## 6. Push branch and tag

```bash
git push origin main
git push origin v{new_version}
```

## 7. Create GitHub Release

Use `gh` to create a release from the tag so it appears in GitHub Releases (not just Tags):

```bash
gh release create v{new_version} --title "v{new_version}" --generate-notes
```

`--generate-notes` auto-populates the release body from commits since the previous tag.

## 8. Report success

Tell the user:

> Released **v{new_version}**: {url returned by gh release create}
>
> hatch-vcs will now resolve this version automatically on any `uv build` or `uv tool install --reinstall`.
> To upgrade an existing install: `uv tool install --reinstall /path/to/cert-pepper`
