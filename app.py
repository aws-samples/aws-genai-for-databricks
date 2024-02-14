import streamlit as st
import boto3
import os
import requests
import json

USER_ICON = "images/user-icon.png"
AI_ICON = "images/ai-icon.png"

# HARDCODED RESPONSE

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

if "questions" not in st.session_state:
    st.session_state.questions = []

if "answers" not in st.session_state:
    st.session_state.answers = []

if "input" not in st.session_state:
    st.session_state.input = ""

if "files" not in st.session_state:
    st.session_state.files = []


def handle_input():
    formatted_user_input = {"role": "user", "content": st.session_state.input}
    st.session_state.chat_history.append(formatted_user_input)
    # print(st.session_state.chat_history)
    response = score_model(
        st.session_state.chat_history)
    model_prediction = response['predictions'][0]['result']
    model_sources = response['predictions'][0]['sources']
    # Append to the model answers
    st.session_state.questions.append(st.session_state.input)
    st.session_state.answers.append(
        {"source": model_sources, "answer": model_prediction})
    st.session_state.chat_history.append(
        {"role": "assistant", "content": model_prediction})
    # Reset the input field
    st.session_state.input = ""


def create_tf_serving_json(data):
    return {'columns': ["messages"], "data": [[{"messages": data}]]}


def score_model(dataset):
    headers = {'Authorization': f'Bearer {os.environ.get("DATABRICKS_API_TOKEN")}',
               'Content-Type': 'application/json'}
    ds_dict = {"dataframe_split": create_tf_serving_json(dataset)}
    data_json = json.dumps(ds_dict, allow_nan=True)
    response = requests.request(
        method='POST', headers=headers, url=os.environ.get("DATABRICKS_API_URL"), data=data_json)
    if response.status_code != 200:
        raise Exception(
            f'Request failed with status {response.status_code}, {"Refresh our Application and try again"}')
    return response.json()


def render_answer(answer):
    col1, col2 = st.columns([1, 12])
    with col1:
        st.image(AI_ICON, use_column_width='always')
    with col2:
        st.info(answer)


def render_sources(sources):
    col1, col2 = st.columns([1, 12])
    with col2:
        with st.expander("Sources"):
            for s in sources:
                st.write(s)


def render_result(result):
    answer, sources = st.tabs(['Answer', 'Sources'])
    with answer:
        render_answer(result['answer'])
    with sources:
        if 'source_documents' in result:
            render_sources(result['source_documents'])
        else:
            render_sources([])


def write_chat_message(answer):
    chat = st.container()
    with chat:
        render_answer(answer['answer'])
        render_sources(answer['source'])


def write_user_message(md):
    col1, col2 = st.columns([1, 12])
    with col1:
        st.image(USER_ICON, use_column_width='always')
    with col2:
        st.warning(md)


with st.container():
    st.write("""
         # AWS RAG Application with Databricks Model Serving      
         """)
st.markdown('-----')

with st.container():
    st.write("""
             ## Application Configuration """)
    os.environ['DATABRICKS_API_TOKEN'] = st.text_input(
        "Enter your credentials for Databricks", placeholder="e.g dapic07e3213c321890da328931434ce3a6a")
    os.environ['DATABRICKS_API_URL'] = st.text_input(
        "Enter your Databricks model endpoint URL", placeholder="e.g https://dbc-32131dadsfd.cloud.databricks.com/serving-endpoints/dare_amazon_rag_endpoint/invocations'")

st.markdown('-----')
st.write("""
         ## Test out your Databricks LLM""")
with st.form('my_form'):
    input_text = st.text_input("You are talking to your Databricks LLM, ask any question.",
                               key="input", placeholder="Ask a question")
    submit_button = st.form_submit_button(
        label='Submit', on_click=handle_input)
st.markdown('-----')

with st.container():
    num_questions_asked = len(st.session_state.answers)
    for i in range(num_questions_asked):
        write_user_message(
            st.session_state.questions[num_questions_asked - i - 1])
        write_chat_message(
            st.session_state.answers[num_questions_asked - i - 1])
