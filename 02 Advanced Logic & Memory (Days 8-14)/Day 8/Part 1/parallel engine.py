import time
import pandas as pd
from concurrent.futures import ProcessPoolExecutor

def auditor_worker(chunk):
    results = []
    for index, row in chunk.iterrows():
        try:
            time.sleep(0.2) # Your 0.2s benchmark
            # Return a DICTIONARY, not a string
            results.append({
                "id": index, 
                "route": row['Route'], 
                "status": "PASS",
                "timestamp": time.ctime()
            })
        except Exception as e:
            results.append({"id": index, "status": "FAIL", "error": str(e)})
    return results

if __name__ == "__main__":
    # Create messy data
    df = pd.DataFrame({'Route': ['Sadiqabad-KHI', 'LHR-Sadiqabad'] * 20})
    
    print("🚀 Running Structured Parallel Audit...")
    start = time.time()

    # Parallel processing
    with ProcessPoolExecutor(max_workers=4) as executor:
        chunks = [df[i:i + 10] for i in range(0, 40, 10)]
        raw_output = list(executor.map(auditor_worker, chunks))

    # 1. Flatten the list of lists
    flat_results = [item for sublist in raw_output for item in sublist]

    # 2. Convert to DataFrame (This makes sorting and saving EASY)
    results_df = pd.DataFrame(flat_results)

    # 3. FORCE THE SORT (The "Senior" safety move)
    # Even if workers finished out of order, this fixes it.
    results_df = results_df.sort_values(by="id")

    # 4. Save to CSV
    results_df.to_csv("Sahi_Structured_Audit.csv", index=False)

    print(f"✅ DONE in {time.time() - start:.2f}s")