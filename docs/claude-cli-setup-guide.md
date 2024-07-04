# Claude CLI Setup and Usage Guide

## Setup

1. Save the script:
   Save the provided `claude_cli.py` script in your scripts directory, e.g., `~/scripts/claude_cli.py`.

2. Make the script executable:
   ```bash
   chmod +x ~/scripts/claude_cli.py
   ```

3. Add an alias to your `~/.zshrc`:
   ```bash
   alias claude='~/scripts/claude_cli.py'
   ```

4. Source your `.zshrc`:
   ```bash
   source ~/.zshrc
   ```

5. Install required Python packages:
   ```bash
   pip3 install anthropic sentence-transformers scikit-learn numpy
   ```

6. Set up your Anthropic API key:
   Add this line to your `~/.zshrc`, replacing `your_api_key_here` with your actual API key:
   ```bash
   export ANTHROPIC_API_KEY='your_api_key_here'
   ```

7. Source your `.zshrc` again:
   ```bash
   source ~/.zshrc
   ```

## Usage

### Basic Usage
```bash
claude "Your prompt here"
```

### Setting and Using the Context Path

Default path: `~/scripts/claude_data`

To change the context path:
```bash
claude --set-context-path "~/your/preferred/path"
```

To index files in the context path:
```bash
claude --index
```

### Saving Responses
```bash
claude --save "Your prompt here"
```
This saves the response to a markdown file with a timestamp.

To specify a filename:
```bash
claude --save custom_filename.md "Your prompt here"
```

### Using Roles

Save a role configuration:
```bash
claude --save-role developer --role "full-stack developer" --temp 0.8 --max-tokens 1500
```

Use a saved role:
```bash
claude --use-role developer "How do I structure a FastAPI project?"
```

List saved roles:
```bash
claude --list-roles
```

### Other Options

- Set temperature: `--temp 0.8`
- Set max tokens: `--max-tokens 1000`
- Save last interaction: `--save-last`

## Examples

1. Basic query:
   ```bash
   claude "What are the key features of Python?"
   ```

2. Using a role with custom settings:
   ```bash
   claude --role "data scientist" --temp 0.7 --max-tokens 2000 "Explain the concept of feature engineering"
   ```

3. Using a saved role and saving the response:
   ```bash
   claude --use-role developer --save "Best practices for API design in FastAPI"
   ```

4. Indexing files and then querying with context:
   ```bash
   claude --index
   claude "Summarize the main points from our project documentation"
   ```

5. Changing the context path and indexing:
   ```bash
   claude --set-context-path "~/projects/current_project/docs"
   claude --index
   claude "What are the key requirements for our project?"
   ```

Remember to add relevant documents to your context path before indexing for the RAG system to work effectively.
