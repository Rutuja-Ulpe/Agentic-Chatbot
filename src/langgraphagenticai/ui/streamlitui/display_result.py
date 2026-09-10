import streamlit as st

from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    ToolMessage
)


class DisplayResultStreamlit:

    def __init__(self, usecase, graph, user_message):
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message

    def display_result_on_ui(self):

        usecase = self.usecase
        graph = self.graph
        user_message = self.user_message

        print("User Message:", user_message)

        # =====================================================
        # BASIC CHATBOT
        # =====================================================

        if usecase == "Basic Chatbot":

            for event in graph.stream(
                {
                    "messages": [
                        HumanMessage(content=user_message)
                    ]
                }
            ):

                for value in event.values():

                    if "messages" in value:

                        message = value["messages"]

                        with st.chat_message("user"):
                            st.write(user_message)

                        with st.chat_message("assistant"):

                            if hasattr(message, "content"):
                                st.write(message.content)
                            else:
                                st.write(message)

        # =====================================================
        # CHATBOT WITH WEB
        # =====================================================

        elif usecase == "Chatbot With Web":

            initial_state = {
                "messages": [
                    HumanMessage(content=user_message)
                ]
            }

            with st.spinner("Searching the web... 🔎"):

                res = graph.invoke(initial_state)

            for message in res.get("messages", []):

                if isinstance(message, HumanMessage):

                    with st.chat_message("user"):
                        st.write(message.content)

                elif isinstance(message, ToolMessage):

                    with st.chat_message("assistant"):
                        st.write("🔎 Web Search Result")
                        st.write(message.content)

                elif isinstance(message, AIMessage):

                    if message.content:

                        with st.chat_message("assistant"):
                            st.write(message.content)

        # =====================================================
        # AI NEWS
        # =====================================================

        elif usecase == "AI News":

            news_query = str(user_message).strip()

            if not news_query:
                st.warning("⚠️ Please enter an AI News query.")
                return

            with st.spinner("Fetching and summarizing AI news... ⏳"):

                try:

                    # Send the complete natural-language query
                    # to the AI News graph.

                    initial_state = {
                        "messages": [
                            HumanMessage(content=news_query)
                        ]
                    }

                    result = graph.invoke(initial_state)

                    print("AI News Result:")
                    print(result)

                    # -------------------------------------------------
                    # Display summary
                    # -------------------------------------------------

                    summary = result.get("summary")

                    if summary:

                        st.subheader("📰 AI News Summary")

                        st.markdown(summary)

                    else:

                        st.warning(
                            "⚠️ No AI news summary was generated."
                        )

                    # -------------------------------------------------
                    # Saved file
                    # -------------------------------------------------

                    filename = result.get("filename")

                    if filename:

                        st.success(
                            f"✅ Summary saved to: {filename}"
                        )

                except Exception as e:

                    st.error(
                        f"❌ AI News Error: {str(e)}"
                    )

                    print("AI News Error:", e)

        # =====================================================
        # UNKNOWN USECASE
        # =====================================================

        else:

            st.error(
                f"❌ Unknown usecase: {usecase}"
            )