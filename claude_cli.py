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
from typing import Union, Dict, List, Tuple, Optional

# Set the environment variable to disable the tokenizers parallelism warning
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Constants for file paths
MODEL = SentenceTransformer('all-MiniLM-L6-v2')
CONFIG_PATH = os.path.expanduser('~/scripts/.claude_cli_config.json')
VECTOR_STORE_PATH = os.path.expanduser('~/scripts/.claude_vector_store.pkl')
CONTEXT_HISTORY_PATH = os.path.expanduser('~/scripts/.claude_context_history.json')
WORK_CONTEXT_FILE = os.path.expanduser('~/scripts/.work_context.md')
SAVED_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'saved')

def load_work_context() -> str:
    if os.path.exists(WORK_CONTEXT_FILE):
        with open(WORK_CONTEXT_FILE, 'r') as f:
            return f.read()
    return ""

WORK_CONTEXT = load_work_context()

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
    return {'context_path': os.path.expanduser('~/scripts/claude_data')}

def save_config(config: Dict[str, any]) -> None:
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=2)

def load_context_history() -> List[Dict[str, str]]:
    if os.path.exists(CONTEXT_HISTORY_PATH):
        try:
            with open(CONTEXT_HISTORY_PATH, 'r') as f:
                content = f.read()
                print(f"Loaded context history file with {len(content)} characters.")
                history = json.loads(content)
                return [
                    {'human': entry['human'], 'assistant': entry['assistant']}
                    for entry in history
                    if isinstance(entry, dict) and 'human' in entry and 'assistant' in entry
                ]
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in context history file: {e}")
            print(f"Error occurred at line {e.lineno}, column {e.colno}")
            print(f"The problematic part of the JSON: {e.doc[max(0, e.pos-20):e.pos+20]}")
            print("Returning empty context history due to error.")
            return []
        except Exception as e:
            print(f"Unexpected error while loading context history: {e}")
            return []
    return []

def save_context_history(history: List[Dict[str, str]]) -> None:
    with open(CONTEXT_HISTORY_PATH, 'w') as f:
        json.dump(history, f, indent=2)

def clean_context_history(context_history: List[Union[Dict[str, str], List[str]]]) -> List[Dict[str, str]]:
    cleaned_history = []
    for entry in context_history:
        if isinstance(entry, dict):
            human = entry.get("human", "")
            assistant = entry.get("assistant", "")
            if isinstance(human, str) and isinstance(assistant, str) and human.strip() and assistant.strip():
                cleaned_history.append({"human": human, "assistant": assistant})
        elif isinstance(entry, list) and len(entry) == 2:
            human, assistant = entry
            if isinstance(human, str) and isinstance(assistant, str) and human.strip() and assistant.strip():
                cleaned_history.append({"human": human, "assistant": assistant})
    return cleaned_history

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

def chat_with_claude(prompt: str, context_history: List[Dict[str, str]], temperature: float = 0.7, max_tokens: Optional[int] = None, stream: bool = True) -> str:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is not set")

    client = anthropic.Anthropic(api_key=api_key)
    system_prompt = f"""You are Claude, an AI assistant created by Anthropic to be helpful, harmless, and honest. You are assisting a Full-Stack Engineer working at Workhelix.
{WORK_CONTEXT}
Always format your responses in markdown. Be concise unless asked to elaborate."""

    messages = []
    for entry in context_history[-5:]:  # Only use the last 5 entries to keep context relevant
        messages.append({"role": "user", "content": entry["human"]})
        messages.append({"role": "assistant", "content": entry["assistant"]})

    messages.append({"role": "user", "content": prompt})

    print("Sending request to Claude API...")
    try:
        if stream:
            print("Streaming response:")
            response = ""
            with client.messages.stream(
                model="claude-3-5-sonnet-20240620",
                max_tokens=max_tokens or 1000,
                temperature=temperature,
                system=system_prompt,
                messages=messages
            ) as stream_response:
                for text in stream_response.text_stream:
                    print(text, end="", flush=True)
                    response += text
                print()  # Print a newline after the stream ends
        else:
            print("Fetching response:")
            response_obj = client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=max_tokens or 1000,
                temperature=temperature,
                system=system_prompt,
                messages=messages
            )
            response = response_obj.content
            print(response)
        
        print("\nResponse received and printed.")
        return response
    except anthropic.APIError as e:
        print(f"An error occurred while communicating with the Claude API: {e}")
        return str(e)

def save_last_interaction(response: str, filename: Optional[str] = None) -> None:
    if filename is None:
        filename = os.path.join(SAVED_FOLDER, 'claude_last_interaction.json')
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as f:
        json.dump({"response": response}, f, indent=2)

def save_response(response: str, filename: Optional[str] = None) -> None:
    if filename is None:
        filename = os.path.join(SAVED_FOLDER, f"claude_save_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md")
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as f:
        f.write(response)
    print(f"Response saved to {filename}")

def main() -> None:
    vector_store = load_vector_store()
    config = load_config()
    context_history = load_context_history()

    parser = argparse.ArgumentParser(description="Chat with Claude from the command line.")
    parser.add_argument("prompt", nargs="*", help="The prompt to send to Claude")
    parser.add_argument("--temp", type=float, default=0.7, help="Set the temperature for Claude's responses")
    parser.add_argument("--max-tokens", type=int, help="Set the maximum number of tokens for Claude's response")
    parser.add_argument("--set-context-path", help="Set the path for context documents")
    parser.add_argument("--index", action="store_true", help="Index local files before querying")
    parser.add_argument("--clear-index", action="store_true", help="Clear the indexed documents")
    parser.add_argument("--clear-history", action="store_true", help="Clear the conversation history")
    parser.add_argument("--save", nargs='?', const=True, help="Save the response to a markdown file")
    parser.add_argument("--save-last", action="store_true", help="Save the last interaction to a file")
    parser.add_argument("--stream", action="store_true", help="Stream Claude's response in real-time")
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

    if args.save_last:
        last_interaction = context_history[-1]["assistant"] if context_history else "No interactions found."
        save_last_interaction(last_interaction)
        print("Saved last interaction.")
        return

    print("Chat with Claude (type 'exit' to end the conversation)")
    print("=" * 40)

    while True:
        prompt = " ".join(args.prompt) if args.prompt else input("\nYou: ")
        if prompt.lower() == 'exit':
            print("Ending conversation. Goodbye!")
            break

        relevant_docs = retrieve_relevant_context(prompt, vector_store)
        context = "\n\n".join([f"Content from {path}:\n{content}" for path, content in relevant_docs])
        full_prompt = f"Consider the following context:\n\n{context}\n\nNow, please respond to this query: {prompt}"

        try:
            response = chat_with_claude(full_prompt, context_history, args.temp, args.max_tokens, args.stream)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            response = str(e)

        # Handle different types of responses
        if isinstance(response, list):
            response = "\n".join([r.text if hasattr(r, 'text') else str(r) for r in response])
        elif hasattr(response, 'text'):
            response = response.text

        print("\nClaude:")
        print("-" * 40)
        print(response.strip())
        print("-" * 40)

        context_history.append({"human": prompt, "assistant": response})
        context_history = context_history[-10:]  # Keep only the last 10 interactions
        save_context_history(context_history)

        if args.save:
            save_response(response, args.save if isinstance(args.save, str) else None)

        args.prompt = None  # Clear prompt for next iteration

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nConversation interrupted. Goodbye!")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()
