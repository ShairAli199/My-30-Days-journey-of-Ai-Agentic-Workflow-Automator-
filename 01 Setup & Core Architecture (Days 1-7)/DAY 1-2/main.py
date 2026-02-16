from crewai import Agent, Task, Crew, LLM

# 1. Connect to the Ollama you downloaded
local_brain = LLM(model="ollama/llama3.2", base_url="http://localhost:11434")

# 2. Create your 'Worker' (The Agent)
my_worker = Agent(
  role='Global Tech Mentor',
  goal='Tell a student one cool thing about AI agents.',
  backstory="You are a helpful teacher from the year 2026.",
  llm=local_brain
)

# 3. Give them a 'Task'
my_task = Task(
  description='Write a short, 1-sentence message about the future of AI.',
  expected_output='A motivating sentence.',
  agent=my_worker
)

# 4. Start the work
my_crew = Crew(agents=[my_worker], tasks=[my_task])
print(my_crew.kickoff())