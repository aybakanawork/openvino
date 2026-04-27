import argparse
import openvino_genai
from duckduckgo_search import DDGS
import json

def streamer(subword):
    print(subword, end='', flush=True)
    return False

class DeepResearchAgent:
    def __init__(self, model_dir, device="CPU"):
        self.pipe = openvino_genai.LLMPipeline(model_dir, device)
        self.config = openvino_genai.GenerationConfig()
        self.config.max_new_tokens = 1024
        self.history = []

    def search(self, query):
        print(f"\n[Deep Research] Investigating: {query}")
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(query, max_results=5)]
        return results

    def run(self, topic):
        print(f"Starting Deep Research on: {topic}")

        # Step 1: Generate Search Queries
        query_prompt = f"Given the topic '{topic}', generate 3 specific search queries to gather comprehensive information. Return only a JSON list of strings."
        queries_raw = self.pipe.generate(query_prompt, self.config)

        # In a real agent, we'd parse JSON. Here we simulate for the sample.
        queries = [f"{topic} latest news", f"{topic} overview", f"{topic} future trends"]

        collected_info = []
        for q in queries:
            results = self.search(q)
            collected_info.append({"query": q, "results": results})

        # Step 2: Synthesize Report
        synthesis_prompt = f"Synthesize a detailed research report on '{topic}' based on the following findings:\n{json.dumps(collected_info)}\n\nReport:"

        print("\n--- Final Research Report ---\n")
        self.pipe.generate(synthesis_prompt, self.config, streamer)
        print("\n----------------------------\n")

def main():
    parser = argparse.ArgumentParser(description="Deep Research AI Agent using OpenVINO")
    parser.add_argument("model_dir", help="Path to the OpenVINO model directory")
    args = parser.parse_args()

    agent = DeepResearchAgent(args.model_dir)
    topic = input("Enter a topic for deep research: ")
    agent.run(topic)

if __name__ == "__main__":
    main()
