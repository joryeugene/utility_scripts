# Claude CLI Python Environment Management

## Setting Up and Managing Python Environments

The Claude CLI tool uses its own virtual environment to avoid conflicts with system Python packages. Here's how to manage different Python environments:

### Virtual Environment for Claude CLI

1. Create the virtual environment:
   ```bash
   python3 -m venv ~/claude_env
   ```

2. Activate the Claude virtual environment:
   ```bash
   source ~/claude_env/bin/activate
   ```
   Or use the alias:
   ```bash
   activate_claude
   ```

3. Deactivate the Claude virtual environment:
   ```bash
   deactivate
   ```
   Or use the alias:
   ```bash
   deactivate_claude
   ```

### Switching Between Python Environments

1. Use system Python:
   ```bash
   use_system_python
   ```
   This removes pyenv paths from your PATH environment variable.

2. Use pyenv-managed Python versions:
   ```bash
   use_pyenv
   ```
   This reinitializes pyenv in your current shell.

### Installing Packages

1. For Claude CLI (when Claude environment is active):
   ```bash
   pip install package_name
   ```

2. For system Python:
   ```bash
   pip3 install --user package_name
   ```
   Or use Homebrew:
   ```bash
   brew install python-package_name
   ```

3. For pyenv-managed Python:
   Activate the desired pyenv version, then:
   ```bash
   pip install package_name
   ```

### Best Practices

1. Always use the Claude virtual environment when working with the Claude CLI tool.
2. Use separate virtual environments for different projects to avoid package conflicts.
3. Be cautious when installing packages globally (system-wide) to prevent potential conflicts.
4. Regularly update your environments and packages to ensure you have the latest features and security updates.

### Troubleshooting

If you encounter "command not found" errors:
1. Ensure you're in the correct environment.
2. Check if the package is installed: `pip list`
3. Verify your PATH includes the correct Python binary: `which python3`

Remember to source your `.zshrc` after making changes:
```bash
source ~/.zshrc
```
