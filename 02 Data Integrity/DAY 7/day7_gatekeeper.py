import pandas as pd
import re
from pydantic import BaseModel, field_validator
from fpdf import FPDF

# 1. THE DATA AUDITOR (The "Gatekeeper")
class SahiAudit(BaseModel):
    route: str
    price: float
    fuel: float
    maintenance: float

    # This 'Surgeon' logic cleans ANY messy money column automatically
    @field_validator('price', 'fuel', 'maintenance', mode='before')
    def clean_money_fields(cls, v):
        # Handle 'k', commas, and lowercase the input
        val = str(v).lower().replace('k', '000')
        # Regex: Remove everything EXCEPT numbers and dots
        val = re.sub(r'[^\d.]', '', val)
        return float(val) if val else 0.0

# 2. THE PDF DESIGNER (The "Presentation Layer")
class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.set_text_color(44, 62, 80) # Dark Blue/Grey
        self.cell(0, 10, 'SAHI LOGISTICS - FINANCIAL AUDIT REPORT', 0, 1, 'C')
        self.ln(10)

# 3. THE EXECUTION ENGINE
try:
    # A. Load the Messy Excel
    df = pd.read_excel('transport_data.xlsx', engine='openpyxl')
    
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_font("Arial", size=10)

    # Prepare list for the "Clean Spreadsheet" output
    clean_data_for_excel = []

    # PDF Table Headers (Professional Blue Design)
    pdf.set_fill_color(52, 152, 219) # Business Blue
    pdf.set_text_color(255, 255, 255) # White text
    headers = ["Route", "Revenue", "Fuel", "Maint.", "Net Profit"]
    widths = [55, 32, 32, 32, 32]
    
    for i in range(len(headers)):
        pdf.cell(widths[i], 12, headers[i], 1, 0, 'C', True)
    pdf.ln()

    # Reset colors for table data
    pdf.set_text_color(0, 0, 0)

    print("--- 🚀 STARTING LOGISTICS TRANSFORMATION ---")

    for index, row in df.iterrows():
        try:
            # Step 1: Clean and Validate using Pydantic + Regex
            record = SahiAudit(
                route=row['Route'], 
                price=row['Price'], 
                fuel=row['Fuel'], 
                maintenance=row['Maintenance']
            )
            
            # Step 2: Professional Calculation
            net_profit = record.price - (record.fuel + record.maintenance)

            # Step 3: Add to PDF Table
            pdf.cell(widths[0], 10, record.route, 1)
            pdf.cell(widths[1], 10, f"{record.price:,.0f}", 1)
            pdf.cell(widths[2], 10, f"{record.fuel:,.0f}", 1)
            pdf.cell(widths[3], 10, f"{record.maintenance:,.0f}", 1)
            
            # Profit Color Coding: Green for Profit, Red for Loss
            if net_profit > 0:
                pdf.set_text_color(46, 204, 113) # Emerald Green
            else:
                pdf.set_text_color(231, 76, 60) # Alizarin Red
                
            pdf.cell(widths[4], 10, f"{net_profit:,.0f}", 1)
            pdf.set_text_color(0, 0, 0) # Reset to black
            pdf.ln()

            # Step 4: Add to the Clean Data List
            clean_data_for_excel.append({
                "Route": record.route,
                "Revenue_PKR": record.price,
                "Fuel_Cost": record.fuel,
                "Maintenance_Cost": record.maintenance,
                "Net_Profit": net_profit
            })
            
            print(f"✅ Row {index+1} Processed Successfully")

        except Exception as e:
            print(f"❌ Error in Row {index+1}: {e}")

    # --- FINAL OUTPUT: SAVE BOTH ASSETS ---
    
    # 1. Save the Professional PDF
    pdf.output("Sahi_Logistics_Final_Audit.pdf")
    
    # 2. Save the Clean Excel Sheet
    clean_df = pd.DataFrame(clean_data_for_excel)
    clean_df.to_excel("Cleaned_Transport_Data.xlsx", index=False)

    print("\n" + "="*40)
    print("DONE! Day 7 Mission Successful.")
    print("1. PDF REPORT: 'Sahi_Logistics_Final_Audit.pdf'")
    print("2. CLEAN SHEET: 'Cleaned_Transport_Data.xlsx'")
    print("="*40)

except Exception as e:
    print(f"CRITICAL ERROR: {e}. Check if 'transport_data.xlsx' exists and is closed.")