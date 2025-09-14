#모듈 가져오기
import streamlit as st
from streamlit_ace import st_ace
import subprocess
import base64
from ollama import chat
import ollama
from streamlit_ace import st_ace

## change_beta_save
user_name = '빈승현'

#페이지 설정
st.set_page_config(page_title="HIRO AI", page_icon='./img/logo.png',layout="wide")

## 사용자 데이터베이스
if 'user' not in st.session_state:
    st.session_state.user = 'not_login'

## 코딩 데이터베이스
if 'code_data_save' not in st.session_state:
    st.session_state.code_data_save = ''
if 'code_chat' not in st.session_state:
    st.session_state.code_chat = [{"role": "system","content": "너의 이름은 HIRO AI Coder이고, 개발자는 HIRO AI Researcher야. 회사 이름은 HIRO AI야.\n너는 사용자와 코딩 관련 대화를 하고, 코드를 작성할 때는 반드시 마지막에 한 번에 모두 작성해야 해.\nProtok은 'prompt'와 'token'의 합성어야.\n그리고 코드를 작성할 때는 파이썬 코드 블록 표시(```)를 시작과 끝에 한 번씩만 사용해야 해. 그 이유는 내가 그것밖에 인식하지 못하기 때문이야.\n단, 코드 블록 밖에서는 자유롭게 설명해도 돼."}]
if 'imsi_code_id_change' not in st.session_state:
    st.session_state.imsi_code_id_change = 'khkjshgoahsgoi'

#창 분활
col1, col2 = st.columns([5, 2])

# --- AI Copilot 영역 ---
with col2:
    st.header("✨ HIRO Canvas")
    messages_UI = st.container(height=700)
    for dic_chat in st.session_state.code_chat:
        if dic_chat['role'] == 'user':
            messages_UI.write(f"### 🎈 사용자")
            messages_UI.markdown(dic_chat['content'])
            messages_UI.markdown("---")
        elif dic_chat['role'] == 'assistant':
            messages_UI.image('./img/logo.png',width=35)
            messages_UI.write('')
            messages_UI.markdown(dic_chat['content'])
            messages_UI.markdown("---")
    
    
    prompt = st.chat_input("무엇이든 물어보세요.")
    
    if prompt:
        if st.session_state.generate == True:
            st.toast('답변을 정지하였습니다.')
            st.session_state.generate = False
        else:
            st.session_state.generate = True
            prompt = f'```python\n{st.session_state.code_data_save}\n```\n'+prompt
            st.session_state.code_chat.append({'role': 'user', 'content': prompt})
            
            #사용자 질문 보여주기
            messages_UI.write(f"### 🎈 사용자")
            messages_UI.markdown(prompt)
            messages_UI.markdown("---")
            
            # AI로고
            messages_UI.image('./img/logo.png',width=35)
            messages_UI.write('')
            
            # 응답 생성
            placeholder_response = messages_UI.empty()
            messages_UI.markdown("---")
            response_text = ""
            is_coding = False
            is_python_world = 0
            
            # 첫 번쨰 응답까지 모델 로딩 보여주기
            with st.spinner("⚡모델을 불러오고 있습니다"):
                stream = chat(
                    model="exaone3.5:7.8b",
                    messages= st.session_state.code_chat,
                    stream=True
                )
                for chunk in stream:
                    response_text += chunk.message.content
                    if '```' in chunk.message.content:
                        is_coding = True
                        is_python_world = 2
                        st.session_state.code_data_save = ''
                        st.toast('AI가 코드를 작성 중입니다!', icon='🧑‍💻')
                    break
            
            #메인 모델 코드
            for chunk in stream:
                if '```' in chunk.message.content:
                    if is_coding == False:
                        is_coding = True
                        is_python_world = 2
                        st.session_state.code_data_save = ''
                        st.toast('AI가 코드를 작성 중입니다!', icon='🧑‍💻')
                        continue
                    else:
                        is_coding = False
                        continue
                
                if is_coding == False:
                    response_text += chunk.message.content
                    placeholder_response.markdown(f"<span style='font-size:16px'>{response_text}</span>", unsafe_allow_html=True)
                if is_coding == True:
                    if is_python_world > 0:
                        is_python_world -= 1
                        continue
                    st.session_state.code_data_save += chunk.message.content
            
            # AI의 응답을 대화 기록에 추가
            st.session_state.code_chat.append({'role':'assistant','content':response_text})
            
            st.session_state.generate = False
            if st.session_state.imsi_code_id_change == 'khkjshgoahsgoi':
                st.session_state.imsi_code_id_change = 'hogkaojgolksjg'
            else:
                st.session_state.imsi_code_id_change = 'khkjshgoahsgoi'

# --- IDE 영역 ---
with col1:
    ## ide
    st.header("IDE (🍫파이썬만 지원)")
    code = st_ace(value=st.session_state.code_data_save, language="python", theme='dracula', height=500, font_size=16,key=st.session_state.imsi_code_id_change)
    
    
    #ide 실행
    input_col, output_col = st.columns(2)
    with input_col:
        st.subheader("입력값 🧾")
        user_input = st.text_area("아래에 입력값을 작성하세요", height=120, label_visibility="collapsed")
    with output_col:
        st.subheader("출력 결과 📤")
        output_placeholder = st.empty()
    
    # 자동 실행 (Apply 또는 Ctrl+Enter)
    if code:
        # 저장하기
        st.session_state.code_data_save = code
        
        full_code = f"""
_input = '''{user_input}'''
def input(prompt=None):
    if prompt:
        print(prompt)
    return _input

{code}
"""
        try:
            result = subprocess.run(
                ["python3", "-c", full_code],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                output_placeholder.success("🔥 실행 성공!")
                output_placeholder.code(result.stdout)
            else:
                output_placeholder.error("❌ 오류 발생!")
                output_placeholder.code(result.stderr)
        except subprocess.TimeoutExpired:
            output_placeholder.error("⏰ 실행 시간 초과!")