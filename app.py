from functools import cached_property
import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from prompt_templates.review_analysis import review_analysis_prompt
from models.review_analysis_result import ReviewAnalysisResult
from dotenv import load_dotenv  # Fixed import

# You are building an AI system to be able to look at customer reviews and do some complex analysis. For each review, get ChatGPT to do the following:
#   - Summarize the review. The summary should be at most 3 lines.
#   - Highlight both the positives and negatives.
#   - Display the overall sentiment of the review (positive, negative, neutral).
#   - Display a list of 3 - 5 emotions expressed by the customer in the review.
#   - If the sentiment is positive or neutral, write an email and thank them for the review.
#   - If the sentiment is negative, apologize and write an email with an appropriate response.

class App:

    @cached_property
    def chatgpt(self):
        return ChatOpenAI(
            model_name="gpt-4", 
            temperature=0.0,
            openai_api_key=st.session_state.openai_api_key
        )  # Updated mo

    def analyze_review(self, review):
        try:
            parser = PydanticOutputParser(pydantic_object=ReviewAnalysisResult)
            chain = review_analysis_prompt | self.chatgpt | parser
            result = chain.invoke({"review": review})
            return result
        except Exception as e:
            raise RuntimeError(f"Error in review analysis pipeline: {e}")
        
    def markdown_result(self, result):
        md = f"""
        ### ✨ Review Summary
        {result.summary}

        ### ✅ Positives
        {', '.join(result.positives) if result.positives else 'None'}

        ### ❌ Negatives
        {', '.join(result.negatives) if result.negatives else 'None'}

        ### 📊 Sentiment
        **{result.sentiment.capitalize()}**

        ### 😌 Emotions
        {', '.join(result.emotions) if result.emotions else 'None'}
        """
        return md
    
    def run(self):
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
        else:
            st.title("Customer Review Analyzer")
            review = st.text_area("Paste the customer review here")

            if st.button("Analyze Review"):
                if review.strip():
                    try:
                        result = self.analyze_review(review)
                        st.success("Review analysis completed!")
                        st.markdown(self.markdown_result(result))
                    except Exception as e:
                        st.error(f"Error analyzing review: {e}")
                else:
                    st.warning("Please enter a review before proceeding.")