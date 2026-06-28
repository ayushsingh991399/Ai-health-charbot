from dotenv import load_dotenv
import os
from langchain_community.tools import TavilySearchResults
from langchain_openai import ChatOpenAI
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

load_dotenv("config.env")
assert os.getenv("GOOGLE_API_KEY")
assert os.getenv("TAVILY_API_KEY")

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0
)

class HealthState(TypedDict):
    topic: str
    search_results: str
    summary: str
    quiz: str
    answer: str
    grade: str
    feedback: str
    continue_chat: bool


search_tool = TavilySearchResults(max_results=5)

def ask_topic(state):
    topic = input("Enter a health topic: ")

    return {
        "topic": topic
    }


def tavily_search(state):
    results = search_tool.invoke(state["topic"])

    return {
        "search_results": results
    }

def summarize(state):

    prompt = f"""
    You are a helpful medical assistant.

    Summarize the following medical information in simple,
    patient-friendly language.

    Include:
    - What it is
    - Symptoms
    - Causes
    - Treatment
    - Prevention

    Search Results:
    {state["search_results"]}
    """

    response = llm.invoke(prompt)

    return {
        "summary": response.content
    }

def display_summary(state):

    print("\n" + "="*60)
    print("MEDICAL SUMMARY")
    print("="*60)

    print(state["summary"])

    print("="*60)

    return {}

def ready_check(state):

    ready = input("\nType 'yes' when you are ready for the quiz: ")

    return {
        "ready": ready
    }

def generate_quiz(state):

    prompt = f"""
    You are a medical educator.

    Based on the summary below, generate ONE simple
    comprehension question for the patient.

    Summary:
    {state["summary"]}

    Return only the question.
    """

    response = llm.invoke(prompt)

    return {
        "quiz_question": response.content
    }

def ask_quiz(state):

    print("\n" + "="*60)
    print("QUIZ")
    print("="*60)

    print(state["quiz_question"])

    print("="*60)

    return {}

def receive_answer(state):

    answer = input("\nEnter your answer: ")

    return {
        "user_answer": answer
    }

def grade_answer(state):

    prompt = f"""
You are a medical instructor.

Summary:
{state["summary"]}

Question:
{state["quiz_question"]}

Patient's Answer:
{state["user_answer"]}

Evaluate the patient's answer.

Return in this format:

Grade: Correct / Partially Correct / Incorrect

Explanation:
Explain why.

Citation:
Mention the relevant part of the summary.
"""

    response = llm.invoke(prompt)

    return {
        "feedback": response.content
    }

def display_feedback(state):

    print("\n" + "="*60)
    print("QUIZ RESULT")
    print("="*60)

    print(state["feedback"])

    print("="*60)

    return {}

def continue_or_exit(state):

    choice = input(
        "\nWould you like to learn another topic? (yes/no): "
    ).strip().lower()

    return {
        "continue_session": choice
    }

def reset_state(state):

    if state["continue_session"] == "yes":

        return {
            "topic": "",
            "search_results": [],
            "summary": "",
            "ready": "",
            "quiz_question": "",
            "user_answer": "",
            "feedback": "",
            "continue_session": ""
        }

    return {}

builder = StateGraph(HealthState)


builder.add_node("ask_topic", ask_topic)
builder.add_node("tavily_search", tavily_search)
builder.add_node("summarize", summarize)
builder.add_node("display_summary", display_summary)
builder.add_node("ready_check", ready_check)
builder.add_node("generate_quiz", generate_quiz)
builder.add_node("ask_quiz", ask_quiz)
builder.add_node("receive_answer", receive_answer)
builder.add_node("grade", grade_answer)
builder.add_node("feedback", display_feedback)
builder.add_node("continue", continue_or_exit)
builder.add_node("reset", reset_state)


builder.add_edge(START, "ask_topic")
builder.add_edge("ask_topic", "tavily_search")
builder.add_edge("tavily_search", "summarize")
builder.add_edge("summarize", "display_summary")
builder.add_edge("display_summary", "ready_check")
builder.add_edge("ready_check", "generate_quiz")
builder.add_edge("generate_quiz", "ask_quiz")
builder.add_edge("ask_quiz", "receive_answer")
builder.add_edge("receive_answer", "grade")
builder.add_edge("grade", "feedback")
builder.add_edge("feedback", "continue")
builder.add_edge("continue", "reset")
builder.add_edge("reset", END)

graph = builder.compile()