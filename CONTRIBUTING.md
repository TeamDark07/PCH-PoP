# Contributing to Practical Python Concurrency (PPC)

First off, thank you for considering contributing! This project is a community effort, and every contribution, from a small typo fix to a new code example, is valuable.

This document provides guidelines to make the contribution process smooth and effective for everyone.

## Table of Contents
*   [How Can I Contribute?](#how-can-i-contribute)
    *   [Reporting Bugs or Typos](#reporting-bugs-or-typos)
    *   [Suggesting Enhancements](#suggesting-enhancements)
    *   [Submitting a Pull Request](#submitting-a-pull-request)
*   [Development Setup](#development-setup)
*   [Style Guides](#style-guides)
    *   [Python Code](#python-code)
    *   [Git Commit Messages](#git-commit-messages)

## How Can I Contribute?

### Reporting Bugs or Typos

If you find a bug in the code, a typo in the documentation, or an explanation that is unclear, please [open an issue](https://github.com/Eng-AliKazemi/PCH-PoP/issues).

Before opening a new issue, please check the existing issues to see if your problem has already been reported.

When creating a bug report, please include:
*   A clear and descriptive title.
*   A detailed description of the problem.
*   The location of the issue (e.g., a link to a line in `GUIDE.md` or a path to an example file).
*   If it's a code bug, steps to reproduce the behavior.

### Suggesting Enhancements

If you have an idea for a new example, a new section for the guide, or an improvement to an existing part, please [open an issue](https://github.com/Eng-AliKazemi/PCH-PoP/issues) to discuss it. This allows us to coordinate efforts and ensure the suggestion aligns with the project's goals.

### Submitting a Pull Request

Ready to contribute code or documentation? Great! Follow these steps to submit a Pull Request (PR):

1.  **Fork the Repository:** Create your own copy of the project by clicking the "Fork" button at the top right of the main repository page.

2.  **Clone Your Fork:** Clone your forked repository to your local machine.
    ```bash
    git clone https://github.com/Eng-AliKazemi/PPC.git
    cd practical-python-concurrency
    ```

3.  **Create a New Branch:** Create a descriptive branch name for your changes.
    ```bash
    # For a new feature or example:
    git checkout -b feature/add-spinlock-example

    # For a bug fix or typo:
    git checkout -b fix/correct-deadlock-explanation
    ```

4.  **Make Your Changes:**
    *   Edit the code and/or documentation.
    *   If you add a new concurrency issue, please create a new folder in the `examples/` directory with `bad_example.py`, `good_example.py`, and a `README.md`.
    *   Ensure you also update the main `GUIDE.md` and the top-level `README.md` if necessary.

5.  **Commit Your Changes:** Commit your changes with a clear and descriptive commit message. See our [Git Commit Messages](#git-commit-messages) style guide.
    ```bash
    git add .
    git commit -m "feat: Add new example for Spinlocks"
    ```

6.  **Push to Your Fork:** Push your new branch to your forked repository on GitHub.
    ```bash
    git push origin feature/add-spinlock-example
    ```

7.  **Open a Pull Request:** Go to your fork on GitHub. You will see a prompt to create a Pull Request. Provide a clear title and a detailed description of the changes you've made.

8.  **Wait for Review:** The maintainers will review your Pull Request and provide feedback. If changes are needed, you can make them in your branch and push them to GitHub. The review process may take some time, as the maintainers are volunteers.

9.  **Merge the Pull Request:** Once your changes are approved, the maintainers will merge your Pull Request into the main repository.
