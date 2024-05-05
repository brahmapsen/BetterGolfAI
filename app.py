import streamlit as st
import os
from dotenv import load_dotenv
import requests

load_dotenv()

twelve_labs_key = os.getenv('TWELVELABS_API_KEY')

headers = { "accept": "application/json", 
            "x-api-key": twelve_labs_key, 
            "Content-Type": "application/json"
          }
indexUrl =  'https://api.twelvelabs.io/v1.2/indexes?page=1&page_limit=10&sort_by=created_at&sort_option=desc'

def get_indexes():
  response = requests.get(indexUrl,  headers=headers)
  return response.json()

def get_videos(index_id):
  url = (
    f'https://api.twelvelabs.io/v1.2/indexes/{index_id}/videos?page=1&page_limit=10&sort_by=created_at&sort_option=desc'
    )
  response = requests.get(url,  headers=headers)
  return response.json()

def getSummary(prompt):
  url = "https://api.twelvelabs.io/v1.2/generate"

  payload = {
      "video_id": st.session_state["video_id"],
      "prompt": prompt
  }
  response = requests.post(url, json=payload, headers=headers)
  return response.json()

def index_video(video_url,twelve_labs_key):
    return response.json()

def create_index(index_name, twelve_labs_key):
    return response.json()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
# Sidebar section
st.sidebar.title("Better Swing")

index_ids = []
indexes = get_indexes().get("data")
for index in indexes:
  index_ids.append(index['_id'])

if len(index_ids) > 0:
  option = st.sidebar.selectbox(
  "Select an index:",
  index_ids,
  placeholder="Select index method...",
  )
  st.session_state["index_id"] = option

  result = get_videos(st.session_state["index_id"])
  data = result['data']
  if data:
    v_id = []
    for d in data:
        v_id.append(d["metadata"]["filename"]+"-"+d["_id"])
    option = st.sidebar.selectbox(
                "Select an video:",
                v_id,
                placeholder="Select video...",
                )
    st.session_state["video_id"] = option.split("-")[-1]
    st.sidebar.write("id : " + st.session_state["video_id"])

if prompt := st.chat_input("Ask any thing on the video"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
      st.markdown(prompt)

    with st.chat_message("assistant"):
      response = getSummary(prompt)
      st.markdown(response.get("data"))

      st.session_state.messages.append(
          {"role": "assistant", "content": response.get("data")}
      )

if st.sidebar.button("Clear Chats", type="primary"):
    st.session_state.messages = []
    st.session_state["video_id"] = ""
    st.session_state["index_id"] = ""