# CI

## cloud.aws_troubleshooting Collection

GitHub Actions are used to run the Continuous Integration for redhat-cop/cloud.aws_troubleshooting collection. The workflows used for the CI can be found [here](https://github.com/redhat-cop/cloud.aws_troubleshooting/tree/main/.github/workflows). These workflows include jobs to run the integration tests, sanity tests, linters, and changelog check. The following table lists the python and ansible versions against which these jobs are run.

| Jobs | Description | Python Versions | Ansible Versions |
| ------ |-------| ------ | -----------|
| changelog |Checks for the presence of Changelog fragments | 3.9 | devel |
| Linters | Runs `ansible-lint`, `black`, `flake8`, and `isort` on plugins and tests | 3.9 | devel |
| Sanity | Runs ansible sanity checks | 3.9, 3.10, 3.11, 3.12 | Stable-2.14 (not on py3.12), 2.15 (not on py3.12), 2.16 (not on py 3.9), Milestone, Devel |
| Integration tests | Executes the integration test suites| 3.12 | Milestone |
