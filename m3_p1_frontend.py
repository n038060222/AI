import streamlit as st
from m3_p1_backend import call_llm

st.title("🗣️ Interactive Language Learning Chat")

# Sidebar for configuration
with st.sidebar:
    st.header("Settings")
    
    # שפת אם
    home_language = st.selectbox(
        "בחר את שפת האם שלך:",
        ("Hebrew", "English", "Russian")
    )

    # שפה ללמידה
    language_to_learn = st.selectbox(
        "בחר את השפה שברצונך ללמוד:",
        ("English", "Hebrew", "Spanish", "French", "German")
    )

    # רמת קושי
    level = st.selectbox(
        "בחר את רמת הקושי:",
        ("Beginner", "Intermediate", "Advanced")
    )

    # שם המורה
    assistant_name = st.text_input("שם המורה:", "Alex")

    # נושא השיעור
    topic = st.selectbox(
        "בחר נושא לשיעור:",
        ("General", "Restaurant", "Travel", "Airport", "Shopping", "Work")
    )

st.divider()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("Ask or practice something in your target language..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # Get assistant reply
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = call_llm(
                user_input=prompt,
                assistant_name=assistant_name,
                home_language=home_language,
                language_to_learn=language_to_learn,
                level=level,
                topic=topic,  # <-- העברת נושא
                history=st.session_state.messages
            )
            st.markdown(response)

    # Save assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
