# Claude CLI Tool Documentation

## Basic Usage

```bash
claude "Your prompt here"
```

This will send your prompt to Claude and display the response.

## Command-line Arguments

### --role

Set a specific role for Claude:

```bash
claude --role "full-stack developer at a cutting-edge startup" "How should I structure a FastAPI project?"
```

### --temp

Set the temperature for Claude's responses (0.0 to 1.0):

```bash
claude --temp 0.8 "Generate creative ideas for a new web app"
```

### --max-tokens

Set the maximum number of tokens for Claude's response:

```bash
claude --max-tokens 2000 "Explain the concept of dependency injection in detail"
```

### --save

Save the response to a markdown file:

```bash
claude --save "What are the best practices for API design?"
```

You can also specify a filename:

```bash
claude --save my_api_notes.md "What are the best practices for API design?"
```

### --save-last

Save the last interaction to a markdown file:

```bash
claude --save-last
```

### --save-role

Save a role configuration for future use:

```bash
claude --save-role fullstack --role "full-stack developer at a cutting-edge startup" --temp 0.8 --max-tokens 1500
```

### --use-role

Use a previously saved role configuration:

```bash
claude --use-role fullstack "How should I implement authentication in FastAPI?"
```

### --list-roles

List all saved role configurations:

```bash
claude --list-roles
```

## RAG (Retrieval-Augmented Generation) System

### Indexing Local Files

Before using the RAG system, you need to index your local files:

```bash
claude-index
```

### Using RAG

After indexing, your queries will automatically use relevant information from your local files:

```bash
claude "How does our project handle database migrations?"
```

## Tips for Effective Use

1. Be specific in your prompts for more accurate responses.
2. Use the `--role` argument to contextualize Claude's responses for your specific needs.
3. Adjust the `--temp` argument for more creative (higher) or more focused (lower) responses.
4. Use the RAG system when you want Claude to consider your local project files in its responses.
5. Save important interactions using the `--save` or `--save-last` arguments for future reference.
6. Create and use role configurations to quickly switch between different contexts or projects.

## Extending the Tool

The Claude CLI tool is built with Python and can be extended further. Some ideas for extension:

- Integrate with your IDE for in-editor querying
- Add support for code generation templates
- Implement project-specific commands (e.g., database schema analysis, API endpoint summaries)
- Create a web interface for easier interaction and result browsing

Remember to keep your API key secure and never share it publicly. If you suspect your key has been compromised, regenerate it immediately through the Anthropic dashboard.
