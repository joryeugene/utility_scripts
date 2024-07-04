# Neovim and Plugin Usage Guide

## Neovim Basics
- `:w` - Save file
- `:q` - Quit
- `:wq` or `:x` - Save and quit
- `i` - Enter insert mode
- `esc` - Exit insert mode
- `/` - Search (use `n` for next, `N` for previous)

## NERDTree
- `Ctrl+n` - Toggle NERDTree
- `o` - Open file/directory
- `t` - Open in new tab
- `i` - Open in split
- `s` - Open in vertical split
- `I` - Toggle hidden files

## Other Plugins
- FZF: `Ctrl+p` - Fuzzy file search
- Git Gutter: 
  - `]c` - Next hunk
  - `[c` - Previous hunk
- Vim Fugitive: 
  - `:Gstatus` - Git status
  - `:Gcommit` - Git commit

# Alias Usage Guide

## Git Aliases
- `g` - git
- `gst` - git status
- `ga` - git add
- `gc` - git commit
- `gp` - git push

## Directory Navigation
- `..` - Go up one directory
- `...` - Go up two directories
- `~` - Go to home directory

## Python Environment
- `activate_claude` - Activate Claude environment
- `deactivate_claude` - Deactivate Claude environment
- `use_system_python` - Use system Python
- `use_pyenv` - Use pyenv-managed Python

# Claude CLI Usage Guide

## Basic Usage
```bash
claude "Your prompt here"
```

## Advanced Options
- `--role`: Set a specific role
- `--temp`: Set temperature
- `--max-tokens`: Set max tokens
- `--save`: Save response to file
- `--stream`: Stream response in real-time

## Examples
```bash
claude --role "data scientist" --temp 0.7 "Explain PCA"
claude --save analysis.md "Analyze this dataset: ..."
claude --stream "Write a short story about AI"
```

# Python Development Best Practices

## Virtual Environments
- Create: `python -m venv myenv`
- Activate: `source myenv/bin/activate`
- Deactivate: `deactivate`

## Dependency Management
- Use `requirements.txt` or `Pipfile`
- Install dependencies: `pip install -r requirements.txt`

## Code Style
- Follow PEP 8
- Use a linter (e.g., flake8)
- Use a formatter (e.g., black)

## Testing
- Write unit tests using pytest
- Run tests: `pytest`

# Database and Docker Setup

## PostgreSQL with Docker
1. Pull PostgreSQL image:
   ```
   docker pull postgres
   ```
2. Run PostgreSQL container:
   ```
   docker run --name my-postgres -e POSTGRES_PASSWORD=mysecretpassword -d -p 5432:5432 postgres
   ```

## Docker Compose for Development
Create a `docker-compose.yml`:

```yaml
version: '3'
services:
  db:
    image: postgres
    environment:
      POSTGRES_PASSWORD: mysecretpassword
  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/code
    ports:
      - "8000:8000"
    depends_on:
      - db
```

Run with: `docker-compose up`

# Miscellaneous Development Tips

- Use version control (Git) for all projects
- Write clear, self-documenting code
- Document your code and APIs
- Regularly update your tools and dependencies
- Use continuous integration for automated testing
- Implement proper error handling and logging
- Optimize your development environment for productivity
- Regularly back up your work
- Stay updated with the latest trends and best practices in your field
