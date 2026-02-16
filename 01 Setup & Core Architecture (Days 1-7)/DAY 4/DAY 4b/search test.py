from serpapi import GoogleSearch

# 1. Paste your key directly here
MY_KEY = "19fc05e3af014848d7d7cff8dff6dcd84af003c9ece3460869c8a8c370db9a17"

def simple_test():
    print("🚀 Sending request to Google...")
    
    params = {
        "engine": "google",
        "q": "current diesel price in Sadiqabad",
        "api_key": MY_KEY
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    if "organic_results" in results:
        print("\n✅ SUCCESS! I found live data:")
        print(results["organic_results"][0]["snippet"])
    else:
        print("❌ Search failed. Check if your key is correct.")

if __name__ == "__main__":
    simple_test()