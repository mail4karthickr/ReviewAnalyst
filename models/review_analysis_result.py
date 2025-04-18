from pydantic import BaseModel, Field

class ReviewAnalysisResult(BaseModel):
    summary: str = Field(description="Summary of the customer review which should not exceed 3 lines")
    positives: list[str] = Field(description="A list showing the positives mentioned by the customer in the review if any - max 3 points")
    negatives: list[str] = Field(description="A list showing the negatives mentioned by the customer in the review if any - max 3 points")
    sentiment: str = Field(description="One word showing the sentiment of the review - positive, negative or neutral")
    emotions: list = Field(description="A list of 3 - 5 emotions expressed by the customer in the review")