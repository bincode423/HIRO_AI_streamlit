#모듈 호충
import streamlit as st
import pandas as pd
import moduls.email as em
import moduls.account as ac

#페이지 설정
st.set_page_config(page_title="HIRO AI", page_icon='./img/logo.png',layout="centered")

# 데이터
if 'user' not in st.session_state:
    st.session_state.user_name = 'not_login'

# 소개 문구
st.write('## 📝 로그인하여 더 많은 기능을 이용하세요!')

# 입력란
e_mail = st.text_input('이메일 주소',key = 1)
password = st.text_input('비밀번호',key = 3, type="password")
st.markdown('---')

# 버튼
if st.button('로그인', use_container_width=True):
    if not em.copy_email(e_mail):
        if False:
            st.session_state.user = 'login'
            st.success('로그인 성공')
        else:
            st.error('비밀번호가 일치하지 않습니다.')
    else:
        st.error('이메일 주소를 찾을 수 없습니다.')
if st.button('이곳을 눌러 회원가입', use_container_width=True):
    st.switch_page("pages/sign_up.py")