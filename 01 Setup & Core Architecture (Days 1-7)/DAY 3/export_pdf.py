from fpdf import FPDF

def create_clean_pdf():
    pdf = FPDF()
    pdf.add_page()
    
    # 1. Professional Header
    pdf.set_font("Arial", 'B', 24)
    pdf.set_text_color(44, 62, 80) 
    pdf.cell(200, 30, txt="EXECUTIVE REVENUE REPORT", ln=True, align='C')
    pdf.ln(10)
    
    try:
        # 2. Open the file with 'utf-8' encoding to read everything correctly
        with open('final_report.md', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        pdf.set_font("Arial", size=16)
        for line in lines:
            # THE FIX: This replaces the $ and cleans out "weird" AI characters
            clean_line = line.encode('ascii', 'ignore').decode('ascii')
            clean_line = clean_line.strip().replace('$', 'USD ')
            
            if not clean_line: # Skip empty lines
                continue

            if "PROFIT" in clean_line.upper():
                pdf.set_font("Arial", 'B', 20)
                pdf.set_text_color(39, 174, 96) # Green for Profit
                pdf.cell(0, 20, txt=clean_line, ln=True, align='L')
            else:
                pdf.set_font("Arial", size=16)
                pdf.set_text_color(0, 0, 0)
                pdf.cell(0, 15, txt=clean_line, ln=True, align='L')
        
        pdf.output("Client_Final_Report.pdf")
        print("✅ SUCCESS! Your clean PDF is ready.")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    create_clean_pdf()