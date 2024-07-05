# Claude CLI

Claude CLI is a command-line interface for interacting with the Claude AI model using the Anthropic API. It provides features for context-aware querying, document indexing, and conversation management.

## Features

- Query Claude AI with context from indexed documents
- Index local files for context retrieval
- Manage conversation history
- Set custom roles for Claude
- Adjust temperature and max tokens for responses
- Stream Claude's responses in real-time (default behavior)

## Prerequisites

- Python 3.7+
- Anthropic API key

## Installation

1. Clone this repository:

2. Install the required dependencies:

    ```sh
    pip install anthropic sentence-transformers scikit-learn
    ```

3. Set your Anthropic API key as an environment variable:

    ```sh
    export ANTHROPIC_API_KEY='your_api_key_here'
    ```

## Usage

The basic syntax for using the Claude CLI is:

   ```
   python3 claude_cli.py [options] [prompt]
   ```

### Command-line Arguments

- `prompt`: The query or prompt to send to Claude.
- `-r, --role ROLE`: Set a specific role for Claude (e.g., "data scientist", "writer").
- `-t, --temp TEMP`: Set the temperature for Claude's responses (default: 0.7).
- `-m, --max-tokens MAX_TOKENS`: Set the maximum number of tokens for Claude's response.
- `--set-context-path PATH`: Set the path for context documents.
- `--index`: Index local files before querying.
- `--clear-index`: Clear the indexed documents.
- `--clear-history`: Clear the conversation history.
- `--save [FILENAME]`: Save the response to a markdown file. If no filename is specified, it uses a timestamp-based name.
- `--save-last [FILENAME]`: Save the last interaction to a file. If no filename is specified, it saves to `~/.claude_last_interaction.json`.
- `--save-role ROLE`: Save a role configuration for future use.
- `--use-role ROLE`: Use a saved role configuration.
- `--list-roles`: List all saved role configurations.
- `--stream`: Stream Claude's response in real-time.

### Examples

#### Basic Query

```
    python3 claude_cli.py "What is the capital of France?"
```

#### Set Context Path

```
    python3 claude_cli.py --set-context-path "/Users/jory/scripts/claude_data"
```

#### Index Documents

```
    python3 claude_cli.py --index
```

#### Query with Context

```
    python3 claude_cli.py "Summarize the main points of the sample RAG content"
```

#### Query with Custom Role

```
    python3 claude_cli.py --role "data scientist" "Analyze this dataset and provide insights"
```

#### Adjust Response Parameters

```
    python3 claude_cli.py --temp 0.8 --max-tokens 500 "Generate a short story about a robot"
```

#### Clear Index

```
    python3 claude_cli.py --clear-index
```

#### Clear Conversation History

```
    python3 claude_cli.py --clear-history
```

#### Saving Responses

Save the current response to a specific file:

```
    python3 claude_cli.py --save my_response.md "What are the three laws of robotics?"
```

Save the current response with an auto-generated filename:

```
    python3 claude_cli.py --save "Explain quantum computing"
```

Save the last interaction:

```
    python3 claude_cli.py --save-last
```

Save the last interaction to a specific file:

```
    python3 claude_cli.py --save-last last_chat.json
```

### Managing Roles

Save a role configuration:

```
    python3 claude_cli.py --save-role "science_expert" --role "expert scientist" --temp 0.5 --max-tokens 2000
```

Use a saved role:

```
    python3 claude_cli.py --use-role "science_expert" "Explain the theory of relativity"
```

List saved roles:

```
    python3 claude_cli.py --list-roles
```

### Streaming Responses

To stream Claude's responses in real-time:

```
    python3 claude_cli.py --stream "Write a short story about a time traveler"
```

### Using the `claude_project` Alias

You can create a `claude_project` alias in your shell configuration file (e.g., `.zshrc` or `.bashrc`) for easier usage:

```
    function claude_project() {
        local project_name=$1
        local context_path="$HOME/projects/$project_name/docs"
        local claude_cli="python3 $HOME/scripts/claude_cli.py"
        
        $claude_cli --set-context-path "$context_path"
        $claude_cli --index
        $claude_cli "Analyze the documents in the context path and summarize the main features of the project they describe. Focus on providing a concise overview highlighting key aspects."
    }
```

Usage:
```
    claude_project test
```

This will set the context path to `/Users/jory/projects/test/docs`, index the documents, and ask Claude to analyze and summarize the project.

### Advanced Examples

#### Analyzing the Claude CLI Code

Set the context to the scripts repository:

```
    python3 claude_cli.py --set-context-path "/Users/jory/scripts"
    python3 claude_cli.py --index
```

Ask Claude to explain a function:

```
    python3 claude_cli.py "Explain the 'chat_with_claude' function in the claude_cli.py script"
```

Request documentation for the script:

```
    python3 claude_cli.py "Generate comprehensive documentation for the claude_cli.py script, including all functions and their purposes"
```

#### Using the Sample RAG Content

Set the context to the `claude_data` folder:

```
    python3 claude_cli.py --set-context-path "/Users/jory/scripts/claude_data"
    python3 claude_cli.py --index
```

Ask questions about the content:

```
    python3 claude_cli.py "What is the main focus of TechNova, and what are the key features of their SmartCommute platform?"
```

Request a detailed analysis:

```
    python3 claude_cli.py "Provide a comprehensive analysis of the urban mobility solution described in the sample RAG content, including potential challenges and future improvements"
```

#### Combining Multiple Contexts

Index multiple directories:

```
    python3 claude_cli.py --set-context-path "/Users/jory/scripts"
    python3 claude_cli.py --index
    python3 claude_cli.py --set-context-path "/Users/jory/scripts/claude_data"
    python3 claude_cli.py --index
```

Ask a question that requires knowledge from both contexts:

```
    python3 claude_cli.py "Compare the features of the SmartCommute platform described in the sample RAG content with the capabilities of the Claude CLI script. How might they complement each other in an urban mobility project?"
```

#### Using Claude for Code Review

Set the context to your project's source code:

```
    python3 claude_cli.py --set-context-path "/path/to/your/project"
    python3 claude_cli.py --index
```

Ask for a code review:

```
    python3 claude_cli.py "Perform a code review of the main application file. Identify any potential issues, suggest improvements, and comment on the overall code quality."
```

#### Generating Project Documentation

Set the context to your project:

```
    python3 claude_cli.py --set-context-path "/path/to/your/project"
    python3 claude_cli.py --index
```

Generate documentation:

```
    python3 claude_cli.py "Generate comprehensive project documentation, including an overview, installation instructions, usage examples, and API documentation for all public functions and classes."
```

## Configuration

The script uses the following configuration files:

- `~/.claude_cli_config.json`: Stores general configuration
- `~/.claude_vector_store.pkl`: Stores indexed document embeddings
- `~/.claude_context_history.json`: Stores conversation history

## Troubleshooting

If you encounter any issues:

- Ensure your Anthropic API key is correctly set in your environment variables.
- Check that all required dependencies are installed.
- Verify that the context path is set correctly and contains the expected documents.
- If you're not getting relevant responses, try clearing the index and re-indexing your documents.
