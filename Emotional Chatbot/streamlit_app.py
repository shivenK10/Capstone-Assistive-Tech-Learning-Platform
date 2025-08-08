import streamlit as st

from emotion_detection_pipeline import detect_enhanced_emotion
from generation_pipeline import generate_educational_response
from logger import Logger

logger = Logger(
    name="Educational ChatBot-UI",
    log_file_needed=True,
    log_file="Logs/educational_chatbot_ui.log",
    level="DEV"
)

st.set_page_config(page_title="🎓 Educational Support Chatbot", page_icon="🎓")

if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "profile" not in st.session_state:
    st.session_state.profile = {
        "session_count": 0,
        "identified_needs": set(),
        "emotional_patterns": []
    }

with st.sidebar:
    st.title("👤 Learning Profile")
    profile = st.session_state.profile
    st.markdown(f"- **Sessions:** {profile['session_count']}")
    if profile["identified_needs"]:
        st.markdown(f"- **Learning patterns:** {', '.join(profile['identified_needs'])}")
    if profile["emotional_patterns"]:
        st.markdown(
            f"- **Recent emotions:** {', '.join(profile['emotional_patterns'][-5:])}"
        )

    st.markdown("---")
    with st.expander("ℹ️ Help", expanded=False):
        st.write(
            """
            • Ask me homework questions or share how you feel about studying.  
            • Tell me if you have dyslexia, ADHD, or other learning differences.  
            • Be specific about what's confusing or frustrating you.  
            • Every question is a good question—just type and hit **Enter**!
            """
        )


st.title("🎓 Educational Support Chatbot")
st.markdown(
    "Hello! I'm your AI learning companion. Ask anything about schoolwork or how you're feeling about learning."
)

for turn in st.session_state.conversation:
    with st.chat_message("user"):
        st.markdown(turn["user"])
    with st.chat_message("assistant"):
        st.markdown(turn["bot"])
        emo = turn["emotion"]
        st.caption(
            f"🧠 *Detected:* {emo['primary_emotion'].title()} "
            f"({emo['confidence']:.0%}) — {emo['educational_context']}"
        )

user_input = st.chat_input("Type your question or feeling …")

if user_input:
    logger.debug(f"User: {user_input}")

    emotion = detect_enhanced_emotion(
        user_input,
        {
            "conversation_history": st.session_state.conversation[-3:],
            "student_profile": st.session_state.profile,
        },
    )

    bot_reply = generate_educational_response(user_input, emotion)

    st.session_state.conversation.append(
        {"user": user_input, "bot": bot_reply, "emotion": emotion}
    )
    profile = st.session_state.profile
    profile["session_count"] += 1
    profile["emotional_patterns"].append(emotion["primary_emotion"])
    if emotion["educational_context"] != "general":
        profile["identified_needs"].add(emotion["educational_context"])
    for ind in emotion["special_needs_indicators"]:
        profile["identified_needs"].add(ind)

    st.rerun()
