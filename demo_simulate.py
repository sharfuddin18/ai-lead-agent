import httpx
import json

# Local FastAPI test endpoint
URL = "http://127.0.0.1:8000/api/v1/leads/ingest"

# Sample Mock Lead simulating a prospective client interested in a bespoke solitaire ring
sample_lead = {
    "client_name": "Vikramaditya Rao",
    "contact_number": "+919822113344",
    "lead_source": "Meta Ads - Jayanagar / Indiranagar Campaign",
    "diamond_metal_preference": "3 Carat Round Solitaire, Platinum Band",
    "budget_range": "INR 5 - 7 Lakhs",
    "consultation_type": "In-Studio Visit"
}

def run_demo():
    print("----------------------------------------------------------------")
    print("🚀 HATO LUXURY LEAD AGENT: LIVE DEMO SIMULATION")
    print("----------------------------------------------------------------")
    print(f"-> Sending mock inbound lead for: {sample_lead['client_name']}")
    print(f"-> Preferred Design: {sample_lead['diamond_metal_preference']}")
    print(f"-> Target Budget: {sample_lead['budget_range']}\n")

    try:
        response = httpx.post(URL, json=sample_lead, timeout=10.0)
        if response.status_code == 201:
            data = response.json()
            print("✅ SUCCESS! Lead successfully captured & processed.")
            print(f"   • Assigned Lead ID : {data['lead_id']}")
            print(f"   • System Status    : {data['status']}")
            print(f"   • Pipeline Action  : {data['message']}")
            print(f"   • Timestamp        : {data['timestamp']}")
        else:
            print(f"❌ Error: Server returned status {response.status_code}")
            print(response.text)
    except httpx.ConnectError:
        print("❌ Connection Error: Is your FastAPI server running?")
        print("   Run 'uvicorn src.main:app --reload' in a separate terminal first!")
    print("----------------------------------------------------------------")

if __name__ == "__main__":
    run_demo()
