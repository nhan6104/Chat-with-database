import streamlit as st
from main import hostAI
import seaborn as sns
import matplotlib.pyplot as plt
import json
import pandas as pd

st.title("Chat with database")

if "messages" not in st.session_state:
    st.session_state.messages = []

if 'host' not in st.session_state:
    st.session_state.host = hostAI()
    st.session_state.host.subscribeTool("ecommerce", "These tools use chat with data in ecommerce", "ws://localhost:8000/ws")
    st.session_state.host.start_app()

# Hiển thị lại lịch sử tin nhắn
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Nhận đầu vào người dùng
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_text = st.session_state.host.chat_app(prompt)
        if response_text['data']['type'] == 'correlation_chart':
            print(type(json.loads(response_text['data']['data'])))
            df = pd.DataFrame(json.loads(response_text['data']['data']))
            df.index = df.columns
            st.markdown("### 🔍 Correlation Heatmap\nBiểu đồ sau thể hiện mức độ tương quan giữa các biến.")

            # 👉 Hiển thị heatmap
            plt.figure(figsize=(8, 6))
            sns.heatmap(df, annot=True, cmap="coolwarm", fmt=".2f")
            plt.xticks(rotation=45, ha='right')
            plt.title("Correlation Matrix")
            st.pyplot(plt)
        else:
            st.json(response_text)

    # Lưu câu trả lời vào session_state
    st.session_state.messages.append({"role": "assistant", "content": response_text})