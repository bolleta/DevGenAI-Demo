import uuid

import boto3
import streamlit as st

USER = "user"
ASSISTANT = "assistant"

# Agentの定義
agent_id: str = "XXXXXXXXXX"  # Agent IDを入力
agent_alias_id: str = "XXXXXXXXXX"  # Alias IDを入力

session_id: str = str(uuid.uuid1())
client = boto3.client("bedrock-agent-runtime")

# チャット履歴保存用のセッションを初期化
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []

# タイトル設定
st.title("Agents for Amazon Bedrok チャット")

if prompt := st.chat_input("質問を入力してください。"):
    # 以前のチャットログを表示
    for chat in st.session_state.chat_log:
        with st.chat_message(chat["name"]):
            st.write(chat["msg"])
    
    with st.chat_message(USER):
        st.markdown(prompt)

    with st.chat_message(ASSISTANT):
        # Agentの実行
        response = client.invoke_agent(
            inputText=prompt,
            agentId=agent_id,
            agentAliasId=agent_alias_id,
            sessionId=session_id,
            enableTrace=False,
        )

        # Agent 実行結果の取得と表示
        #（ストリームを処理しているようなコードだが、実際はストリームのように細切れでレスポンスは返ってきていない。
        # https://repost.aws/questions/QU_jIzfKIAQHSXyPeE4JMAJg/issue-streaming-response-from-bedrock-agent
        event_stream = response["completion"]
        assistant_msg = "" 
        for event in event_stream:
            if "chunk" in event:
                assistant_msg += event["chunk"]["bytes"].decode("utf-8")
        st.write(assistant_msg)
    
    # セッションにチャットログを追加
    st.session_state.chat_log.append({"name": USER, "msg": prompt})
    st.session_state.chat_log.append({"name": ASSISTANT, "msg": assistant_msg})
