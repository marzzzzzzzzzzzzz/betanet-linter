from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="betanet-linter",
    version="1.0.0",
    author="Betanet Compliance Team",
    author_email="compliance@betanet.example",
    description="A spec-compliance linter for Betanet programs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/betanet-linter",  # Update with your repo
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    install_requires=[],
    entry_points={
        "console_scripts": [
            "betanet-linter=betanet_linter.cli:main",
        ],
    },
)