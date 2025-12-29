# Deployment Guide

This document explains how to bump versions and deploy packages.

## Version Bumping

Version bumping is done through a manual GitHub Actions workflow.

### Process

1. Go to **Actions** → **Bump Version** → **Run workflow**
2. Select:
   - **Language**: `typescript` or `python`
   - **Bump Type**: `major`, `minor`, `patch`, or `dev`
3. Click **Run workflow**

The workflow will:

- ✅ Verify CI passed on main
- 🔄 Bump the version using `bump_subdir_version.sh`
- 📝 Commit the version change to main
- 🏷️ Create a tag `<language>_v<version>` (if not a dev version)
- 🚀 Trigger deployment automatically (if not a dev version)

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

Deployment happens automatically when a release version tag is pushed, following a pack → deploy pipeline.

### NPM Deployment

**Workflow**: `.github/workflows/typescript_pack_and_deploy.yml`

**Trigger**: Tag matching `typescript_v*` (e.g., `typescript_v0.1.0`)

**Note**: Dev versions are never tagged, so only release versions trigger this workflow.

**Process**:

**Job 1: Pack**

1. Parse version from tag
2. Verify version matches `package.json`
3. Install dependencies
4. Build package
5. Pack tarball
6. Upload artifact

**Job 2: Deploy**

1. Download artifact
2. Publish to npm

**Requirements**:

- `NPM_TOKEN` secret must be configured
- Tag must match `typescript_vX.Y.Z` format (release versions only)
- Version in tag must match version in `package.json`
- CI must have passed on main (enforced by bump workflow)

### PyPI Deployment

_Coming soon_

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
