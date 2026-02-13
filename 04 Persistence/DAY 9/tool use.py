import os
from langchain_ollama import OllamaLLM
from fpdf import FPDF

# 1. THE TOOL (The AI's "Precision Hands")
def calculate_fuel_cost(liters, price):
    # This is pure Python - no version errors possible here!
    total = float(liters) * float(price)
    return f"PKR {total:,.2f}"

# 2. THE PDF PRINTER (Your Professional Output)
def create_pdf_note(query, calculation, ai_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Logistics Financial Audit", ln=True, align='C')
    
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt=f"Subject: {query}", ln=True)
    
    pdf.ln(5)
    pdf.set_text_color(0, 102, 204) # Blue for the verified math
    pdf.cell(200, 10, txt=f"SYSTEM VERIFIED TOTAL: {calculation}", ln=True)
    
    pdf.ln(5)
    pdf.set_text_color(0, 0, 0) # Back to Black
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 10, txt=f"Professional Analysis:\n{ai_text}")
    
    filename = "Financial_Audit_Day9.pdf"
    pdf.output(filename)
    print(f"\n✅ SUCCESS! File generated: {filename}")

# 3. THE BRAIN (Day 9 Tool Logic)
def run_audit():
    llm = OllamaLLM(model="llama3.2")
    
    # Data for the audit
    liters = 6500
    rate = 272.97
    
    print("🚀 Running Precision Math Tool...")
    math_result = calculate_fuel_cost(liters, rate)
    
    print("🧠 Asking AI for Professional Analysis...")
    prompt = f"""
    You are a Financial Auditor. 
    A logistics company just purchased {liters} liters of diesel at {rate} PKR per liter.
    The verified total is {math_result}.
    Write a 3-sentence professional audit summary for the company ledger.
    """
    
    try:
        analysis = llm.invoke(prompt)
        create_pdf_note(f"{liters}L Diesel Purchase", math_result, analysis)
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    run_audit()