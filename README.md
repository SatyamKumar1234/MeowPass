# MEOWPASS CLI by GgSatyam

A personalized wordlist generator designed for security research, featuring a beautiful CLI, systematic rule-based generation, and an optional AI-enhancement mode.

## Features

-   **Polished CLI:** An easy-to-use and professional interface powered by Rich.
-   **Normal Mode:** Fast, local, and systematic password generation.
-   **AI-Assisted Mode:** Enhances the wordlist with creative, human-like password guesses using Google Gemini or OpenRouter.
-   **Smart Dependencies:** Prompts to install optional AI libraries only when needed.
-   **Safe and Flexible:** Includes checks to prevent saving files in sensitive directories and allows you to choose your save location.

## Installation from GitHub

1.  **Clone the Repository**
    ```bash
    git clone https://your-github-repo-url-here/meowpass-project.git
    cd meowpass-project
    ```

2.  **Install Core Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Install the Tool**
    This makes the `meowpass` command available everywhere in your terminal.
    ```bash
    pip install -e .
    ```

## Installation from PyPI

Once published, you can install MEOWPASS directly:
```bash
# For Normal Mode only
pip install meowpass-cli

# To include AI features
pip install meowpass-cli[ai]