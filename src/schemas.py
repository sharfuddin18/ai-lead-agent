from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime

class InboundLeadPayload(BaseModel):
    client_name: str = Field(..., min_length=2, description="Full name of the client")
    contact_number: str = Field(..., pattern=r"^\+?[1-9]\d{1,14}$", description="E.164 formatted contact number")
    lead_source: str = Field(default="Meta Ads / Web Inbound", description="Source acquisition channel")
    diamond_metal_preference: Optional[str] = Field(default="Not Specified", description="Cut, carat, or metal preference")
    budget_range: Optional[str] = Field(default="Consultation Required", description="Target budget scale")
    consultation_type: Literal["In-Studio Visit", "Virtual Consultation", "Pending Decision"] = "Pending Decision"

class LeadIngestionResponse(BaseModel):
    status: str
    lead_id: str
    message: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
