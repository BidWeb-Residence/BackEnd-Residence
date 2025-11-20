from pydantic import BaseModel

class ScanPayload(BaseModel):
    url: str