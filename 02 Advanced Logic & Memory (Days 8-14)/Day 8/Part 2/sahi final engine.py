import time
import os
import pandas as pd
from fpdf import FPDF
from concurrent.futures import ProcessPoolExecutor

# Setup folder
if not os.path.exists("Invoices"): os.makedirs("Invoices")

# --- WORKER: Creates individual PDFs and returns data for the Master Ledger ---
def process_and_create_individual_pdf(row_tuple):
    # Using a tuple because ProcessPoolExecutor works better with simple structures
    idx, route, rev, cost = row_tuple
    profit = rev - cost
    
    # Create Individual PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=f"INVOICE ID: {idx}", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(0, 10, txt=f"Route: {route}", ln=True)
    pdf.cell(0, 10, txt=f"Revenue: Rs. {rev:,.2f}", ln=True)
    pdf.cell(0, 10, txt=f"Cost: Rs. {cost:,.2f}", ln=True)
    pdf.cell(0, 10, txt=f"Profit: Rs. {profit:,.2f}", ln=True)
    
    pdf_path = f"Invoices/Invoice_{idx}.pdf"
    pdf.output(pdf_path)
    
    # Return data so we can build the Master Ledger without re-calculating
    return {"ID": idx, "Route": route, "Revenue": rev, "Cost": cost, "Profit": profit}

if __name__ == "__main__":
    # 1. Prepare Data
    data = {
        'ID': range(1, 41),
        'Route': ['Sadiqabad-KHI', 'LHR-KHI'] * 20,
        'Revenue': [150000, 200000] * 20,
        'Cost': [90000, 110000] * 20
    }
    df = pd.DataFrame(data)
    # Convert rows to a list of tuples for the parallel worker
    tasks = [(r['ID'], r['Route'], r['Revenue'], r['Cost']) for _, r in df.iterrows()]

    print("🚀 Running Parallel Engine: Creating 40 Individual PDFs...")
    start = time.time()

    # 2. Parallel Step: Create 40 Individual Files
    with ProcessPoolExecutor(max_workers=4) as executor:
        results_list = list(executor.map(process_and_create_individual_pdf, tasks))

    # 3. Master Ledger Step: Create the Table PDF
    print("📊 Stitching data into Master Business Ledger...")
    master_pdf = FPDF()
    master_pdf.add_page()
    
    # Summary Header
    total_rev = sum(r['Revenue'] for r in results_list)
    total_profit = sum(r['Profit'] for r in results_list)
    
    master_pdf.set_font("Arial", 'B', 16)
    master_pdf.cell(0, 10, "EXECUTIVE MASTER LEDGER", ln=True, align='C')
    master_pdf.set_font("Arial", '', 12)
    master_pdf.cell(0, 10, f"Total Revenue: Rs. {total_rev:,.2f} | Net Profit: Rs. {total_profit:,.2f}", ln=True, align='C')
    master_pdf.ln(5)

    # Table Header
    master_pdf.set_font("Arial", 'B', 10)
    master_pdf.set_fill_color(230, 230, 230)
    master_pdf.cell(20, 10, "ID", 1, 0, 'C', 1)
    master_pdf.cell(60, 10, "Route", 1, 0, 'C', 1)
    master_pdf.cell(35, 10, "Revenue", 1, 0, 'C', 1)
    master_pdf.cell(35, 10, "Cost", 1, 0, 'C', 1)
    master_pdf.cell(35, 10, "Profit", 1, 1, 'C', 1)

    # Table Rows (3 or 4 per page? Let's do 15 to keep it clean but compact)
    master_pdf.set_font("Arial", '', 10)
    for res in results_list:
        master_pdf.cell(20, 10, str(res['ID']), 1)
        master_pdf.cell(60, 10, res['Route'], 1)
        master_pdf.cell(35, 10, f"{res['Revenue']:,.0f}", 1)
        master_pdf.cell(35, 10, f"{res['Cost']:,.0f}", 1)
        master_pdf.cell(35, 10, f"{res['Profit']:,.0f}", 1)
        master_pdf.ln()

    master_pdf.output("Master_Business_Ledger.pdf")

    print(f"✅ DONE in {time.time() - start:.2f}s")
    print("📁 40 PDFs are in the '/Invoices' folder.")
    print("📁 Summary is in 'Master_Business_Ledger.pdf'")