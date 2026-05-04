import argparse
import openvino_genai
from duckduckgo_search import DDGS

def streamer(subword):
    """Callback function for streaming output."""
    print(subword, end='', flush=True)
    return False  # Return False to continue generation

def search_tool(query):
    """Simple tool using DuckDuckGo to find information."""
    print(f"\n[Tool] Searching for: {query}")
    with DDGS() as ddgs:
        results = [r['body'] for r in ddgs.text(query, max_results=3)]
    return "\n".join(results)

def main():
    parser = argparse.ArgumentParser(description="Simple AI Agent using OpenVINO GenAI")
    parser.add_argument("model_dir", help="Path to the OpenVINO model directory")
    args = parser.parse_args()

    # Initialize the LLM Pipeline
    device = "CPU"  # Can be "GPU" or "NPU"
    pipe = openvino_genai.LLMPipeline(args.model_dir, device)

    config = openvino_genai.GenerationConfig()
    config.max_new_tokens = 512

    print("Welcome to the OpenVINO AI Agent! (Type 'exit' to quit)")

    while True:
        user_input = input("\nUser: ")
        if user_input.lower() in ['exit', 'quit']:
            break

        # Simple logic: If the user asks for a search, use the tool
        if "search for" in user_input.lower() or "find info about" in user_input.lower():
            query = user_input.replace("search for", "").replace("find info about", "").strip()
            search_results = search_tool(query)

            prompt = f"Background information:\n{search_results}\n\nUser Question: {user_input}\n\nAnswer based on the background information:"
        else:
            prompt = user_input

        print("Agent: ", end="")
        pipe.generate(prompt, config, streamer)
        print()

if __name__ == "__main__":
    main()
