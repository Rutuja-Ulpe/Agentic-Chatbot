from langgraph.graph import StateGraph
from src.langgraphagenticai.state.state import State
from langgraph.graph import START, END
from src.langgraphagenticai.nodes.basic_chatbot_node import BasicChatbotNode
from src.langgraphagenticai.tools.search_tool import get_tools, create_tool_node
from langgraph.prebuilt import tools_condition
from src.langgraphagenticai.nodes.chatbot_with_Tool_node import ChatbotWithToolNode
from src.langgraphagenticai.nodes.ai_news_node import AINewsNode


class GraphBuilder:

    def __init__(self, model):
        self.llm = model
        self.graph_builder = StateGraph(State)

    def basic_chatbot_build_graph(self):
        """
        Builds a basic chatbot graph using LangGraph.
        """

        self.basic_chatbot_node = BasicChatbotNode(self.llm)

        self.graph_builder.add_node(
            "chatbot",
            self.basic_chatbot_node.process
        )

        self.graph_builder.add_edge(
            START,
            "chatbot"
        )

        self.graph_builder.add_edge(
            "chatbot",
            END
        )

    def chatbot_with_tools_build_graph(self):
        """
        Builds an advanced chatbot graph with tool integration.
        """

        # Define the tools and tool node
        tools = get_tools()
        tool_node = create_tool_node(tools)

        # Define the LLM
        llm = self.llm

        # Define chatbot node
        obj_chatbot_with_node = ChatbotWithToolNode(llm)
        chatbot_node = obj_chatbot_with_node.create_chatbot(tools)

        # Add nodes
        self.graph_builder.add_node(
            "chatbot",
            chatbot_node
        )

        self.graph_builder.add_node(
            "tools",
            tool_node
        )

        # Define edges
        self.graph_builder.add_edge(
            START,
            "chatbot"
        )

        self.graph_builder.add_conditional_edges(
            "chatbot",
            tools_condition
        )

        self.graph_builder.add_edge(
            "tools",
            "chatbot"
        )

    def ai_news_build_graph(self):
        """
        Builds the AI News workflow.

        Flow:
        START -> fetch_news -> summarize_news -> save_result -> END
        """

        ai_news_node = AINewsNode(self.llm)

        # Add AI News nodes
        self.graph_builder.add_node(
            "fetch_news",
            ai_news_node.fetch_news
        )

        self.graph_builder.add_node(
            "summarize_news",
            ai_news_node.summarize_news
        )

        self.graph_builder.add_node(
            "save_result",
            ai_news_node.save_result
        )

        # Define edges
        self.graph_builder.add_edge(
            START,
            "fetch_news"
        )

        self.graph_builder.add_edge(
            "fetch_news",
            "summarize_news"
        )

        self.graph_builder.add_edge(
            "summarize_news",
            "save_result"
        )

        self.graph_builder.add_edge(
            "save_result",
            END
        )

    def setup_graph(self, usecase: str):
        """
        Sets up the graph for the selected use case.
        """

        if usecase == "Basic Chatbot":
            self.basic_chatbot_build_graph()

        elif usecase == "Chatbot With Web":
            self.chatbot_with_tools_build_graph()

        elif usecase == "AI News":
            self.ai_news_build_graph()

        return self.graph_builder.compile()