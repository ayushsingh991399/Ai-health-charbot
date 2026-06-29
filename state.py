from typing import TypedDict, List


class HealthState(TypedDict):

    topic: str
    search_results: List
    summary: str
    ready: str
    quiz_type: str
    quiz_question: str
    user_answer: str
    feedback: str
    continue_chat: str
