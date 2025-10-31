# Quick Deployment Guide

## For Testing Locally

```bash
# Install from current directory
pip install -e .

# Test it works
anada --version
anada  # Start interactive mode
```

## For Publishing to PyPI

### First Time Setup

1. **Create PyPI accounts:**
   - [PyPI](https://pypi.org/account/register/)
   - [TestPyPI](https://test.pypi.org/account/register/) (for testing)

2. **Install build tools:**
   ```bash
   pip install --upgrade build twine
   ```

3. **Update package metadata:**
   - Edit `pyproject.toml`:
     - Change `name` (must be unique on PyPI)
     - Update `author`, `author_email`
     - Update `url` and `Homepage` (your GitHub repo)

### Build and Publish

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info

# Build package
python -m build

# Test on TestPyPI first (recommended)
python -m twine upload --repository testpypi dist/*

# If test works, publish to PyPI
python -m twine upload dist/*
```

### Users Install With

```bash
pip install anada
```

## For GitHub Distribution

Users can install directly from GitHub:

```bash
pip install git+https://github.com/yourusername/anada.git
```

## Automated Publishing with GitHub Actions

1. **Create PyPI API token:**
   - Go to PyPI → Account Settings → API Tokens
   - Create a new API token
   - Copy the token

2. **Add to GitHub Secrets:**
   - Go to your GitHub repo → Settings → Secrets and variables → Actions
   - Add new secret: `PYPI_API_TOKEN` with your token

3. **Publish releases:**
   - Create a new release tag on GitHub (e.g., `v0.1.0`)
   - GitHub Actions will automatically publish to PyPI

## Quick Commands Reference

```bash
# Build package
python -m build

# Test package locally
pip install -e .

# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*

# Upload to PyPI
python -m twine upload dist/*

# Install from PyPI
pip install anada

# Install from GitHub
pip install git+https://github.com/yourusername/anada.git
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

