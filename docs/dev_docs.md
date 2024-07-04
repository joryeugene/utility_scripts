# Final Documentation: Zsh, Neovim, and Python Development

## Zsh Aliases and Functions

- `vim`: Opens Neovim
- `zshconfig`: Edit Zsh configuration file
- `ohmyzsh`: Edit Oh My Zsh configuration
- `nvimconfig`: Edit Neovim configuration
- `sourcezsh`: Reload Zsh configuration
- `update`: Update Homebrew, npm packages, and Oh My Zsh
- `ls`: List files with colors and indicators
- `ll`: Detailed list of files, including hidden files
- `grep`: Search with color highlighting
- `..`: Go up one directory
- `...`: Go up two directories
- `....`: Go up three directories
- `mkcd`: Create a directory and change into it
- `path`: Pretty print the PATH variable

## Neovim Must-Knows

### General
- `:w`: Save file
- `:q`: Quit
- `:wq` or `:x`: Save and quit
- `u`: Undo
- `Ctrl+r`: Redo

### Navigation
- `h`, `j`, `k`, `l`: Move left, down, up, right
- `w`: Move to next word
- `b`: Move to previous word
- `0`: Start of line
- `$`: End of line
- `gg`: Go to first line
- `G`: Go to last line
- `Ctrl+u`: Page up
- `Ctrl+d`: Page down

### Editing
- `i`: Insert mode
- `a`: Append
- `o`: New line below
- `O`: New line above
- `d`: Delete (with motion)
- `y`: Yank (copy)
- `p`: Paste after cursor
- `P`: Paste before cursor

### Custom Mappings
- `<Space>`: Leader key
- `<leader>/`: Toggle comment
- `<leader>w`: EasyMotion word jump
- `<C-n>`: Toggle NERDTree
- `<leader>rn`: Rename (simulated)
- `<leader>gd`: Go to definition (simulated)
- `<leader>gi`: Go to implementation (simulated)
- `<leader>fu`: Find usages (simulated)
- `<leader>ff`: Find files
- `<leader>s`: Select in NERDTree
- `<leader>l`: Reformat code (simulated)
- `<leader>vv`: Edit Neovim config
- `<leader>vr`: Reload Neovim config

## Common Command Lines for Python Development

### Virtual Environment
- `python -m venv venv`: Create a virtual environment
- `source venv/bin/activate`: Activate virtual environment (Unix)
- `venv\Scripts\activate`: Activate virtual environment (Windows)
- `deactivate`: Deactivate virtual environment

### Package Management
- `pip install <package>`: Install a package
- `pip uninstall <package>`: Uninstall a package
- `pip freeze > requirements.txt`: Save current packages to file
- `pip install -r requirements.txt`: Install packages from file

### Python Execution
- `python script.py`: Run a Python script
- `python -m <module>`: Run a module as a script

### Code Quality
- `black .`: Format code with Black
- `flake8 .`: Lint code with Flake8
- `mypy .`: Type check with MyPy
- `pytest`: Run tests with pytest

### Git
- `git init`: Initialize a new Git repository
- `git clone <repo-url>`: Clone a repository
- `git add .`: Stage all changes
- `git commit -m "message"`: Commit staged changes
- `git push origin <branch>`: Push commits to remote
- `git pull origin <branch>`: Pull changes from remote

### Environment Variables
- `export VAR_NAME=value`: Set environment variable (Unix)

### Database (PostgreSQL)
- `psql -d <database>`: Connect to PostgreSQL database
- `createdb <database>`: Create a new database
- `dropdb <database>`: Delete a database

Remember to use `pyenv` for Python version management and `poetry` for dependency management if you have them installed. Always activate your virtual environment before working on your Python projects.
