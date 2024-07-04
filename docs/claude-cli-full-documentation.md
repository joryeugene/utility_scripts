# Claude CLI Tool Documentation

## Overview

The Claude CLI tool allows you to interact with the Claude AI assistant from your command line. It supports various features including role-based interactions, context-aware responses using RAG (Retrieval-Augmented Generation), and customizable output formatting.

## Setup

1. Ensure you have Python 3.7+ installed.
2. Install required packages: `pip install anthropic sentence-transformers scikit-learn numpy`
3. Set your Anthropic API key: `export ANTHROPIC_API_KEY='your_api_key_here'`
4. Place the `claude_cli.py` script in your desired location (e.g., `~/scripts/`)
5. Make the script executable: `chmod +x ~/scripts/claude_cli.py`
6. Add an alias to your `.zshrc`: `alias claude='~/scripts/claude_cli.py'`

## Basic Usage

```bash
claude "Your prompt here"
```

## Command-line Arguments

- `--role`: Set a specific role for Claude
- `--temp`: Set the temperature for Claude's responses (0.0 to 1.0)
- `--max-tokens`: Set the maximum number of tokens for Claude's response
- `--save`: Save the response to a markdown file
- `--save-last`: Save the last interaction to a markdown file
- `--save-role`: Save a role configuration for future use
- `--use-role`: Use a previously saved role configuration
- `--list-roles`: List all saved role configurations
- `--set-context-path`: Set the path for context documents
- `--index`: Index local files before querying
- `--stream`: Stream Claude's response in real-time
- `--width`: Set the width for response formatting

## RAG (Retrieval-Augmented Generation) System

### Setting Context Path
```bash
claude --set-context-path "~/your/context/path"
```

### Indexing Files
```bash
claude --index
```

## Role Management

### Saving a Role
```bash
claude --save-role developer --role "full-stack developer" --temp 0.8 --max-tokens 1500
```

### Using a Saved Role
```bash
claude --use-role developer "How do I structure a FastAPI project?"
```

### Listing Saved Roles
```bash
claude --list-roles
```

## Output Management

### Saving Responses
```bash
claude --save "Your prompt here"
```

### Saving Last Interaction
```bash
claude --save-last
```

### Streaming Responses
```bash
claude --stream "Your prompt here"
```

### Formatting Response Width
```bash
claude --width 100 "Your prompt here"
```

## Examples of Usage

1. Basic query:
   ```bash
   claude "Explain the concept of recursion in programming"
   ```

2. Using a specific role:
   ```bash
   claude --role "data scientist" "What are the key steps in feature engineering?"
   ```

3. Adjusting response parameters:
   ```bash
   claude --temp 0.9 --max-tokens 2000 "Write a creative short story about time travel"
   ```

4. Saving a response to a file:
   ```bash
   claude --save story.md "Write a short story about artificial intelligence"
   ```

5. Using a saved role and streaming the response:
   ```bash
   claude --use-role developer --stream "Explain the benefits of containerization in software development"
   ```

6. Indexing local files and then querying with context:
   ```bash
   claude --index
   claude "Summarize the main points from our project documentation"
   ```

7. Changing the context path, indexing, and then querying:
   ```bash
   claude --set-context-path "~/projects/current_project/docs"
   claude --index
   claude "What are the key requirements for our project?"
   ```

8. Saving a role configuration:
   ```bash
   claude --save-role tech_writer --role "technical writer" --temp 0.7 --max-tokens 1800
   ```

9. Using a saved role with custom width:
   ```bash
   claude --use-role tech_writer --width 120 "Write an introduction for a user manual about our new software product"
   ```

10. Streaming a response with a specific role:
    ```bash
    claude --role "cybersecurity expert" --stream "Explain the concept of zero-trust security"
    ```

11. Saving the last interaction after a query:
    ```bash
    claude "What are the principles of responsive web design?"
    claude --save-last
    ```

12. Using RAG with a specific query:
    ```bash
    claude "Based on our project documents, what authentication method are we using?"
    ```

13. Combining multiple options:
    ```bash
    claude --use-role developer --temp 0.8 --max-tokens 2000 --stream --width 100 "Explain the benefits and drawbacks of microservices architecture"
    ```

Remember to adjust the context path and add relevant documents to get the most out of the RAG system. Experiment with different roles, temperatures, and token limits to find the best configuration for your specific needs.
