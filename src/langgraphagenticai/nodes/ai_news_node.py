import os

from tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplate


class AINewsNode:

    def __init__(self, llm):
        """
        Initialize AI News Node.

        Args:
            llm: LangChain-compatible LLM model.
        """

        self.llm = llm

        # -------------------------------------------------
        # Get Tavily API key
        # -------------------------------------------------

        tavily_api_key = os.getenv("TAVILY_API_KEY")

        if not tavily_api_key:
            raise ValueError(
                "TAVILY_API_KEY is missing. "
                "Please enter your Tavily API key in the UI."
            )

        self.tavily = TavilyClient(
            api_key=tavily_api_key
        )

    # =====================================================
    # DETECT TIMEFRAME
    # =====================================================

    def detect_timeframe(self, query: str) -> str:
        """
        Detect whether the user wants daily, weekly,
        or monthly news.
        """

        query_lower = query.lower().strip()

        # -------------------------------------------------
        # Monthly
        # -------------------------------------------------

        monthly_keywords = [
            "this month",
            "monthly",
            "month",
            "last 30 days",
            "past month",
            "last month"
        ]

        for keyword in monthly_keywords:

            if keyword in query_lower:
                return "monthly"

        # -------------------------------------------------
        # Weekly
        # -------------------------------------------------

        weekly_keywords = [
            "this week",
            "weekly",
            "week",
            "last 7 days",
            "past week",
            "last week"
        ]

        for keyword in weekly_keywords:

            if keyword in query_lower:
                return "weekly"

        # -------------------------------------------------
        # Daily
        # -------------------------------------------------

        daily_keywords = [
            "today",
            "today's",
            "today news",
            "latest",
            "latest news",
            "latest ai news",
            "last 24 hours",
            "past day",
            "daily",
            "yesterday"
        ]

        for keyword in daily_keywords:

            if keyword in query_lower:
                return "daily"

        # -------------------------------------------------
        # Default
        # -------------------------------------------------

        return "daily"

    # =====================================================
    # BUILD SEARCH QUERY
    # =====================================================

    def build_search_query(self, query: str) -> str:
        """
        Build a better Tavily search query.
        """

        query_lower = query.lower().strip()

        # -------------------------------------------------
        # Predefined timeframe buttons
        # -------------------------------------------------

        if query_lower == "daily":

            return (
                "latest artificial intelligence AI technology "
                "news India and globally"
            )

        if query_lower == "weekly":

            return (
                "artificial intelligence AI technology "
                "news India and globally"
            )

        if query_lower == "monthly":

            return (
                "artificial intelligence AI technology "
                "major news India and globally"
            )

        # -------------------------------------------------
        # Natural language query
        # -------------------------------------------------

        return query

    # =====================================================
    # FETCH NEWS
    # =====================================================

    def fetch_news(self, state: dict) -> dict:
        """
        Fetch AI news using Tavily.
        """

        # -------------------------------------------------
        # Get message
        # -------------------------------------------------

        messages = state.get("messages", [])

        if not messages:

            raise ValueError(
                "No news query was provided."
            )

        message = messages[0]

        # LangChain message
        if hasattr(message, "content"):

            query = message.content

        else:

            query = str(message)

        query = str(query).strip()

        if not query:

            raise ValueError(
                "News query cannot be empty."
            )

        # -------------------------------------------------
        # Detect timeframe
        # -------------------------------------------------

        frequency = self.detect_timeframe(query)

        print("----------------------------------------")
        print("AI NEWS QUERY:", query)
        print("DETECTED TIMEFRAME:", frequency)
        print("----------------------------------------")

        # -------------------------------------------------
        # Tavily configuration
        # -------------------------------------------------

        time_range_map = {
            "daily": "d",
            "weekly": "w",
            "monthly": "m"
        }

        days_map = {
            "daily": 1,
            "weekly": 7,
            "monthly": 30
        }

        # -------------------------------------------------
        # Build search query
        # -------------------------------------------------

        search_query = self.build_search_query(query)

        print("TAVILY SEARCH QUERY:", search_query)

        # -------------------------------------------------
        # Tavily Search
        # -------------------------------------------------

        response = self.tavily.search(
            query=search_query,
            topic="news",
            time_range=time_range_map[frequency],
            include_answer="advanced",
            max_results=20,
            days=days_map[frequency]
        )

        # -------------------------------------------------
        # Get results
        # -------------------------------------------------

        news_data = response.get(
            "results",
            []
        )

        print(
            "NUMBER OF NEWS ARTICLES:",
            len(news_data)
        )

        # -------------------------------------------------
        # Return updated state
        # -------------------------------------------------

        return {

            "messages": messages,

            "news_data": news_data,

            "frequency": frequency,

            "query": query
        }

    # =====================================================
    # SUMMARIZE NEWS
    # =====================================================

    def summarize_news(self, state: dict) -> dict:
        """
        Summarize fetched news using the selected LLM.
        """

        news_items = state.get(
            "news_data",
            []
        )

        frequency = state.get(
            "frequency",
            "daily"
        )

        query = state.get(
            "query",
            ""
        )

        messages = state.get(
            "messages",
            []
        )

        # -------------------------------------------------
        # No news found
        # -------------------------------------------------

        if not news_items:

            summary = (
                "## No AI News Found\n\n"
                "No relevant AI news articles were found "
                "for the selected query and timeframe."
            )

            return {

                "messages": messages,

                "news_data": [],

                "frequency": frequency,

                "query": query,

                "summary": summary
            }

        # -------------------------------------------------
        # Prepare articles
        # -------------------------------------------------

        articles = []

        for index, item in enumerate(news_items, start=1):

            title = item.get(
                "title",
                "No title"
            )

            content = item.get(
                "content",
                ""
            )

            url = item.get(
                "url",
                ""
            )

            published_date = item.get(
                "published_date",
                ""
            )

            articles.append(
                f"""
ARTICLE {index}

Title:
{title}

Content:
{content}

Published Date:
{published_date}

Source URL:
{url}
"""
            )

        articles_str = "\n\n".join(
            articles
        )

        # -------------------------------------------------
        # Prompt
        # -------------------------------------------------

        prompt_template = ChatPromptTemplate.from_messages(
            [

                (
                    "system",
                    """
You are a professional AI News Analyst.

Your task is to analyze the provided news articles
and create a clear, accurate and concise AI news report.

USER'S REQUEST:
Use the user's query to understand what type of
AI news they are interested in.

IMPORTANT INSTRUCTIONS:

1. Include only relevant AI/technology news.
2. Remove duplicate articles.
3. Sort articles from newest to oldest.
4. Do not invent facts.
5. Use the article content provided.
6. Include the original source URL.
7. Keep summaries concise but informative.
8. Mention important companies or organizations.
9. If the publication date is available, use it.
10. Use Markdown formatting.

For each article use this format:

### YYYY-MM-DD

- **Title:** Article title
- **Summary:** 2-4 sentence concise summary
- **Company/Organization:** Important company if available
- **Source:** [Read Full Article](URL)

At the beginning, include a short heading:

# AI News Summary

Then list the articles from latest to oldest.
"""
                ),

                (
                    "user",
                    """
User Query:
{query}

Detected Timeframe:
{frequency}

News Articles:
{articles}
"""
                )

            ]
        )

        # -------------------------------------------------
        # Create prompt
        # -------------------------------------------------

        prompt = prompt_template.format(
            query=query,
            frequency=frequency,
            articles=articles_str
        )

        print("Sending news articles to LLM...")

        # -------------------------------------------------
        # Invoke LLM
        # -------------------------------------------------

        response = self.llm.invoke(
            prompt
        )

        # -------------------------------------------------
        # Extract response
        # -------------------------------------------------

        if hasattr(response, "content"):

            summary = response.content

        else:

            summary = str(response)

        summary = str(summary).strip()

        # -------------------------------------------------
        # Fallback
        # -------------------------------------------------

        if not summary:

            summary = self.create_fallback_summary(
                news_items
            )

        print(
            "SUMMARY GENERATED:",
            bool(summary)
        )

        # -------------------------------------------------
        # Return state
        # -------------------------------------------------

        return {

            "messages": messages,

            "news_data": news_items,

            "frequency": frequency,

            "query": query,

            "summary": summary
        }

    # =====================================================
    # FALLBACK SUMMARY
    # =====================================================

    def create_fallback_summary(
        self,
        news_items: list
    ) -> str:
        """
        Create a basic summary if LLM returns
        an empty response.
        """

        output = "# AI News Summary\n\n"

        for item in news_items:

            title = item.get(
                "title",
                "Untitled"
            )

            content = item.get(
                "content",
                "No description available."
            )

            url = item.get(
                "url",
                ""
            )

            published_date = item.get(
                "published_date",
                "Date not available"
            )

            # Limit content length
            content = str(content).strip()

            if len(content) > 500:

                content = content[:500] + "..."

            output += (
                f"### {published_date}\n\n"
                f"- **Title:** {title}\n"
                f"- **Summary:** {content}\n"
                f"- **Source:** "
                f"[Read Full Article]({url})\n\n"
            )

        return output

    # =====================================================
    # SAVE RESULT
    # =====================================================

    def save_result(self, state: dict) -> dict:
        """
        Save AI News summary into Markdown file.
        """

        frequency = state.get(
            "frequency",
            "daily"
        )

        summary = state.get(
            "summary",
            ""
        )

        query = state.get(
            "query",
            ""
        )

        news_data = state.get(
            "news_data",
            []
        )

        messages = state.get(
            "messages",
            []
        )

        # -------------------------------------------------
        # Make sure directory exists
        # -------------------------------------------------

        os.makedirs(
            "./AINews",
            exist_ok=True
        )

        # -------------------------------------------------
        # File path
        # -------------------------------------------------

        filename = (
            f"./AINews/"
            f"{frequency}_summary.md"
        )

        # -------------------------------------------------
        # Save Markdown
        # -------------------------------------------------

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
                f"# {frequency.capitalize()} AI News Summary\n\n"
            )

            f.write(
                f"**User Query:** {query}\n\n"
            )

            f.write(
                summary
            )

        print(
            "News summary saved to:",
            filename
        )

        # -------------------------------------------------
        # Return final state
        # -------------------------------------------------

        return {

            "messages": messages,

            "news_data": news_data,

            "frequency": frequency,

            "query": query,

            "summary": summary,

            "filename": filename
        }