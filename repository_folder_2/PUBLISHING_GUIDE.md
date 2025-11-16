# Publishing AbuLang to PyPI 📦

## Step-by-Step Guide

### 1. Prepare Your Repository

```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit: AbuLang v3.0.0"
```

### 2. Create PyPI Account

1. Go to https://pypi.org/account/register/
2. Create an account
3. Verify your email
4. Create an API token at https://pypi.org/manage/account/tokens/

### 3. Install Build Tools

```bash
pip install build twine
```

### 4. Update setup.py

Replace these placeholders in `setup.py`:
- `yourusername` → Your GitHub username
- `your.email@example.com` → Your email

### 5. Build the Package

```bash
python -m build
```

This creates:
- `dist/abulang-3.0.0.tar.gz` (source distribution)
- `dist/abulang-3.0.0-py3-none-any.whl` (wheel)

### 6. Upload to PyPI

```bash
twine upload dist/*
```

When prompted, use:
- Username: `__token__`
- Password: Your API token from step 2

### 7. Verify Installation

```bash
pip install abulang
```

Test it:
```python
from abulang import run
run('show "Hello from PyPI!"')
```

## GitHub Setup

### 1. Create Repository

```bash
git remote add origin https://github.com/yourusername/abulang.git
git branch -M main
git push -u origin main
```

### 2. Add GitHub Badges

In README.md, update:
- `yourusername` → Your GitHub username
- `your.email@example.com` → Your email

### 3. Create Release

1. Go to GitHub → Releases
2. Click "Create a new release"
3. Tag: `v3.0.0`
4. Title: `AbuLang v3.0.0`
5. Description: Copy from CHANGELOG
6. Publish release

## Automated Publishing (Optional)

Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [created]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.10'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    - name: Build package
      run: python -m build
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*
```

Then add `PYPI_API_TOKEN` to GitHub Secrets.

## Version Management

### Update Version

1. Edit `setup.py`: Change `version="3.0.0"` to `version="3.1.0"`
2. Commit: `git commit -am "Bump version to 3.1.0"`
3. Tag: `git tag v3.1.0`
4. Push: `git push origin main --tags`
5. Build and upload: `python -m build && twine upload dist/*`

## Maintenance

### Check Package Info

```bash
twine check dist/*
```

### View on PyPI

https://pypi.org/project/abulang/

### Update Documentation

1. Edit README.md
2. Commit and push
3. PyPI auto-updates from GitHub

## Troubleshooting

### "Invalid distribution"
```bash
twine check dist/*
```

### "File already exists"
Delete old dist files:
```bash
rm -rf dist/
python -m build
```

### "Authentication failed"
Check your API token at https://pypi.org/manage/account/tokens/

## Next Steps

1. ✅ Create PyPI account
2. ✅ Build package: `python -m build`
3. ✅ Upload: `twine upload dist/*`
4. ✅ Create GitHub repo
5. ✅ Push code
6. ✅ Create release
7. ✅ Share with community!

## Promotion Ideas

- Post on Reddit: r/Python, r/learnprogramming
- Share on Twitter/X with #Python #Programming
- Add to Awesome Python lists
- Write blog post about AbuLang
- Create tutorial videos
- Submit to Python Weekly newsletter

## Resources

- [PyPI Help](https://pypi.org/help/)
- [Twine Documentation](https://twine.readthedocs.io/)
- [Python Packaging Guide](https://packaging.python.org/)
- [setuptools Documentation](https://setuptools.pypa.io/)

---

**You're ready to publish! 🚀**
