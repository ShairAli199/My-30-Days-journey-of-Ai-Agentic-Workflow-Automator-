from typing import TypedDict, Annotated, List
import operator
from langgraph.graph import StateGraph, END, START
from langchain_ollama import OllamaLLM

# This is our 'Discrete Structure' State (The Notebook)
class AgentState(TypedDict):
    financial_data: str
    audit_report: str
    is_math_correct: bool
    iterations: int  # To make sure we don't loop forever!
    
llm = OllamaLLM(model="llama3.2")


def auditor_worker(state: AgentState):
    print("--- WORKER: AUDITING DATA ---")
    data = state['financial_data']
    prompt = f"Act as a Senior Auditor. Analyze these numbers and find the total deficit: {data}. Be precise."
    response = llm.invoke(prompt)
    # We update the 'Notebook' with the report
    return {"audit_report": response, "iterations": state.get('iterations', 0) + 1}

def math_verifier(state: AgentState):
    print("--- WORKER: VERIFYING MATH ---")
    report = state['audit_report']
    # We ask a second 'internal' logic if the math looks solid
    prompt = f"Look at this audit report: {report}. Is there a calculation present? Answer with just 'YES' or 'NO'."
    check = llm.invoke(prompt)
    
    # Logic to decide the path
    is_correct = "YES" in check.upper()
    return {"is_math_correct": is_correct}
def file_writer_node(state: AgentState):
    print("\n--- WORKER: WRITING REPORT TO DISK ---")
    report = state['audit_report']
    
    # This creates a real file in your folder
    with open("Final_Client_Audit.txt", "w") as f:
        f.write(report)
        
    print("✅ Success: 'Final_Client_Audit.txt' created!")
    return {} # No changes needed to the notebook
# --- SECTION 4: THE ARCHITECTURE (Connecting the Dots) ---
workflow = StateGraph(AgentState)

# 1. Add our Nodes (Station 1, 2, and now 3!)
workflow.add_node("auditor", auditor_worker)
workflow.add_node("verifier", math_verifier)
workflow.add_node("writer", file_writer_node) # <--- ADDED THIS

# 2. Add our Edges (The basic paths)
workflow.add_edge(START, "auditor")
workflow.add_edge("auditor", "verifier")

# 3. The 'Smart Loop' & The New Path to the Writer
def decide_to_end_or_repeat(state: AgentState):
    if state["is_math_correct"] == True or state["iterations"] >= 3:
        return "end" # This 'end' string now maps to the 'writer' below
    else:
        print("!!! MATH FAILED: LOOPING BACK TO AUDITOR !!!")
        return "repeat"

workflow.add_conditional_edges(
    "verifier", 
    decide_to_end_or_repeat,
    {
        "end": "writer",   # <--- UPDATED: Instead of END, go to the writer
        "repeat": "auditor" 
    }
)

# 4. Final Connection
workflow.add_edge("writer", END) # <--- ADDED THIS: From writer to finish

# 5. Compile the Factory
app = workflow.compile()
# --- SECTION 5: THE RUN ---
print("\n🚀 STARTING BEAST MODE PRODUCTION LINE...")
raw_numbers = "Revenue: 1000, Tax: 200, Rent: 500, Salary: 400"
inputs = {"financial_data": raw_numbers, "iterations": 0}

for output in app.stream(inputs):
    for key, value in output.items():
        print(f"\nNode '{key}' has finished.")
    print("---------------------------------")

print("\n🎯 PROCESS COMPLETE. Check your folder for 'Final_Client_Audit.txt'!")