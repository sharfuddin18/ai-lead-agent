import gspread
from google.oauth2.service_account import Credentials
import os
from datetime import datetime
from src.schemas import InboundLeadPayload

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

class SheetsService:
    def __init__(self):
        self.sheet_id = os.getenv("GOOGLE_SHEET_ID", "")
        self.client = None

    def _authenticate(self):
        creds_dict = {
            "type": "service_account",
            "client_email": os.getenv("GOOGLE_SERVICE_ACCOUNT_EMAIL", ""),
            "private_key": os.getenv("GOOGLE_PRIVATE_KEY", "").replace("\\n", "\n"),
            "token_uri": "https://oauth2.googleapis.com/token"
        }
        credentials = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
        self.client = gspread.authorize(credentials)

    def append_lead_to_master(self, lead_id: str, payload: InboundLeadPayload) -> bool:
        if not self.sheet_id:
            # Fallback for local testing prior to live creds injection
            print(f"[LOCAL TEST LOG] Lead {lead_id} queued for client: {payload.client_name}")
            return True

        if not self.client:
            self._authenticate()

        spreadsheet = self.client.open_by_key(self.sheet_id)
        worksheet = spreadsheet.worksheet("Master_Raw_Leads")

        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        row_data = [
            lead_id,
            timestamp,
            payload.client_name,
            payload.contact_number,
            payload.lead_source,
            f"Pref: {payload.diamond_metal_preference} | Budget: {payload.budget_range} | Type: {payload.consultation_type}",
            "Unassigned",
            "Pending Call",
            "New AI lead captured"
        ]

        worksheet.append_row(row_data)
        return True
