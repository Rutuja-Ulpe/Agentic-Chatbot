import streamlit as st 
 
from src.langgraphagenticai.ui.streamlitui.loadui import LoadStreamlitUI 
from src.langgraphagenticai.LLMS.groqllm import GroqLLM 
from src.langgraphagenticai.graph.graph_builder import GraphBuilder 
from src.langgraphagenticai.ui.streamlitui.display_result import DisplayResultStreamlit 
 
 
def load_langgraph_agenticai_app(): 
    """ 
    Main entry point for the LangGraph Agentic AI application. 
    """ 
 
    # ===================================================== 
    # 1. LOAD UI 
    # ===================================================== 
 
    ui = LoadStreamlitUI() 
    user_input = ui.load_streamlit_ui() 
 
    if not user_input: 
        st.error("❌ Failed to load user input from UI.") 
        return 
 
    # ===================================================== 
    # 2. GET SELECTED USECASE 
    # ===================================================== 
 
    usecase = user_input.get("selected_usecase") 
 
    if not usecase: 
        st.error("❌ No use case selected.") 
        return 
 
    print("----------------------------------------") 
    print("Selected Usecase:", usecase) 
    print("----------------------------------------") 
 
    # ===================================================== 
    # 3. INITIALIZE USER MESSAGE 
    # ===================================================== 
 
    user_message = None 
 
    # ===================================================== 
    # 4. AI NEWS 
    # ===================================================== 
 
    if usecase == "AI News": 
 
        fetch_clicked = st.session_state.get( 
            "IsFetchButtonClicked", 
            False 
        ) 
 
        # ------------------------------------------------- 
        # Option 1: Fetch button 
        # ------------------------------------------------- 
 
        if fetch_clicked: 
 
            user_message = st.session_state.get( 
                "timeframe", 
                "" 
            ) 
 
            if not user_message: 
 
                st.warning( 
                    "⚠️ Please select a time frame." 
                ) 
 
                return 
 
        # ------------------------------------------------- 
        # Option 2: Natural language query 
        # ------------------------------------------------- 
 
        else: 
 
            user_message = st.chat_input( 
                "Enter AI News query..." 
            ) 
 
            if not user_message: 
                return 
 
    # ===================================================== 
    # 5. BASIC CHATBOT 
    #    CHATBOT WITH WEB 
    # ===================================================== 
 
    else: 
 
        # AI News button state reset 
        st.session_state.IsFetchButtonClicked = False 
 
        # Get normal chat input 
        user_message = st.chat_input( 
            "Enter your message:" 
        ) 
 
        # IMPORTANT: 
        # Do not continue until user enters a message 
        if not user_message: 
            return 
 
    # ===================================================== 
    # 6. VALIDATE USER MESSAGE 
    # ===================================================== 
 
    if user_message is None: 
        return 
 
    user_message = str(user_message).strip() 
 
    if not user_message: 
        return 
 
    print("----------------------------------------") 
    print("Usecase:", usecase) 
    print("User Message:", user_message) 
    print("----------------------------------------") 
 
    # ===================================================== 
    # 7. INITIALIZE GROQ LLM 
    # ===================================================== 
 
    try: 
 
        obj_llm_config = GroqLLM( 
            user_contols_input=user_input 
        ) 
 
        model = obj_llm_config.get_llm_model() 
 
        if model is None: 
 
            st.error( 
                "❌ Error: LLM model could not be initialized." 
            ) 
 
            return 
 
    except Exception as e: 
 
        st.error( 
            f"❌ LLM initialization failed: {str(e)}" 
        ) 
 
        print( 
            "LLM Initialization Error:", 
            e 
        ) 
 
        return 
 
    # ===================================================== 
    # 8. BUILD GRAPH 
    # ===================================================== 
 
    try: 
 
        graph_builder = GraphBuilder(model) 
 
        graph = graph_builder.setup_graph( 
            usecase 
        ) 
 
        print( 
            "✅ Graph created successfully." 
        ) 
 
    except Exception as e: 
 
        st.error( 
            f"❌ Graph setup failed: {str(e)}" 
        ) 
 
        print( 
            "Graph Setup Error:", 
            e 
        ) 
 
        return 
 
    # ===================================================== 
    # 9. DISPLAY RESULT 
    # ===================================================== 
 
    try: 
 
        display_result = DisplayResultStreamlit( 
            usecase=usecase, 
            graph=graph, 
            user_message=user_message 
        ) 
 
        display_result.display_result_on_ui() 
 
    except Exception as e: 
 
        st.error( 
            f"❌ Error while processing request: {str(e)}" 
        ) 
 
        print( 
            "Processing Error:", 
            e 
        ) 
 
        return 
 
    # ===================================================== 
    # 10. RESET AI NEWS FETCH BUTTON 
    # ===================================================== 
 
    if usecase == "AI News": 
 
        st.session_state.IsFetchButtonClicked = False 