from pydantic import BaseModel, Field

class EmailResult(BaseModel):
    email: str = Field("")