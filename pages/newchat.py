import streamlit as st

#페이지 설정
st.set_page_config(page_title="HIRO AI",  page_icon='./img/logo.png',layout="centered")

## 세션 스테이트
if 'check_idx' not in st.session_state:
    st.session_state.check_idx = len(st.session_state.history_name)-1

## 채팅 데이터베이스
if 'user' not in st.session_state:
    st.session_state.user = 'not_login'
if 'history_name' not in st.session_state:
    st.session_state.history_name = ['⚡새 대화1']
if 'history_chathisroty' not in st.session_state:
    st.session_state.history_chathisroty = [[{"role": "system", "content": "Your name is HIRO AI. Your company is HIRO AI."}]]
if 'history_model' not in st.session_state:
    st.session_state.history_model = ["HIRO 1"]

st.title("📌 새 채팅 - 모델 선택")
selected_model = st.selectbox("사용할 모델을 선택하세요:", ["HIRO 1 mini","HIRO 1","HIRO 2","HIRO 3o","HIRO 4o","HIRO dep1","HIRO dep2"])
if st.button("🚀 선택한 모델로 대화를 시작하기",use_container_width=True):
    st.session_state.history_model.append(selected_model)
    st.session_state.history_chathisroty.append([{"role": "system", "content": "Your name is HIRO AI. Your company is HIRO AI."}])
    st.session_state.history_name.append(f'⚡새 대화 {len(st.session_state.history_name)+1}')
    st.session_state.check_idx = len(st.session_state.history_name)-1
    st.switch_page("pages/chat.py")
st.write("HRIO 3o와 HIRO 4o는 이미지 인식이 가능합니다.")