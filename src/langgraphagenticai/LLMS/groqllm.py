import os
import streamlit as st
from langchain_groq import ChatGroq


class GroqLLM:

    def __init__(self, user_contols_input):
        self.user_controls_input = user_contols_input

    def get_llm_model(self):

        try:

            # -------------------------------------------------
            # Get Groq API Key
            # -------------------------------------------------

            groq_api_key = self.user_controls_input.get(
                "GROQ_API_KEY",
                ""
            )

            groq_api_key = groq_api_key.strip()

            # -------------------------------------------------
            # Validate API Key
            # -------------------------------------------------

            if not groq_api_key:

                st.error(
                    "❌ Please enter your GROQ API KEY."
                )

                return None

            # -------------------------------------------------
            # Store API key in environment
            # -------------------------------------------------

            os.environ["GROQ_API_KEY"] = groq_api_key

            # -------------------------------------------------
            # Get selected model
            # -------------------------------------------------

            selected_groq_model = self.user_controls_input.get(
                "selected_groq_model"
            )

            if not selected_groq_model:

                st.error(
                    "❌ Please select a Groq model."
                )

                return None

            print(
                "Selected Groq Model:",
                selected_groq_model
            )

            # -------------------------------------------------
            # Create ChatGroq model
            # -------------------------------------------------

            llm = ChatGroq(
                api_key=groq_api_key,
                model=selected_groq_model,
                temperature=0
            )

            return llm

        except Exception as e:

            raise ValueError(
                f"Error Occurred With Exception: {e}"
            )