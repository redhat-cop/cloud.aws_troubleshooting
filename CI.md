# Continuous Integration (CI)

## AWS Troubleshooting Collection Testing

GitHub Actions are used to run the CI for the cloud.aws_troubleshooting collection. The workflows used for the CI can be found [here](https://github.com/redhat-cop/cloud.aws_troubleshooting/tree/main/.github/workflows). These workflows include jobs to run the sanity tests, linters, integration tests, and changelog checks.

The collection uses reusable workflows from [ansible-network/github_actions](https://github.com/ansible-network/github_actions) for standardized testing.

### PR Testing Workflows

The following tests run on every pull request:

| Job | Description | Python Versions | ansible-core Versions |
| --- | ----------- | --------------- | --------------------- |
| Changelog | Checks for the presence of changelog fragments | ubuntu-latest default | N/A |
| Linters | Runs `ansible-lint` (via dedicated action) and `black`, `flake8`, `isort` (via tox) | 3.10 (tox linters) | N/A |
| Sanity | Runs ansible sanity checks | See compatibility table below | Determined by reusable workflow |
| Integration tests | Executes integration test suites on AWS (split across 2 jobs, requires "safe to test" label) | 3.12 | milestone |

### Python Version Compatibility by ansible-core Version

These are determined by the reusable workflows from [ansible-network/github_actions](https://github.com/ansible-network/github_actions) with specific exclusions applied in the collection's CI configuration.

For the official Ansible core support matrix, see the [Ansible documentation](https://docs.ansible.com/ansible/latest/reference_appendices/release_and_maintenance.html#ansible-core-support-matrix).

The collection's minimum requirements:
- **ansible-core**: >=2.17.0
- **Python**: 3.10+

| ansible-core Version | Sanity Tests | Integration Tests |
| -------------------- | ------------ | ----------------- |
| devel | 3.12, 3.13, 3.14 | - |
| stable-2.20 | 3.12, 3.13, 3.14 | - |
| stable-2.19 | 3.11, 3.12, 3.13 | - |
| stable-2.18 | 3.11, 3.12, 3.13 | - |
| stable-2.17 | 3.10, 3.11, 3.12 | - |
| milestone | - | 3.12 |

**Note**:
- ansible-core 2.16 is completely excluded from testing (reached EOL in May 2025)
- ansible-core 2.17 reached EOL in November 2025

### Testing with `ansible-test`

The `tests` directory contains configuration for running sanity and integration tests using [`ansible-test`](https://docs.ansible.com/ansible/latest/dev_guide/testing_integration.html).

You can run the collection's test suites with the commands:

```shell
# Run sanity tests
ansible-test sanity

# Run integration tests (requires AWS credentials)
ansible-test integration [target]
```

Before running integration tests, you must configure AWS credentials:

```shell
# Using the "default" profile on AWS
aws configure set aws_access_key_id your-access-key
aws configure set aws_secret_access_key your-secret-key
aws configure set region us-east-1
```

The collection also uses `tox` for linting. Assuming this repository is checked out in the proper structure (e.g., `collections_root/ansible_collections/cloud/aws_troubleshooting/`), run:

```shell
# Run all linters (black, flake8, isort)
tox -e linters

# Run ansible-lint separately
tox -e ansible-lint
```

### Integration Test Details

Integration tests have specific characteristics:
- Run on real AWS infrastructure using Ansible Core CI AWS provider
- Split across 2 parallel jobs using `ansible_test_splitter` to reduce test execution time
- Require the "safe to test" label on pull requests to prevent unauthorized AWS resource creation
- Use Python 3.12 with `milestone` ansible-core version
- AWS credentials are provided via the `ansible_aws_test_provider` action, which creates temporary STS session credentials

### Available Integration Test Targets

The collection includes the following integration test targets:
- `test_aws_setup_credentials` - Validates AWS credential setup functionality
- `test_connectivity_troubleshooter` - Tests the main connectivity troubleshooting role and sub-roles
- `test_troubleshoot_rds_connectivity` - Tests RDS-specific connectivity troubleshooting

### Additional Dependencies

The collection depends on the following for integration testing:
- **AWS Environment**: Temporary AWS credentials via Ansible Core CI
- **Python packages**: boto3>=1.26.0, botocore>=1.29.0
- **Collections**: amazon.aws (>=10.0.0), community.aws (>=10.0.0)
- **Collection dependencies source**: Integration tests use the latest `main` branch versions of amazon.aws and community.aws

### Security Model

Integration tests use `pull_request_target` trigger and require explicit approval:
- PRs from external contributors require the "safe to test" label to be added by a maintainer
- This prevents unauthorized execution of tests that create AWS resources
- The `safe-to-test` job validates authorization before any AWS resources are created
