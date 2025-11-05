# import streamlit as st
# from backend import stream_rag_chain


# # --- Streamlit App ---

# st.set_page_config(page_title="Bank Chatbot with RAG", layout="centered")

# st.title("learn signal in angular")

# # --- Sidebar for Inputs ---
# with st.sidebar:
#     st.header("Configuration")
#     model = st.selectbox("Select model:", ["Gemini", "Open AI"])
#     language = st.selectbox("Select language:", ["English", "Hebrew"])

#     if st.button("Clear Chat History"):
#         st.session_state.messages = []
#         st.rerun()

# # --- Chat Interface ---

# # Initialize chat history in session state if it doesn't exist
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # Display past messages from the chat history
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# # Get user input from the chat input box
# if prompt := st.chat_input("What is your question?"):
#     with st.chat_message("user"):
#         st.markdown(prompt)

#     # Get assistant response and display it
#     with st.chat_message("assistant"):

#         # stream
#         response = st.write_stream(stream_rag_chain(prompt))


#     # Add user message to chat history and display it
#     st.session_state.messages.append({"role": "user", "content": prompt})

#     # Add assistant response to chat history
#     st.session_state.messages.append({"role": "assistant", "content": response})
import streamlit as st
from backend import stream_rag_chain

# --- Streamlit App ---
st.set_page_config(page_title="Learn Signals in Angular", layout="centered")
st.title("💬 Learn Angular Signals with AI")

# --- Sidebar ---
with st.sidebar:
    st.header("Configuration")
    model = st.selectbox("Select model:", ["Gemini", "Open AI"])
    language = st.selectbox("Select language:", ["English", "Hebrew"])

    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# --- Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"], unsafe_allow_html=True)

# --- Chat Input ---
if prompt := st.chat_input("Ask something about Angular Signals..."):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get model answer (streamed)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Stream the response and collect it into one string
            full_response = ""
            for chunk in stream_rag_chain(prompt):
                full_response += chunk
                st.write(chunk, end="")

        # ✅ הצגת לינקים למקורות (אם קיימים)
        st.markdown(
            f"\n\n📚 **Source:** [Angular.dev Signals Guide](https://angular.dev/guide/signals)",
            unsafe_allow_html=True
        )

    # --- שמירת ההודעות בהיסטוריה ---
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append({
        "role": "assistant",
        "content": f"{full_response}\n\n📚 [Angular.dev Signals Guide](https://angular.dev/guide/signals)"
    })
