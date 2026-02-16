from typing import TypedDict, Annotated, List
import operator
import sqlite3
from langgraph.graph import StateGraph, END, START
from langchain_ollama import OllamaLLM
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.types import Command  # <--- NEW: Used to resume the graph

# 1. SETUP THE BRAIN & MEMORY
llm = OllamaLLM(model="llama3.2")

# Persistence Setup
conn = sqlite3.connect("audit_memory.sqlite", check_same_thread=False)
memory = SqliteSaver(conn)

# 2. DEFINE THE STATE
class AgentState(TypedDict):
    financial_data: str
    audit_report: str
    is_math_correct: bool
    iterations: int 

# --- NODES ---
def auditor_worker(state: AgentState):
    print("\n--- WORKER: AUDITING DATA ---")
    data = state['financial_data']
    prompt = f"Act as a Senior Auditor. Analyze these numbers and find the total deficit: {data}. Be precise."
    response = llm.invoke(prompt)
    return {"audit_report": response, "iterations": state.get('iterations', 0) + 1}

def math_verifier(state: AgentState):
    print("--- WORKER: VERIFYING MATH ---")
    report = state['audit_report']
    prompt = f"Look at this audit report: {report}. Is there a calculation present? Answer with just 'YES' or 'NO'."
    check = llm.invoke(prompt)
    is_correct = "YES" in check.upper()
    return {"is_math_correct": is_correct}

def file_writer_node(state: AgentState):
    print("\n--- WORKER: WRITING REPORT TO DISK ---")
    report = state['audit_report']
    with open("Final_Client_Audit.txt", "w") as f:
        f.write(report)
    print("✅ Success: 'Final_Client_Audit.txt' created!")
    return {}

# --- THE ARCHITECTURE ---
workflow = StateGraph(AgentState)

workflow.add_node("auditor", auditor_worker)
workflow.add_node("verifier", math_verifier)
workflow.add_node("writer", file_writer_node)

workflow.add_edge(START, "auditor")
workflow.add_edge("auditor", "verifier")

def decide_to_end_or_repeat(state: AgentState):
    if state["is_math_correct"] == True or state["iterations"] >= 3:
        return "end"
    else:
        print("!!! MATH FAILED: LOOPING BACK TO AUDITOR !!!")
        return "repeat"

workflow.add_conditional_edges(
    "verifier", 
    decide_to_end_or_repeat,
    {"end": "writer", "repeat": "auditor"}
)

workflow.add_edge("writer", END)

# --- 3. COMPILE WITH INTERRUPT (The Emergency Brake) ---
# We tell the graph: "PAUSE before you enter the writer node"
app = workflow.compile(checkpointer=memory, interrupt_before=["writer"])

# --- 4. THE RUN LOGIC ---
config = {"configurable": {"thread_id": "audit_session_007"}}
raw_numbers = "Revenue: 1000, Tax: 200, Rent: 500, Salary: 400"
inputs = {"financial_data": raw_numbers, "iterations": 0}

print("\n🚀 PHASE 1: AI Analysis & Verification...")

# Run the graph until it hits the interrupt
for output in app.stream(inputs, config=config):
    for key, value in output.items():
        print(f"Node '{key}' has finished.")

# ---------------------------------------------------------
# NEW LINES START HERE: This is where you inspect the math!
# ---------------------------------------------------------
print("\n--- ⏸️ AI IS WAITING FOR YOUR APPROVAL ---")

# We reach into the "Save Game" and grab the current state
current_snapshot = app.get_state(config)
report_to_review = current_snapshot.values.get("audit_report", "No report generated yet.")

print("\n📢 PREVIEW OF THE AUDIT REPORT:")
print("--------------------------------------------------")
print(report_to_review) # This prints the actual math Llama did!
print("--------------------------------------------------")
# ---------------------------------------------------------

user_input = input("\nShould I write the final TXT file? (yes/no): ")

if user_input.lower() == "yes":
    print("\n🚀 PHASE 2: Resuming to Write File...")
    # Passing 'None' tells it to resume from the checkpoint
    for output in app.stream(None, config=config):
        for key, value in output.items():
            print(f"Node '{key}' has finished.")
    print("\n🎯 PROCESS COMPLETE. Check 'Final_Client_Audit.txt'.")
else:
    print("\n🛑 EMERGENCY STOP: Audit rejected. No file was created.")