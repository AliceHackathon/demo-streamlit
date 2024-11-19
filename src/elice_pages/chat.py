import streamlit as st

from elice_pages.components.cache import get_chat_chain
from elice_pages.components.select import select_llm
from elice_pages.components.session_state import SessionChatMessage, SessionState
from config import settings


st.session_state = SessionState()

st.markdown(
    f"""
# Chat Demo

- Current Session ID: `{st.session_state.session_id}`

---
"""
)

st.session_state.display_all_messages()


if settings.enable_sidebar_selectboxes:
    selected_llm = select_llm("LLM", "gpt-4o-mini")
    verbose = st.sidebar.checkbox("Verbose", value=False)


else:
    selected_llm = "gpt-4o-mini"
    verbose = False


chain = get_chat_chain(selected_llm)


if prompt := st.chat_input("Ask anything!"):
    st.session_state.append_message(SessionChatMessage(role="user", content=prompt))

    assistant_dict = {"role": "assistant"}
    with st.chat_message("assistant", avatar="🤖"):
        with st.status("Thinking...", expanded=True) as status:
            # try:
            #     result = chain.invoke(prompt, st.session_state.session_id)

            #     assistant_dict |= {"content": result}

            # except Exception as e:
            #     assistant_dict |= {
            #         "content": f"""Sorry, there was an error on the server. Please try again.""",
            #         "error": str(e.with_traceback(None)),
            #     }
            result = chain.invoke(prompt, st.session_state.session_id)

            assistant_dict |= {
                "content": result["response"],
                "emotion": result["emotion"],
            }

        chat_message = SessionChatMessage(**assistant_dict)

        st.write(chat_message.content)
        st.markdown(f"**감정 :** {chat_message.emotion}")

        st.session_state.messages.append(chat_message)
