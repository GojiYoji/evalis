# Deployment Guide

This document explains how to bump versions and deploy packages.

## Version Bumping

Version bumping is done locally using the `bump_subdir_version.sh` script, followed by creating a tag via GitHub Actions.

### Process

**Step 1: Bump Version Locally**

```bash
# Bump version (creates commit automatically)
./support/bump_subdir_version.sh <language> <bump-type>

# Examples:
./support/bump_subdir_version.sh typescript minor
./support/bump_subdir_version.sh python dev

# Optional flags:
./support/bump_subdir_version.sh typescript patch --no-commit  # Skip auto-commit
./support/bump_subdir_version.sh python major --force          # Allow uncommitted changes
```

The script will:

- Bump the version using semantic versioning rules
- Auto-commit the change (unless `--no-commit` or `--force` is used)
- Display next steps

**Step 2: Create PR and Merge**

1. Push your branch: `git push origin <branch-name>`
2. Create a pull request
3. Wait for CI checks to pass
4. Merge to main

**Step 3: Tag the Release**

After your PR is merged to main:

1. Go to **Actions** → **Tag Version** → **Run workflow**
2. Select the **Language** you want to tag (must match the version you just bumped)
3. Click **Run workflow**

The workflow will:

- Verify CI passed on main
- Read the current version from the repo
- Error if version is dev (can't tag dev versions)
- Error if tag already exists
- Create and push tag `<language>_v<version>`
- Trigger deployment automatically

### Version Bump Types

- **major**: `1.2.3` → `2.0.0` (breaking changes)
- **minor**: `1.2.3` → `1.3.0` (new features)
- **patch**: `1.2.3` → `1.2.4` (bug fixes)
- **dev**: `1.2.3` → `1.2.4-dev` (development cycle)

### Examples

**Starting a new development cycle after releasing 0.1.0:**

```
Bump Type: dev
Result: 0.1.0 → 0.1.1-dev
Tag: None (dev version)
```

**Releasing the accumulated changes:**

```
# If changes are just bug fixes
Bump Type: patch
Result: 0.1.1-dev → 0.1.1
Tag: typescript_v0.1.1

# If changes include new features
Bump Type: minor
Result: 0.1.1-dev → 0.2.0
Tag: typescript_v0.2.0
```

## Deployment

Deployment happens automatically when you create a release tag via the Tag Version workflow. The deployment follows a pack → deploy pipeline that validates, builds, and publishes the package.

### How to Deploy a Package

1. **Bump the version** (see Version Bumping section above)
2. **Create PR and merge to main**
3. **Run the Tag Version workflow**:
   - Go to **Actions** → **Tag Version** → **Run workflow**
   - Select the language (typescript or python)
   - The workflow will create a tag like `typescript_v0.1.3` or `python_v0.1.0`
4. **Deployment runs automatically** when the tag is pushed

The deployment workflow will:

- Build and pack the package
- Validate the package
- Publish to npm (TypeScript) or PyPI (Python)
- Create a deployment summary

## Tag Format

Release version tags follow the pattern: `<language>_v<version>`

Examples:

- `typescript_v0.1.0`
- `typescript_v1.2.3`
- `python_v0.1.0` (future)

**Important**: Dev versions (`X.Y.Z-dev`) are never tagged. Only release versions (major/minor/patch bumps) create tags and trigger deployment.

## Troubleshooting

### "CI has not passed on main"

The bump workflow requires that all CI checks pass on the main branch before bumping versions.

**Solution**: Wait for CI to pass, or fix any failing checks.

### "Version mismatch"

The deployment workflow detected that the tag version doesn't match the package version.

**Solution**: This shouldn't happen if using the bump workflow. If manually creating tags, ensure they match the package version.

### NPM publish fails

**Common causes**:

- Invalid or expired `NPM_TOKEN`
- Version already published to npm
- Package name already taken (first publish)

**Solution**: Check npm token and verify the version hasn't been published yet.
