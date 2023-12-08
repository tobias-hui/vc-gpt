import streamlit as st
from langchain.callbacks import StreamlitCallbackHandler
from app.xml_agent import agent_executor as agent

with st.sidebar:
    # 显示 VCGPT logo
    st.image("https://i.ibb.co/SNKTtbt/vcgpt-logo-removebg-preview.png", width=66)  # 替换 "vcgpt_logo_url" 为实际的图片 URL

    # VCGPT 简介
    st.markdown("## VCGPT")
    st.markdown("""
    VCGPT 是一款先进的聊天助手，专为帮助创业者和初创企业经理快速有效地撰写商业计划而设计。
    """)

st.title("🔎 VCGPT - 天下没有难找的投资")

"""
VCGPT致力于帮助投资者和创业者进行对接，帮助创业者在初期低成本快速的生成BP商业计划并且分析市场数据，对接到匹配的投资机构.
"""

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "你好啊勇敢的创业者，我是VCGPT，帮助你生成专属的商业计划，踏上这条充满危险的创业之路。"},
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input(placeholder="我想要创建一家金融科技公司"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        response = agent.invoke(
            input={
                "question": st.session_state.messages,
                "chat_history":[],
                #"intermediate_steps":[],
            }
            )
        #response = agent.invoke(st.session_state.messages, callbacks=[st_cb])
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)
