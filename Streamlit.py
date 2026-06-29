import streamlit as st
from graph import graph
import os


st.set_page_config(
    page_title="Medical HealthBot",
    page_icon="🩺",
    layout="wide"
)

st.title("🩺 Medical HealthBot")
st.caption("AI-Powered Patient Education System")


WELCOME_MESSAGE = """
# 👋 Hello!

I am **Medical HealthBot: AI-Powered Patient Education System** 🩺

I can help you:

✅ Explain diseases in simple language

✅ Provide symptoms, causes, treatment & prevention

✅ Generate a short quiz

✅ Evaluate your answers

---

### Please enter a health topic to begin.

**Examples**

- Diabetes
- Hypertension
- Asthma
- Dengue
- Migraine
"""

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": WELCOME_MESSAGE
        }
    ]

if "stage" not in st.session_state:
    st.session_state.stage = "topic"

if "state" not in st.session_state:
    st.session_state.state = {}

if "reply" not in st.session_state:
    st.session_state.reply = ""

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


user_input = st.chat_input("Type here...")

if user_input:

    # -----------------------
    # User Message
    # -----------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)


    if st.session_state.stage == "topic":

        state = {
            "topic": user_input,
            "ready": ""
        }

        result = graph.invoke(state)

        st.session_state.state = result

        reply = (
            result["summary"] +
            "\n\n---\n\n"
            "**Would you like to take a quiz? (yes/no)**"
            "**if yes which Type MCQ or Simple Comprehension Question**"
        )

        st.session_state.stage = "ready"


    elif st.session_state.stage == "ready":

        if user_input.lower() == "yes":

            state = st.session_state.state
            state["ready"] = "yes"

            result = graph.invoke(state)

            st.session_state.state = result

            reply = (
                "## 📝 Quiz\n\n"
                + result["quiz_question"]
            )

            st.session_state.stage = "answer"

        elif user_input.lower() == "no":

            reply = (
                "😊 No problem.\n\n"
                "Would you like to learn another topic? (yes/no)"
            )

            st.session_state.stage = "continue"

        else:

            reply = "Please type **yes** or **no**."


    elif st.session_state.stage == "answer":

        state = st.session_state.state

        state["user_answer"] = user_input

        result = graph.invoke(state)

        st.session_state.state = result

        reply = (
            result["feedback"]
            + "\n\n---\n\n"
            + "Would you like another topic? (yes/no)"
        )

        st.session_state.stage = "continue"


    elif st.session_state.stage == "continue":

        if user_input.lower() == "yes":

            st.session_state.state = {}

            reply = (
                "Great! 😊\n\n"
                "Please enter another health topic."
            )

            st.session_state.stage = "topic"

        elif user_input.lower() == "no":

            reply = "👋 Thank you for using Medical HealthBot ❤️"

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": reply
                }
            )

            with st.chat_message("assistant"):
                st.markdown(reply)

            import time
            time.sleep(2)

            # Reset everything

            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": WELCOME_MESSAGE
                }
            ]

            st.session_state.state = {}

            st.session_state.stage = "topic"

            st.rerun()

        else:

            reply = "Please type **yes** or **no**."

    else:

        reply = "Session Ended."


    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": reply
        }
    )

    with st.chat_message("assistant"):
        st.markdown(reply)
            
