from langchain_ollama import OllamaLLM
from langchain_community.utilities import SerpAPIWrapper
from fpdf import FPDF
import os

# 1. Setup
os.environ["SERPAPI_API_KEY"] = "19fc05e3af014848d7d7cff8dff6dcd84af003c9ece3460869c8a8c370db9a17"
llm = OllamaLLM(model="llama3.2")
search_tool = SerpAPIWrapper()

# 2. THE PDF MAKER
def save_to_pdf(agent_name, query, report_text):
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=f"{agent_name} Professional Report", ln=True, align='C')
    
    # Query
    pdf.set_font("Arial", 'B', 12)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Subject: {query}", ln=True)
    
    # Body
    pdf.set_font("Arial", size=11)
    pdf.ln(5)
    # Multi_cell handles long text and wrapping
    pdf.multi_cell(0, 10, txt=report_text)
    
    filename = f"{agent_name}_Report.pdf"
    pdf.output(filename)
    print(f"✅ PDF Saved successfully as: {filename}")

# 3. THE UPDATED FACTORY
def create_agent(name, role_description, can_search=False):
    def run_agent(user_query):
        context = ""
        if can_search:
            context = f"\nLive Data Found: {search_tool.run(user_query)}"
        
        prompt = f"Role: {role_description}\nContext: {context}\nUser Query: {user_query}\nProvide a detailed report."
        response = llm.invoke(prompt)
        
        # Automatically save to PDF
        save_to_pdf(name, user_query, response)
        return response
    
    return run_agent

# --- EXECUTION ---
if __name__ == "__main__":
    fuel_expert = create_agent("Logistics_Manager", "Expert in Pakistan fuel markets", can_search=True)
    
    print("🚀 Generating your professional PDF...")
    fuel_expert("Current diesel prices in Sadiqabad and Multan")