from fastapi import FastAPI, HTTPException, status
from src.schemas import InboundLeadPayload, LeadIngestionResponse
from src.sheets_service import SheetsService
import uuid
from datetime import datetime

app = FastAPI(
    title="HATO Lead Scout Microservice",
    description="Automated Inbound Lead Qualification & Google Sheets Ingestion API for HATO - The Ring Studio",
    version="1.0.0"
)

sheets_service = SheetsService()

@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    return {"status": "online", "system": "HATO-LeadAgent Engine", "timestamp": datetime.utcnow().isoformat()}

@app.post("/api/v1/leads/ingest", response_model=LeadIngestionResponse, status_code=status.HTTP_201_CREATED)
async def ingest_lead(payload: InboundLeadPayload):
    try:
        generated_id = f"HATO-{uuid.uuid4().hex[:8].upper()}"
        sheets_service.append_lead_to_master(generated_id, payload)
        return LeadIngestionResponse(
            status="Success",
            lead_id=generated_id,
            message=f"Lead for {payload.client_name} successfully ingested into Master_Raw_Leads."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lead ingestion failed: {str(e)}")
