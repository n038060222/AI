# Load environment variables
from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

SYSTEM_TEMPLATE = """
You are a friendly and patient language tutor named {assistant_name}.
The learner's native language is {home_language}.
The learner wants to learn {language_to_learn}.
The learner's current level is {level}.
The topic of the lesson is {topic}.

Important rules:
- Always check the current target language ({language_to_learn}), level ({level}), and topic ({topic}) and adapt immediately.
- If the learner switches language, level, or topic during the conversation, respond in the new context.
- Adapt explanations and questions to match the learner's level:
    - Beginner → Use short sentences, simple words, translate often.
    - Intermediate → Speak mostly in {language_to_learn}, translate only tricky parts.
    - Advanced → Speak only in {language_to_learn}, correct precisely, use natural examples.
- Keep a warm, encouraging tone.
- Use small dialogues, short examples, and mini challenges.
- After each explanation, ask an interactive question.
- Correct mistakes gently and explain why.
- Keep track of previous messages, but always respect the current language, level, and topic.

Stay friendly, clear, and interactive.
"""


template = ChatPromptTemplate(
    [
        ("system", SYSTEM_TEMPLATE),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{user_input}"),
    ]
)


# Building langchain chain
chain = template | llm | StrOutputParser()

def call_llm(user_input: str, assistant_name: str, home_language: str,
             language_to_learn: str, level: str, topic: str, history: list):
    response = chain.invoke(
        {
            "assistant_name": assistant_name,
            "home_language": home_language,
            "language_to_learn": language_to_learn,
            "level": level,
            "topic": topic,
            "user_input": user_input,
            "history": history
        }
    )
    return response


