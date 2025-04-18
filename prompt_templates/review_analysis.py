from models.review_analysis_result import ReviewAnalysisResult
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

parser = PydanticOutputParser(pydantic_object=ReviewAnalysisResult)
review_analysis_prompt = PromptTemplate(
    template="""
        Analyze the give customer reivew below and generate the response based on the instructions mentioned below in the format instructions.

        Format Instructions: 
        {format_instructions}

        Review:
        {review}
    """,
    input_variables=["review"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)