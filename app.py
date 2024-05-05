import streamlit as st
import os
import requests
import json

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

if "questions" not in st.session_state:
    st.session_state.questions = []

if "answers" not in st.session_state:
    st.session_state.answers = []

def create_tf_serving_json(data):
    return {'messages': data}
    # return {'columns': ["messages"], "data": [[{"messages": data}]]}

def score_model(dataset):
    headers = {'Authorization': f'Bearer {os.environ.get("DATABRICKS_API_TOKEN")}',
               'Content-Type': 'application/json'}
    # ds_dict = {"dataframe_split": create_tf_serving_json(dataset)}
    ds_dict = create_tf_serving_json(dataset)
    data_json = json.dumps(ds_dict, allow_nan=True)
    response = requests.request(
        method='POST', headers=headers, url=os.environ.get("DATABRICKS_API_URL"), data=data_json)
    if response.status_code != 200:
        # print(response.text)
        raise Exception(
            f'Request failed with status {response.status_code}, {"Refresh our Application and try again"}')
    return response.json()

def render_sources(sources):
    with st.expander(label="Sources"):
        for s in sources:
            st.markdown(s)

def write_answer_with_source(result):
    with st.chat_message("assistant"):
        st.write(result['answer'])
        if 'source' in result:
            render_sources(result['source'])
        else:
            render_sources([])

def write_question(question):
    with st.chat_message("user"):
        st.write(question)

st.set_page_config(
    page_title="Zero to generative AI",
    page_icon=":rocket:"
)

# Title UI
st.title(":rocket: Zero to generative AI")
st.write("Demo chatbot application. To learn more, see [aws-samples/aws-genai-for-databricks](https://github.com/aws-samples/aws-genai-for-databricks)")

# Configuration UI
with st.expander(label="⚙️ Configuration", expanded=True):
    os.environ['DATABRICKS_API_TOKEN'] = st.text_input(
        "Enter your Databricks personal access token", key="DATABRICKS_API_TOKEN", placeholder="dapiXXXXXXXXXXXXXX")
    os.environ['DATABRICKS_API_URL'] = st.text_input(
        "Enter your Databricks model endpoint URL", key="DATABRICKS_API_URL", placeholder="https://XXXXX.cloud.databricks.com/serving-endpoints/serving-endpoints/catalog_XXXXX_default_endpoint/invocations")

st.divider()

# Chat messages UI
number_of_questions = len(st.session_state.questions)

for i in range(number_of_questions):
    write_question(st.session_state.questions[i])
    write_answer_with_source(st.session_state.answers[i]) 

# Chat input UI
with st.spinner("Loading..."):
    if question := st.chat_input("Type something here..."):
        try:
            # Append question to chat history
            st.session_state.chat_history.append({"role": "user", "content": question})
            print(st.session_state.chat_history)
            # Call model
            response = score_model(st.session_state.chat_history)
            answer = response[0]['result']
            source = response[0]['sources']
            # Append to the session state
            answer_with_source = {"answer": answer, "source": source}
            st.session_state.questions.append(question)
            st.session_state.answers.append(answer_with_source)
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
            # Render answers to UI
            write_question(question)
            write_answer_with_source(answer_with_source)
        except Exception as e:
            st.error("Error: Please check your databricks credentials and model endpoint URL.", icon="🚨")
            # print(e)