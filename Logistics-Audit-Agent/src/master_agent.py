import os
import time

def audit_logistics_data():
    print("\n--- 🚛 LOGISTICS AI AUDITOR STARTING ---")
    time.sleep(1)
    
    # Mock data representing your father's business records
    records = [
        {"truck_id": "ST-001", "driver": "Ali", "fuel_spent": 50000, "km_covered": 450},
        {"truck_id": "ST-002", "driver": "Hamza", "fuel_spent": 20000, "km_covered": 180},
        {"truck_id": "ST-003", "driver": "Zubair", "fuel_spent": 90000, "km_covered": 300}, # This looks suspicious!
    ]

    print(f"Checking {len(records)} records for financial discrepancies...\n")
    time.sleep(2)

    for record in records:
        # Business Logic: Average fuel cost should be approx 120-150 PKR per KM
        efficiency = record['fuel_spent'] / record['km_covered']
        
        print(f"Checking Truck {record['truck_id']} (Driver: {record['driver']})...")
        
        if efficiency > 200:
            print(f"⚠️  ALERT: High fuel spend detected! ({efficiency:.2f} PKR/KM)")
            print(f"ACTION: Flagging for Debt Recovery audit.\n")
        else:
            print(f"✅ Record looks clean. ({efficiency:.2f} PKR/KM)\n")
        time.sleep(1)

    print("--- AUDIT COMPLETE ---")
    print("Report generated: report_logistics.pdf (Simulated)")

if __name__ == "__main__":
    audit_logistics_data()