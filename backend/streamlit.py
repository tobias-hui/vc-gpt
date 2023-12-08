import streamlit as st
from langchain.callbacks import StreamlitCallbackHandler
from app.xml_agent import agent_executor as agent

# with st.sidebar:
#     # 显示 VCGPT logo
#     st.image("https://i.ibb.co/SNKTtbt/vcgpt-logo-removebg-preview.png", width=66)  # 替换 "vcgpt_logo_url" 为实际的图片 URL

#     # VCGPT 简介
#     st.markdown("""
#     VCGPT 是一款先进的聊天助手，专为帮助创业者和初创企业经理快速有效地撰写商业计划而设计。
#     """)

st.set_page_config(
    page_title='VCGPT-Agent',
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)


#st.markdown('<img src="https://i.ibb.co/Wncjq6P/vcgpt-01-removebg-preview.png" width="150" height="50">', unsafe_allow_html=True)
st.image("https://i.ibb.co/xgWdnrz/vcgpt-01-removebg-preview.png", width=150)
st.header("Be Your Personal Business Agent", divider = "violet")
# """
# Be Your Personal Business Agent
# """

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "你好，请问需要什么帮助"},
    ]

for msg in st.session_state.messages:
    avatar_url = "https://i.ibb.co/SNKTtbt/vcgpt-logo-removebg-preview.png" if msg["role"] == "assistant" else "https://i.ibb.co/9VnnBnc/White-Creative-Doodle-Brainstorming-Presentation-2-removebg-preview.png"
    with st.chat_message(msg["role"], avatar=avatar_url):
        st.write(msg["content"])

if prompt := st.chat_input(placeholder="我想要创建一家金融科技公司"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="https://i.ibb.co/9VnnBnc/White-Creative-Doodle-Brainstorming-Presentation-2-removebg-preview.png"):
        st.write(prompt)

    with st.chat_message("assistant", avatar="https://i.ibb.co/SNKTtbt/vcgpt-logo-removebg-preview.png"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        response = agent.invoke(
            input={
                "question": st.session_state.messages,
                "chat_history":[],
                #"intermediate_steps":[],
            }
        )
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)

