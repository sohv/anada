# Deployment Guide for Anada

This guide shows you how to deploy Anada for everyone to use. There are several options depending on your needs.

## Option 1: Publish to PyPI (Recommended for Public Distribution)

This allows anyone to install Anada with `pip install anada`.

### Prerequisites

1. Create accounts on:
   - [PyPI](https://pypi.org/account/register/) (for production releases)
   - [TestPyPI](https://test.pypi.org/account/register/) (for testing releases)

2. Install build tools:
```bash
pip install --upgrade build twine
```

### Step-by-Step Process

#### 1. Update Package Metadata

Edit `pyproject.toml` and update:
- `name` (must be unique on PyPI)
- `author` and `author_email`
- `url` and `Homepage` (your GitHub repo)
- `version` (use semantic versioning: MAJOR.MINOR.PATCH)

#### 2. Prepare Your Package

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info

# Build the package
python -m build

# This creates:
# - dist/anada-0.1.0.tar.gz (source distribution)
# - dist/anada-0.1.0-py3-none-any.whl (wheel distribution)
```

#### 3. Test on TestPyPI (Optional but Recommended)

```bash
# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ anada
```

#### 4. Publish to PyPI

```bash
# Upload to production PyPI
python -m twine upload dist/*

# You'll be prompted for:
# - Username: your PyPI username
# - Password: your PyPI password or API token
```

#### 5. Verify Installation

```bash
# Install from PyPI
pip install anada

# Test it works
anada --version
anada  # Should start the REPL
```

### Updating a Release

1. Update version in `pyproject.toml` and `anada/__init__.py`
2. Rebuild: `python -m build`
3. Re-upload: `python -m twine upload dist/*`

## Option 2: Install from GitHub (For Development/Quick Distribution)

Users can install directly from your GitHub repository.

### Prerequisites

- Push your code to a GitHub repository

### Installation Command

Users can install with:

```bash
pip install git+https://github.com/yourusername/anada.git
```

Or for a specific version/branch:

```bash
pip install git+https://github.com/yourusername/anada.git@main
pip install git+https://github.com/yourusername/anada.git@v0.1.0
```

## Option 3: Local Installation from Source

For local distribution or testing.

### Installation Steps

```bash
# Clone the repository
git clone https://github.com/yourusername/anada.git
cd anada

# Install in development mode (editable)
pip install -e .

# Or install normally
pip install .
```

This installs the `anada` command globally.

## Option 4: Create a Standalone Script

For simple distribution without packaging.

### Create install script

```bash
# Make main.py executable
chmod +x main.py

# Users can:
# 1. Clone the repo
git clone https://github.com/yourusername/anada.git

# 2. Add to PATH (in ~/.bashrc or ~/.zshrc)
export PATH="$PATH:/path/to/anada"

# 3. Or create symlink
ln -s /path/to/anada/main.py /usr/local/bin/anada
```

## Option 5: Create a Docker Image (Advanced)

For containerized deployment.

### Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN pip install -e .

VOLUME ["/root/.notes"]

ENTRYPOINT ["anada"]
```

### Build and Run

```bash
# Build image
docker build -t anada .

# Run container
docker run -it -v ~/.notes:/root/.notes anada
```

## Verification Checklist

Before publishing, make sure:

- [ ] All dependencies are listed in `pyproject.toml`
- [ ] `README.md` is complete and accurate
- [ ] Version numbers match in `pyproject.toml` and `anada/__init__.py`
- [ ] License file is included
- [ ] Entry point is configured correctly (`anada = anada.cli:cli`)
- [ ] Test installation works: `pip install .`
- [ ] The `anada` command works after installation
- [ ] Code is clean and follows best practices

## Post-Deployment

### Announce Your Tool

1. **GitHub Releases**: Create a release tag and notes
2. **Documentation**: Update README with installation instructions
3. **Community**: Share on Reddit (r/commandline, r/Python), Hacker News, etc.
4. **Package Managers**: Consider creating packages for:
   - Homebrew (macOS): `brew install anada`
   - AUR (Arch Linux)
   - Scoop (Windows)

### Maintenance

- Keep dependencies updated
- Fix bugs promptly
- Release new versions regularly
- Respond to issues and PRs

## Troubleshooting

### "Package already exists on PyPI"

- Your package name must be unique
- Change `name` in `pyproject.toml`
- Or contact the owner of the existing package

### "Command not found: anada"

- Check entry points in `pyproject.toml`
- Reinstall: `pip install --force-reinstall .`
- Verify Python bin directory is in PATH

### Build Errors

- Ensure you have latest `build` and `setuptools`
- Check `pyproject.toml` syntax
- Verify all files in MANIFEST.in exist

