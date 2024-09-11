
## 🧱 Pull Request template

Please, go through these steps before you submit a PR.

1. Make sure that your PR is not a duplicate or fixes something other PR is already fixing.
2. If not, then make sure that:

   a. You have done your changes in a separate branch. Branches MUST have descriptive names that start with either the `fix/` or `feature/` prefixes. Good examples are: `fix/signin-issue` or `feature/issue-templates`.

   b. You have a descriptive commit messages with a short title (first line).

   c. Make sure `coverage run pytest` doesn't throw any error. If it does, fix them first before submitting.

   d. Format and lint your code running ./scripts/lint.sh command, it will run all the linters used in the project, if there is any issue please fix it before continuing.
3. **After** these steps, you're ready to open a pull request.

   a. Your pull request MUST NOT target the `master` branch on this repository. You probably want to target `develop` instead.

   b. Give a descriptive title to your PR.

   c. Describe your changes.

   d. Put `closes #XXXX` in your purpose to auto-close the issue that your PR fixes (if such).

IMPORTANT: Please review the [CONTRIBUTING.md](../CONTRIBUTING.md) file for detailed contributing guidelines.

**PLEASE REMOVE THIS TEMPLATE BEFORE SUBMITTING AND USE THE ONE BELOW.**


## 🚀 Purpose

What is intended to be achieved with the PR. In case this is linked to a issue/task paste it here.


### 🛠️ Changes

Give a description of the changes made, what did you added, created, modified, fixed. etc


### 🗒️ Documentation

[ ] I have added or updated the documentation.

[ ] No documentation changes were required.


### 🧪 Unit Tests

Paste a screenshot of the tests.


### 👀 Coverage

Paste a screenshot showing that the piece of code you affected has tests coverage.


### 🪄 Linter

Show that the linting script formatted your code successfully.
