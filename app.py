import os
import streamlit as st

from functools import cached_property
from models.email import Email
from dotenv import load_dotenv

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI

from prompt_templates.review_analysis import review_analysis_prompt, review_analysis_parser
from prompt_templates.email_generation import email_generation_prompt, email_generation_parser
from models.review_analysis_result import ReviewAnalysisResult

class App:
    def __init__(self):
        load_dotenv()

    @cached_property
    def chatgpt(self):
        return ChatOpenAI(
            model_name="gpt-4", 
            temperature=0.0,
            openai_api_key=st.session_state.openai_api_key
        )  # Updated mo

    def analyze_review(self, review: str) -> ReviewAnalysisResult:
        try:
            chain = review_analysis_prompt | self.chatgpt | review_analysis_parser
            result = chain.invoke({"review": review})
            return result
        except Exception as e:
            raise RuntimeError(f"Error in review analysis pipeline: {e}")
        
    def email_generator(self, sentiment: str) -> Email:
        try:
            chain = email_generation_prompt | self.chatgpt | email_generation_parser
            result = chain.invoke({"sentiment": sentiment})
            return result
        except Exception as e:
            raise RuntimeError(f"Error in review analysis pipeline: {e}")
        
    def render_result(self, review_analysis: ReviewAnalysisResult, email: str):
        md = f"""
        ### ✨ Review Summary
        {review_analysis.summary}

        ### ✅ Positives
        {', '.join(review_analysis.positives) if review_analysis.positives else 'None'}

        ### ❌ Negatives
        {', '.join(review_analysis.negatives) if review_analysis.negatives else 'None'}

        ### 📊 Sentiment
        **{review_analysis.sentiment.capitalize()}**

        ### 😌 Emotions
        {', '.join(review_analysis.emotions) if review_analysis.emotions else 'None'}

        ### \U0001F4E7 Email
        {email}
        """
        return md

    def setup_api_key(self) -> bool:
        # Try loading from .env first
        env_key = os.getenv("OPENAI_API_KEY")
        if env_key and "openai_api_key" not in st.session_state:
            st.session_state.openai_api_key = env_key
            return True
        
        # Ask user to input manually
        if "openai_api_key" not in st.session_state:
            if "openai_api_key" not in st.session_state:
                st.title("🔐 Enter OpenAI API Key to Start")
                openai_api_key_input = st.text_input("Enter your OpenAI API Key", type="password")

                if st.button("Submit"):
                    if openai_api_key_input.strip():
                        st.session_state.openai_api_key = openai_api_key_input.strip()
                        st.success("API Key stored! You can now use the app.")
                        st.rerun()
                    else:
                        st.warning("Please enter a valid key")

        return "openai_api_key" in st.session_state
    
    def run(self):
        if not self.setup_api_key():
            return
        
        st.title("Customer Review Analyzer")
        review = st.text_area("Paste the customer review here")

        if st.button("Analyze Review"):
            if review.strip():
                try:
                    review_analysis_result = self.analyze_review(review)
                    email_result = self.email_generator(review_analysis_result.sentiment)
                    st.markdown(self.render_result(review_analysis_result, email_result.email))
                except Exception as e:
                    st.error(f"Error analyzing review: {e}")
            else:
                st.warning("Please enter a review before proceeding.")