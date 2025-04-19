from pydantic import BaseModel, Field

class Email(BaseModel):
    email: str = Field("Detailed email to the customer based on the sentiment")