# Continuous Integration (CI)

## AWS Troubleshooting Collection Testing

GitHub Actions are used to run the CI for the cloud.aws_troubleshooting collection. The workflows used for the CI can be found in the [.github/workflows](.github/workflows) directory.

### PR Testing Workflows

The following tests run on every pull request:

| Job | Description | Python Versions | ansible-core Versions |
| --- | ----------- | --------------- | --------------------- |
| [Changelog](.github/workflows/changelog.yaml) | Checks for the presence of changelog fragments | 3.12 | devel |
| [Linters](.github/workflows/linters.yaml) | Runs `black`, `flake8`, `isort`, and `ansible-lint` on plugins and tests | 3.10 | devel |
| [Sanity](.github/workflows/sanity.yaml) | Runs ansible sanity checks | See compatibility table below | devel, stable-2.17, stable-2.18, stable-2.19, stable-2.20 |
| [Integration](.github/workflows/integration.yaml) | Executes integration test suites on AWS (split across 2 jobs, requires "safe to test" label) | 3.12 | milestone |

**Note:** Integration tests run on real AWS infrastructure and require the "safe to test" label on pull requests to prevent unauthorized AWS resource creation.

### Python Version Compatibility by ansible-core Version

These are outlined in the collection's [tox.ini](tox.ini) file (`envlist`) and GitHub Actions workflow exclusions.

| ansible-core Version | Sanity Tests |
| -------------------- | ------------ |
| devel | 3.12, 3.13, 3.14 |
| stable-2.20 | 3.12, 3.13, 3.14 |
| stable-2.19 | 3.11, 3.12, 3.13 |
| stable-2.18 | 3.11, 3.12, 3.13 |
| stable-2.17 | 3.10, 3.11, 3.12 |
