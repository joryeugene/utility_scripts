#!/usr/bin/env python3

import argparse
import os
import anthropic
import json
from datetime import datetime
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import glob
import pickle
import sys
from typing import Dict, List, Tuple, Optional

# Set the environment variable to disable the tokenizers parallelism warning
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Constants for file paths
MODEL = SentenceTransformer('all-MiniLM-L6-v2')
CONFIG_PATH = os.path.expanduser('~/.claude_cli_config.json')
VECTOR_STORE_PATH = os.path.expanduser('~/.claude_vector_store.pkl')
CONTEXT_HISTORY_PATH = os.path.expanduser('~/.claude_context_history.json')

def embed_text(text: str) -> List[float]:
    return MODEL.encode([text])[0]

def load_vector_store() -> Dict[str, List[float]]:
    if os.path.exists(VECTOR_STORE_PATH):
        with open(VECTOR_STORE_PATH, 'rb') as f:
            return pickle.load(f)
    return {}

def save_vector_store(vector_store: Dict[str, List[float]]) -> None:
    with open(VECTOR_STORE_PATH, 'wb') as f:
        pickle.dump(vector_store, f)

def load_config() -> Dict[str, any]:
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    return {'context_path': os.path.expanduser('~/claude_data'), 'roles': {}}

def save_config(config: Dict[str, any]) -> None:
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=2)

def load_context_history() -> List[Dict[str, str]]:
    if os.path.exists(CONTEXT_HISTORY_PATH):
        with open(CONTEXT_HISTORY_PATH, 'r') as f:
            return json.load(f)
    return []

def save_context_history(history: List[Dict[str, str]]) -> None:
    with open(CONTEXT_HISTORY_PATH, 'w') as f:
        json.dump(history, f, indent=2)

def add_file_to_store(filepath: str, vector_store: Dict[str, List[float]]) -> None:
    try:
        with open(filepath, 'r') as file:
            content = file.read()
        vector_store[filepath] = embed_text(content)
        print(f"Indexed: {filepath}")
    except Exception as e:
        print(f"Error indexing {filepath}: {str(e)}")

def retrieve_relevant_context(query: str, vector_store: Dict[str, List[float]], top_k: int = 3) -> List[Tuple[str, str]]:
    if not vector_store:
        print("Error: Vector store is empty. Please run --index first.")
        return []

    query_embedding = embed_text(query)
    similarities = {path: cosine_similarity([query_embedding], [emb])[0][0] for path, emb in vector_store.items()}
    sorted_paths = sorted(similarities.items(), key=lambda x: x[1], reverse=True)

    relevant_documents = []
    for path, similarity in sorted_paths[:top_k]:
        with open(path, 'r') as file:
            content = file.read()
            relevant_documents.append((path, content[:1000]))

    print(f"Retrieved {len(relevant_documents)} relevant documents.")
    return relevant_documents

def chat_with_claude(prompt: str, context_history: List[Dict[str, str]], role: Optional[str] = None,
                     temperature: float = 0.7, max_tokens: Optional[int] = None) -> str:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is not set")

    client = anthropic.Anthropic(api_key=api_key)
    system_prompt = "You are Claude, an AI assistant created by Anthropic to be helpful, harmless, and honest."
    if role:
        system_prompt += f" You are acting as the assistant to a {role}."

    messages = [{"role": "user", "content": prompt}]
    try:
        with client.messages.stream(
                model="claude-3-5-sonnet-20240620",
                max_tokens=max_tokens or 1000,
                temperature=temperature,
                system=system_prompt,
                messages=messages
        ) as stream:
            full_response = ""
            for text in stream.text_stream:
                print(text, end="", flush=True)
                full_response += text
            print()
        return full_response
    except anthropic.APIError as e:
        print(f"An error occurred while communicating with the Claude API: {e}")
        return str(e)

def main() -> None:
    vector_store = load_vector_store()
    config = load_config()
    context_history = load_context_history()

    parser = argparse.ArgumentParser(description="Chat with Claude from the command line.")
    parser.add_argument("prompt", nargs="*", help="The prompt to send to Claude")
    parser.add_argument("--role", help="Set a specific role for Claude")
    parser.add_argument("--temp", type=float, default=0.7, help="Set the temperature for Claude's responses")
    parser.add_argument("--max-tokens", type=int, help="Set the maximum number of tokens for Claude's response")
    parser.add_argument("--set-context-path", help="Set the path for context documents")
    parser.add_argument("--index", action="store_true", help="Index local files before querying")
    parser.add_argument("--clear-index", action="store_true", help="Clear the indexed documents")
    parser.add_argument("--clear-history", action="store_true", help="Clear the conversation history")
    args = parser.parse_args()

    if args.clear_index:
        vector_store.clear()
        save_vector_store(vector_store)
        print("Cleared indexed documents.")
        return

    if args.clear_history:
        context_history.clear()
        save_context_history(context_history)
        print("Cleared conversation history.")
        return

    if args.set_context_path:
        config['context_path'] = os.path.expanduser(args.set_context_path)
        save_config(config)
        print(f"Context path set to: {config['context_path']}")
        return

    if args.index:
        context_path = os.path.expanduser(config['context_path'])
        os.makedirs(context_path, exist_ok=True)
        for filepath in glob.glob(os.path.join(context_path, '*')):
            add_file_to_store(filepath, vector_store)
        save_vector_store(vector_store)
        print(f"Indexed files from: {context_path}")
        return

    prompt = " ".join(args.prompt) if args.prompt else input("Enter your prompt: ")
    relevant_docs = retrieve_relevant_context(prompt, vector_store)
    context = "\n\n".join([f"Content from {path}:\n{content}" for path, content in relevant_docs])
    full_prompt = f"Consider the following context:\n\n{context}\n\nNow, please respond to this query: {prompt}"

    response = chat_with_claude(full_prompt, context_history, args.role, args.temp, args.max_tokens)

    context_history.append({"human": prompt, "assistant": response})
    save_context_history(context_history)

if __name__ == "__main__":
    main()
