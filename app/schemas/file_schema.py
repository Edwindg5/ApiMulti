from pydantic import BaseModel

class FileResponse(BaseModel):
    file_url: str
