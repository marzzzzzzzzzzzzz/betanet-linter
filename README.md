# Betanet Spec-Compliance Linter

A command-line tool that automatically checks Betanet program binaries against all 11 required specification features and generates a Software Bill of Materials (SBOM).

## Features

- ✅ Checks all 11 required Betanet specification features
- 📦 Generates CycloneDX-compatible SBOM
- ⚙️ Ready-to-use GitHub Action template
- 📝 Detailed pass/fail reporting
 - 🔄 JSON and text output formats

## GitHub Actions

This repository includes a ready‑made GitHub Actions workflow at
`.github/workflows/betanet-linter.yml`.  The workflow can be triggered manually
from your repository’s **Actions** tab or incorporated into your continuous
integration pipeline.  It installs the linter, runs all 11 checks against the
binary you specify and uploads both the compliance report and SBOM as workflow
artifacts.  When invoking the workflow manually, provide the relative path to
your candidate binary via the `binary-path` input.

## Installation

### From Source

```bash
# On Windows:
cd D:\Programming\betanet LINTER
python -m venv venv
venv\Scripts\activate
pip install -e .