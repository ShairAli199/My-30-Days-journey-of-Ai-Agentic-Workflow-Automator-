import os
from langchain_community.utilities import SerpAPIWrapper
from langchain_ollama import OllamaLLM

# 1. Your working key
os.environ["SERPAPI_API_KEY"] = "19fc05e3af014848d7d7cff8dff6dcd84af003c9ece3460869c8a8c370db9a17"

# 2. Setup the Tools and Brain
search = SerpAPIWrapper()
llm = OllamaLLM(model="llama3.2")

def logistics_expert_report(area):
    print(f"🕵️ Agent is investigating fuel prices in {area}...")
    
    # Get the raw data you just saw in the terminal
    raw_search_data = search.run(f"current diesel and petrol price in {area} Pakistan")
    
    # Ask Llama to make it professional
    prompt = f"""
    You are a Logistics Expert for a transport business in Pakistan.
    Below is raw search data about fuel prices:
    {raw_search_data}
    
    Task:
    1. Extract the exact prices for Petrol and Diesel.
    2. Write a 2-sentence advice for a fleet manager on whether to refuel now or wait.
    3. Be professional and use a confident tone.
    """
    
    report = llm.invoke(prompt)
    return report

# --- RUN THE FINAL AGENT ---
if __name__ == "__main__":
    final_report = logistics_expert_report("Sadiqabad")
    print("\n--- 📜 AGENT'S PROFESSIONAL REPORT ---")
    print(final_report)