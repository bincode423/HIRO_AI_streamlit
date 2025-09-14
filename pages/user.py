#모듈 호충
import streamlit as st
import pandas as pd

st.write('### 🔖 메모리 설정')
if 'database' not in st.session_state:
    st.session_state.database = ['사용자는 개발자가 되고 싶다.','사용자는 개를 키우고 있다.']

st.write('### 메모리 목록')
df = pd.DataFrame(st.session_state.database, columns=['메모리 목록'])
st.dataframe(df.reset_index(drop=True), hide_index=True)
st.text_area('삭제할 메모리 번호')
st.button('메모리 삭제',use_container_width=True)
st.button('메모리 전체 삭제',use_container_width=True)
