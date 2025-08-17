import streamlit as st

## 채팅 데이터베이스
if 'history_name' not in st.session_state:
    st.session_state.history_name = ['⚡새 대화1']
if 'history_chathisroty' not in st.session_state:
    st.session_state.history_chathisroty = [[{"role": "system", "content": "Your name is HIRO AI. Your company is HIRO AI. "}]]
if 'history_model' not in st.session_state:
    st.session_state.history_model = ["HIRO 1"]
if 'check_idx' not in st.session_state:
    st.session_state.check_idx = len(st.session_state.history_name)-1
if 'generate' not in st.session_state:
    st.session_state.generate = False
if 'database' not in st.session_state:
    st.session_state.database = ['사용자는 개발자가 되고 싶다.','사용자는 개를 키우고 있다.']
if 'user' not in st.session_state:
    st.session_state.user = 'login'

#로그인 또는 이름
if st.session_state.user == 'not_login':
    pg = {
        '🎈 사용자':[st.Page("pages/login.py", title="로그인"),st.Page("pages/sign_up.py", title="회원가입")],
        '🛠️ AI 도구들':[st.Page("pages/mindmap.py", title="HIRO 마인더리"),st.Page("pages/writeai.py", title="보고서 작성")],
        '🔥 채팅': [st.Page("pages/chat.py", title="최근 채팅 기록"),st.Page("pages/newchat.py", title="새 채팅")]
    }
else:
    pg = {
        '🎈 사용자':[st.Page("pages/user.py", title="사용자 설정")],
        '🛠️ AI 도구들':[st.Page("pages/mindmap.py", title="HIRO 마인더리"),st.Page("pages/writeai.py", title="보고서 작성")],
        '🔥 채팅': [st.Page("pages/chat.py", title="최근 채팅 기록"),st.Page("pages/newchat.py", title="새 채팅")]
    }
pg = st.navigation(pg)
pg.run()

## 기록보여주기
st.sidebar.title("Chat History")
for i, name in enumerate(st.session_state.history_name):
    if st.sidebar.button(name, type="tertiary"):
        st.session_state.check_idx = i
        st.switch_page("pages/chat.py")