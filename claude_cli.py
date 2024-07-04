#!/usr/bin/env python3

import argparse
import os
import anthropic
import json
from datetime import datetime
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import glob
import textwrap

# Initialize the embedding model for RAG
model = SentenceTransformer('all-MiniLM-L6-v2')

# Simple in-memory vector store (replace with a proper vector database for production)
vector_store = {}

def embed_text(text):
    """Embed the given text using the sentence transformer model."""
    return model.encode([text])[0]

def add_file_to_store(filepath):
    """Read a file and add its embedded content to the vector store."""
    with open(filepath, 'r') as file:
        content = file.read()
    vector_store[filepath] = embed_text(content)

def retrieve_relevant_context(query, top_k=3):
    """Find the most relevant context from the vector store for a given query."""
    query_embedding = embed_text(query)
    similarities = {path: cosine_similarity([query_embedding], [emb])[0][0] for path, emb in vector_store.items()}
    sorted_paths = sorted(similarities.items(), key=lambda x: x[1], reverse=True)[:top_k]
    context = ""
    for path, _ in sorted_paths:
        with open(path, 'r') as file:
            context += f"\nContent from {path}:\n{file.read()}\n"
    return context

def load_config():
    """Load the configuration file for saved roles and context path."""
    config_path = os.path.expanduser('~/.claude_cli_config.json')
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return json.load(f)
    return {'context_path': os.path.expanduser('~/scripts/claude_data'), 'roles': {}}

def save_config(config):
    """Save the configuration file with updated roles and context path."""
    config_path = os.path.expanduser('~/.claude_cli_config.json')
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)

def format_response(response, width=80):
    """Format the response with word wrapping."""
    if isinstance(response, str):
        return textwrap.fill(response, width=width)
    elif isinstance(response, dict):
        return json.dumps(response, indent=2)
    elif isinstance(response, list):
        return "\n".join(textwrap.fill(str(item), width=width) for item in response)
    else:
        return str(response)

class CustomJSONEncoder(json.JSONEncoder):
    """Custom JSON Encoder to handle non-serializable objects."""
    def default(self, obj):
        try:
            return json.JSONEncoder.default(self, obj)
        except TypeError:
            return str(obj)

def chat_with_claude(prompt, role=None, temperature=0.7, max_tokens=None, context="", stream=False):
    """Send a prompt to Claude and return the response, with optional streaming."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is not set")

    client = anthropic.Anthropic(api_key=api_key)
    system_prompt = "You are Claude, an AI assistant created by Anthropic to be helpful, harmless, and honest."
    if role:
        system_prompt += f" You are acting as the assistant to a {role}."

    full_prompt = f"""As an AI assistant, please consider the following context and user query:
Context:
{context}
User query: {prompt}
Please provide a response that addresses the user's query, taking into account the provided context and your knowledge."""

    message_params = {
        "model": "claude-3-5-sonnet-20240620",  # Updated to the newest model
        "max_tokens": max_tokens if max_tokens is not None else 1000,  # Default to 1000 if not provided
        "temperature": temperature,
        "system": system_prompt,
        "messages": [{"role": "user", "content": full_prompt}]
    }

    try:
        if stream:
            full_response = ""
            with client.messages.stream(**message_params) as stream:
                for text in stream.text_stream:
                    print(text, end="", flush=True)
                    full_response += text
                print()  # Final newline
            return full_response
        else:
            message = client.messages.create(**message_params)
            return message.content  # Return the content of the message
    except anthropic.APIError as e:
        print(f"An error occurred while communicating with the Claude API: {e}")
        return None

def save_to_markdown(prompt, response, filename=None):
    """Save the prompt and response to a markdown file."""
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"claude_response_{timestamp}.md"
    with open(filename, 'w') as f:
        f.write(f"# Claude Response\n\n")
        f.write(f"## Prompt\n\n{prompt}\n\n")
        f.write(f"## Response\n\n{response}\n")
    print(f"Response saved to {filename}")

def save_last_interaction(prompt, response):
    """Save the last interaction to a JSON file."""
    last_interaction = {
        'timestamp': datetime.now().isoformat(),
        'prompt': prompt,
        'response': response
    }
    with open(os.path.expanduser('~/.claude_last_interaction.json'), 'w') as f:
        json.dump(last_interaction, f, indent=2, cls=CustomJSONEncoder)

