import streamlit as st
import openai
import requests

openai.api_key = st.secrets["api_key"]

st.title("Make your own Image using ChatGPT Plus DALL-E")

with st.form("form"):
    user_input = st.text_input("Prompt")
    size = st.selectbox("Size", ["1024x1024", "512x512", "256x256"])
    submit = st.form_submit_button("Submit")

if submit and user_input:
    gpt_prompt = [{
        "role": "system",
        "content": "Imagine the detail appeareance of the input. Response it shortly around 20 words"
    }]

    gpt_prompt.append({
        "role": "user",
        "content": user_input
    })

    with st.spinner("Waiting for ChatGPT..."):
        gpt_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=gpt_prompt
        )

    prompt = gpt_response["choices"][0]["message"]["content"]
    st.write(prompt)

    with st.spinner("Waiting for DALL-E..."):
        dalle_response = openai.Image.create(
            prompt=prompt,
            size=size
        )

    # 생성된 이미지 URL을 세션 상태에 저장
    st.session_state.image_url = dalle_response["data"][0]["url"]

# 이미지를 표시. 이미 생성된 이미지가 있는 경우 세션 상태에서 가져와 표시
if 'image_url' in st.session_state:
    st.image(st.session_state.image_url)

# 사용자에게 앨범 정보를 입력받습니다.
atitle = st.text_input("앨범 제목")
atype_options = ["App", "Card", "Web"]
atype = st.radio("앨범 유형 선택", atype_options)
anote = st.text_input("앨범 설명")
save_button = st.button("장고에 저장")

if save_button:
    django_api_endpoint = "http://backend-svc:8080/api/album_insert/"
    response = requests.post(django_api_endpoint, data={
        "a_title": atitle,
        "a_type": atype,
        "a_note": anote,
        "ufile": st.session_state.image_url
    })

    if response.json().get("success"):
        st.success(response.json().get("message"))
    else:
        st.error("이미지 저장에 실패했습니다.")
