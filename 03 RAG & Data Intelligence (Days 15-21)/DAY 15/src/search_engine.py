import faiss
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from fpdf import FPDF
import os

# --- 1. Load the Brain ---
print("Loading AI Model... please wait.")
model = SentenceTransformer('all-MiniLM-L6-v2')

class FinancialAuditor:
    def __init__(self):
        self.logs = []
        self.index = None

    def grab_data(self, folder_path):
        """Read Excel/CSV and keep the Column Names"""
        print(f"--- Checking for data in '{folder_path}' ---")
        
        # specific check to help you debug
        if not os.path.exists(folder_path):
            print(f"ERROR: The folder '{folder_path}' does not exist!")
            print("Please create a folder named 'Data' and put your file inside.")
            return

        files_found = 0
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            
            if file.endswith(('.csv', '.xlsx')):
                files_found += 1
                print(f"   > Reading file: {file}")
                # Read file
                df = pd.read_csv(file_path) if file.endswith('.csv') else pd.read_excel(file_path)
                
                # Turn each row into a labeled sentence: "Date: 6/4/2024 | Amount: $500"
                for _, row in df.iterrows():
                    # Clean up the row data
                    entry_parts = []
                    for col in df.columns:
                        # minimal cleanup to remove empty values
                        val = str(row[col])
                        if val and val.lower() != 'nan':
                            entry_parts.append(f"{col}: {val}")
                    
                    self.logs.append(" | ".join(entry_parts))

        if self.logs:
            print(f"   > Vectorizing {len(self.logs)} rows... (This makes them searchable)")
            embeddings = model.encode(self.logs)
            self.index = faiss.IndexFlatL2(embeddings.shape[1])
            self.index.add(np.array(embeddings).astype('float32'))
            print("--- Data Successfully Indexed ---")
        else:
            print(f"WARNING: No CSV or Excel files found in '{folder_path}'.")

    def find_leaks(self, query):
        if not self.index: return []
        query_vector = model.encode([query]).astype('float32')
        D, I = self.index.search(query_vector, 3) # Find top 3 matches
        return [self.logs[idx] for idx in I[0]]

    def generate_pdf_report(self, query, results, filename="Audit_Evidence.pdf"):
        """Creates the 'Owner Friendly' Report in Plain English"""
        pdf = FPDF()
        pdf.add_page()
        
        # --- Header ---
        pdf.set_fill_color(44, 62, 80) # Navy Blue
        pdf.rect(0, 0, 210, 40, 'F')
        pdf.set_font("Arial", 'B', 22)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(0, 20, txt="LOGISTICS FINANCIAL AUDIT", ln=True, align='C')
        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 5, txt="Business Owner's Summary", ln=True, align='C')
        pdf.ln(20)

        pdf.set_text_color(0, 0, 0)
        
        # --- Loop through findings ---
        for i, res in enumerate(results):
            # Parse the text back into a dictionary
            # Example: "SCAC: CRST | Price: 100" -> {'SCAC': 'CRST', 'Price': '100'}
            data = {}
            parts = res.split(" | ")
            for p in parts:
                if ": " in p:
                    key, val = p.split(": ", 1)
                    data[key.strip()] = val.strip()

            # 1. The Red Flag Title
            pdf.set_font("Arial", 'B', 14)
            pdf.set_text_color(200, 0, 0) # Red
            pdf.cell(0, 10, txt=f"ISSUE #{i+1}: POTENTIAL FINANCIAL LEAK", ln=True)
            
            # 2. The Simple English Story
            pdf.set_font("Arial", '', 12)
            pdf.set_text_color(0, 0, 0)
            
            # Safe variables (in case columns are named differently)
            date = data.get('Ship Date', data.get('Date', 'Unknown Date'))
            amt = data.get('FreightPaid', data.get('Amount', '$0'))
            carrier = data.get('SCAC', data.get('Carrier', 'Unknown Carrier'))
            dest = data.get('Dest City', data.get('Destination', 'Unknown City'))
            miles = data.get('Miles', '0')
            
            # Calculate cost per mile if possible
            cost_note = ""
            try:
                # remove '$' and ',' to do math
                clean_amt = float(str(amt).replace('$','').replace(',',''))
                clean_miles = float(str(miles).replace(',',''))
                if clean_miles > 0:
                    cpm = clean_amt / clean_miles
                    cost_note = f"This comes out to ${cpm:.2f} per mile."
            except:
                pass # If math fails, just skip that sentence
            
            summary = (
                f"On {date}, a payment of {amt} was recorded for carrier '{carrier}' "
                f"for a trip to {dest}. The recorded distance was {miles} miles. "
                f"{cost_note} Please verify if this rate is accurate."
            )
            
            pdf.multi_cell(0, 8, txt=summary)
            pdf.ln(5)
            
            # 3. The Raw Data Box (Grey)
            pdf.set_fill_color(240, 240, 240)
            pdf.set_font("Courier", '', 9) # Typewriter font for raw data
            raw_text = "RAW DATA: " + res
            pdf.multi_cell(0, 5, txt=raw_text, border=1, fill=True)
            
            pdf.ln(10) # Space between items
            
        pdf.output(filename)
        print(f"--- SUCCESS: Report saved as {filename} ---")

# --- EXECUTION BLOCK (DO NOT DELETE) ---
if __name__ == "__main__":
    # 1. Start the Auditor
    auditor = FinancialAuditor()
    
    # 2. Grab the Data
    # Make sure your folder is named 'Data' (Case sensitive on Linux/Mac, usually fine on Windows)
    auditor.grab_data("Data") 
    
    # 3. Run the Search
    if auditor.logs:
        target = "Find missing invoices, fuel theft, or unpaid trips"
        print(f"   > Searching for: {target}")
        found_data = auditor.find_leaks(target)
        
        # 4. Generate the PDF
        auditor.generate_pdf_report(target, found_data)
    else:
        print("System stopped: No data found to analyze.")