def load_last_interaction():
    """Load the last interaction from the JSON file."""
    try:
        with open(os.path.expanduser('~/.claude_last_interaction.json'), 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def main():
    """Main function to handle command-line arguments and execute the appropriate actions."""
    config = load_config()

    parser = argparse.ArgumentParser(description="Chat with Claude from the command line.")
    parser.add_argument("prompt", nargs="*", help="The prompt to send to Claude")
    parser.add_argument("--role", help="Set a specific role for Claude (e.g., 'full-stack developer at a cutting-edge startup')")
    parser.add_argument("--temp", type=float, help="Set the temperature for Claude's responses")
    parser.add_argument("--max-tokens", type=int, help="Set the maximum number of tokens for Claude's response")
    parser.add_argument("--save", nargs='?', const=True, help="Save the response to a markdown file. Optionally specify a filename.")
    parser.add_argument("--save-role", help="Save a role configuration for future use")
    parser.add_argument("--use-role", help="Use a saved role configuration")
    parser.add_argument("--list-roles", action="store_true", help="List all saved role configurations")
    parser.add_argument("--save-last", action="store_true", help="Save the last interaction to a markdown file")
    parser.add_argument("--set-context-path", help="Set the path for context documents")
    parser.add_argument("--index", action="store_true", help="Index local files before querying")
    parser.add_argument("--stream", action="store_true", help="Stream Claude's response in real-time")
    parser.add_argument("--width", type=int, default=80, help="Set the width for response formatting")
    args = parser.parse_args()

    if args.set_context_path:
        config['context_path'] = os.path.expanduser(args.set_context_path)
        save_config(config)
        print(f"Context path set to: {config['context_path']}")
        return

    if args.index:
        context_path = os.path.expanduser(config['context_path'])
        os.makedirs(context_path, exist_ok=True)  # Create the directory if it doesn't exist
        for filepath in glob.glob(os.path.join(context_path, '*')):
            add_file_to_store(filepath)
        print(f"Indexed local files from: {context_path}")
        return

    if args.save_role:
        config['roles'] = config.get('roles', {})
        config['roles'][args.save_role] = {
            'role': args.role,
            'temperature': args.temp,
            'max_tokens': args.max_tokens
        }
        save_config(config)
        print(f"Saved role configuration: {args.save_role}")
        return

    if args.list_roles:
        roles = config.get('roles', {})
        if roles:
            print("Saved role configurations:")
            for name, details in roles.items():
                print(f" {name}: {details}")
        else:
            print("No saved role configurations.")
        return

    if args.save_last:
        last_interaction = load_last_interaction()
        if last_interaction:
            save_to_markdown(last_interaction['prompt'], last_interaction['response'])
        else:
            print("No previous interaction found.")
        return

    if args.use_role:
        role_config = config.get('roles', {}).get(args.use_role)
        if role_config:
            args.role = role_config.get('role', args.role)
            args.temp = float(role_config.get('temperature', args.temp)) if role_config.get('temperature') is not None else None
            args.max_tokens = role_config.get('max_tokens', args.max_tokens)
        else:
            print(f"No saved configuration found for role: {args.use_role}")
        return

    if not args.prompt:
        prompt = input("Enter your prompt: ")
    else:
        prompt = " ".join(args.prompt)

    context = retrieve_relevant_context(prompt) if vector_store else ""

    # Provide default values and ensure correct types
    max_tokens = int(args.max_tokens) if args.max_tokens is not None else 1000
    temperature = float(args.temp) if args.temp is not None else 0.7

    response = chat_with_claude(prompt, args.role, temperature, max_tokens, context, args.stream)

    if response:
        if not args.stream:
            formatted_response = format_response(response, args.width)
            print(formatted_response)
        save_last_interaction(prompt, response)
        if args.save:
            save_to_markdown(prompt, formatted_response, args.save if isinstance(args.save, str) else None)
    else:
        print("Failed to get a response from Claude.")

if __name__ == "__main__":
    main()
