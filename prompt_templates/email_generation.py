from functools import cached_property
from models.email import Email

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

email_generation_parser = PydanticOutputParser(pydantic_object=Email)
email_generation_prompt = PromptTemplate(
    template="""
        Write a detailed email response for the email field based on these conditions:
        Also remember to write a detailed email response for the email field based on these conditions:
            - email should be addressed to Dear Customer and signed with Service Agent
            - thank them if the review is positive or neutral
            - apologize if the review is negative

        Format Instructions: 
        {format_instructions}

        Sentiment:
        {sentiment}
    """,
    input_variables=["sentiment"],
    partial_variables={"format_instructions": email_generation_parser.get_format_instructions()}
)