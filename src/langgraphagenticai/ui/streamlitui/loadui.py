import streamlit as st 
import os 
 
from src.langgraphagenticai.ui.uiconfigfile import Config 
 
 
class LoadStreamlitUI: 
 
    def __init__(self): 
        self.config = Config() 
        self.user_controls = {} 
 
    def load_streamlit_ui(self): 
 
        st.set_page_config( 
            page_title="🤖 " + self.config.get_page_title(), 
            layout="wide" 
        ) 
 
        st.header("🤖 " + self.config.get_page_title()) 
 
        # ------------------------------------------------- 
        # Initialize session state only once 
        # ------------------------------------------------- 
 
        if "timeframe" not in st.session_state: 
            st.session_state.timeframe = "" 
 
        if "IsFetchButtonClicked" not in st.session_state: 
            st.session_state.IsFetchButtonClicked = False 
 
        # ------------------------------------------------- 
        # Sidebar 
        # ------------------------------------------------- 
 
        with st.sidebar: 
 
            # Get options from config 
            llm_options = self.config.get_llm_options() 
            usecase_options = self.config.get_usecase_options() 
 
            # ------------------------------------------------- 
            # LLM selection 
            # ------------------------------------------------- 
 
            self.user_controls["selected_llm"] = st.selectbox( 
                "Select LLM", 
                llm_options 
            ) 
 
            # ------------------------------------------------- 
            # Groq 
            # ------------------------------------------------- 
 
            if self.user_controls["selected_llm"] == "Groq": 
 
                model_options = self.config.get_groq_model_options() 
 
                self.user_controls["selected_groq_model"] = st.selectbox( 
                    "Select Model", 
                    model_options 
                ) 
 
                groq_api_key = st.text_input( 
                    "API Key", 
                    value=st.session_state.get("GROQ_API_KEY", ""), 
                    type="password" 
                ) 
 
                self.user_controls["GROQ_API_KEY"] = groq_api_key 
 
                st.session_state["GROQ_API_KEY"] = groq_api_key 
 
                # Validate API key 
                if not groq_api_key: 
                    st.warning( 
                        "⚠️ Please enter your GROQ API key to proceed." 
                    ) 
 
            # ------------------------------------------------- 
            # Usecase selection 
            # ------------------------------------------------- 
 
            self.user_controls["selected_usecase"] = st.selectbox( 
                "Select Usecases", 
                usecase_options 
            ) 
 
            # ------------------------------------------------- 
            # Tavily API key 
            # Required for Chatbot With Web and AI News 
            # ------------------------------------------------- 
 
            if self.user_controls["selected_usecase"] in [ 
                "Chatbot With Web", 
                "AI News" 
            ]: 
 
                tavily_api_key = st.text_input( 
                    "TAVILY API KEY", 
                    value=st.session_state.get("TAVILY_API_KEY", ""), 
                    type="password" 
                ) 
 
                self.user_controls["TAVILY_API_KEY"] = tavily_api_key 
 
                st.session_state["TAVILY_API_KEY"] = tavily_api_key 
 
                # Set environment variable 
                if tavily_api_key: 
                    os.environ["TAVILY_API_KEY"] = tavily_api_key 
 
                # Validate API key 
                if not tavily_api_key: 
                    st.warning( 
                        "⚠️ Please enter your TAVILY API KEY to proceed." 
                    ) 
 
            # ------------------------------------------------- 
            # AI NEWS 
            # ------------------------------------------------- 
 
            if self.user_controls["selected_usecase"] == "AI News": 
 
                st.subheader("📰 AI News Explorer") 
 
                time_frame = st.selectbox( 
                    "📅 Select Time Frame", 
                    ["Daily", "Weekly", "Monthly"], 
                    index=0 
                ) 
 
                # Store selected timeframe 
                self.user_controls["timeframe"] = time_frame 
 
                # ------------------------------------------------- 
                # Fetch News Button 
                # ------------------------------------------------- 
 
                if st.button( 
                    "🔍 Fetch Latest AI News", 
                    use_container_width=True 
                ): 
 
                    st.session_state.IsFetchButtonClicked = True 
 
                    st.session_state.timeframe = time_frame 
 
                    # Store in user controls 
                    self.user_controls["timeframe"] = time_frame 
 
        return self.user_controls  