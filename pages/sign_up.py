#모듈 호충
import streamlit as st
import pandas as pd
import moduls.email as em
import moduls.account as ac
import moduls.clocker as ck
from datetime import datetime
import time

#페이지 설정
st.set_page_config(page_title="HIRO AI", page_icon='./img/logo.png',layout="centered")

# 데이터
if 'user' not in st.session_state:
    st.session_state.user = 'not_login'

# 동의서 작성
st.write("## 개인정보수집 및 이용 동의 (필수)")
document = st.container(height=300)
with open("./document/text/license.txt", "r", encoding="utf-8") as file:
    content = file.read()
document.write(content)
agree = st.checkbox('위 내용을 모두 확인하고, HIRO AI가 상기 명시한 목적에 따라 이메일 주소를 수집·이용하는 것에 동의합니다.')

st.write("😎 HIRO AI 서비스 회원가입")
#아이디
user_id = st.text_input('아이디')
#이메일
e_mail = st.text_input('이메일 주소',key = 2)
sended = st.button('⚙️ 인증번호 전송')
if sended:
    code = ac.generate_email_key()
    with open(f"./database/email_code/{e_mail}.txt", "w", encoding="utf-8") as f:
        f.write(code)
    em.send_code_email(e_mail, code, user_id)
ac_code = st.text_input('발송 버튼을 누르신 뒤 인증번호를 입력해 주세요.')

#비밀번호
password = st.text_input('비밀번호',key = 4, type="password")
password_again = st.text_input('비밀번호 확인', type="password")


#버튼
if st.button('계정 생성'):
    try:
        able_code = True
        with open(f'./database/email_code/{e_mail}.txt', "r", encoding="utf-8") as f:
            code = f.read().strip()
    except:
        able_code = False
        st.error('😥 인증 메일을 발송해 주세요...')
    if user_id == '':
        st.error('😥 아이디를 입력해 주세요')
    elif not agree:
        st.error('😥 "개인정보수집 및 이용 동의 (필수)"에 동의해 주세요.')
    elif em.check_email(e_mail) == False:
        st.error('😥 이메일 주소를 정확히 다시 입력해 주세요.')
    elif em.copy_email(e_mail) == False:
        st.error('😥 동일한 이메일 주소가 이미 존재합니다.')
    elif password != password_again:
        st.error('😥 비밀번호가 비밀번호 확인과 다릅니다.')
    elif able_code == True and ac_code != code:
        st.error('😥 인증번호가 일치하지 않습니다.')
    else:
        if able_code == True:
            ac.make_account(user_id, e_mail, password)
            st.write('✨ 계정 생성중...')
            time.sleep(1)
            for i in range(3):
                st.write(f'✨ {3-i}초 후 로그인 페이지로 이동합니다...')
                time.sleep(1)
            st.switch_page("pages/login.py")