import pandas as pd
from crewai import Agent, Task, Crew, LLM, Process

# 1. Brain Setup
local_llm = LLM(model="ollama/llama3.2")

def get_data():
    df = pd.read_excel('Client_Inputs/client_data.xlsx', engine='openpyxl')
    return df.to_string()

# 2. THE WORKER: Finds the data
accountant = Agent(
    role="Data Extraction Specialist",
    goal="Provide the Total Revenue, Total Expenses, and Net Profit from the data.",
    backstory="You are a precise data analyst. You only provide facts and numbers.",
    allow_delegation=False, # Worker stays focused on his task
    verbose=True,
    llm=local_llm
)

# 3. THE BOSS: Finalizes the work
qa_manager = Agent(
    role="Final Report Manager",
    goal="Verify the numbers and immediately save the final report.",
    backstory="You are a decisive manager. You do not ask follow-up questions once the numbers are clear.",
    allow_delegation=False, # Stop the back-and-forth loop
    verbose=True,
    llm=local_llm
)

# 4. TASK 1: Extract numbers
analysis_task = Task(
    description=f"Read this data: {get_data()}. Calculate Total Revenue, Total Expenses, and Net Profit.",
    expected_output="A list: Total Revenue, Total Expenses, and Net Profit.",
    agent=accountant
)

# 5. TASK 2: Finalize and Save
# We tell the manager to STOP delegating and just write the file.
verification_task = Task(
    description="""Take the numbers from the Accountant. 
    1. Confirm the math (Revenue - Expenses = Profit).
    2. Write the final report. 
    3. DO NOT ask the accountant any more questions. Finish the job now.""",
    expected_output="Final report with REVENUE, EXPENSES, and PROFIT.",
    agent=qa_manager,
    output_file='final_report.md' 
)

# 6. THE CREW
financial_crew = Crew(
    agents=[accountant, qa_manager],
    tasks=[analysis_task, verification_task],
    process=Process.sequential # CHANGED: Sequential is much faster for local Llama
)

print("### STARTING CLEAN DAY 3 RUN ###")
financial_crew.kickoff()