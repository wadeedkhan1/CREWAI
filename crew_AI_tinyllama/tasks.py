from crewai import Task

def create_simple_tasks(agent):
    return [
        Task(
            description="Answer the question: What is a healthy breakfast option?",
            expected_output="A brief and simple answer, suitable for a general audience.",
            agent=agent
        )
    ]

def create_research_task(agent):
    return Task(
        description=(
            "Conduct comprehensive research on the latest advancements in AI, focusing on large language models (LLMs) and their applications. "
            "Identify key trends, breakthroughs, and potential future impacts." 
            "Your final answer MUST be a detailed report in markdown format, summarizing your findings with sources and specific examples."
        ),
        expected_output="A comprehensive report on the latest AI advancements in LLMs, including trends, breakthroughs, and future impacts, with sources.",
        agent=agent,
    )

def create_write_article_task(agent, context_tasks):
    return Task(
        description=(
            "Using the research report provided, write a compelling and informative article (minimum 500 words) about the latest advancements in LLMs. "
            "The article should be engaging for a general audience, explaining complex concepts clearly and highlighting the most significant aspects of the research. "
            "Your final answer MUST be the full article in markdown format."
        ),
        expected_output="A comprehensive and engaging article (minimum 500 words) on LLM advancements, based on the provided research, in markdown format.",
        agent=agent,
        context=context_tasks,
    )

def create_review_article_task(agent, context_tasks):
    return Task(
        description=(
            "Review the provided article for clarity, grammatical errors, factual accuracy (if verifiable from context), and overall structure. "
            "Ensure the article meets the minimum word count requirement and is engaging for a general audience. "
            "Provide constructive feedback and rewrite sections if necessary to improve quality and readability. "
            "Your final answer MUST be the refined article in markdown format."
        ),
        expected_output="A refined and polished article in markdown format, with improved clarity, structure, and readability.",
        agent=agent,
        context=context_tasks,
    )