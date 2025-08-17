import streamlit as st
import graphviz
from collections import deque
from ollama import chat
import ollama
from graphviz import Source
import uuid, os

## change_beta_save
user_name = '빈승현'

#페이지 설정
st.set_page_config(page_title="HIRO AI",  page_icon='./img/logo.png',layout="wide")

if 'grap' not in st.session_state:
    st.session_state.grap = graphviz.Digraph()
if 'gp_arr' not in st.session_state:
    st.session_state.gp_arr = []


#메인 마인드맵
st.write("## 💡 HIRO 마인더리")
if st.session_state.gp_arr == []:
    shapes = {'🌳 나무 형태':'dot',"🍩 둥근 형태":'fdp'}
    start_txt = st.text_area('👉 마인드맵 중심 텍스트를 입력해 주세요.')
    option = st.selectbox("⚡ 어떤 모양의 마인드맵을 원하시나요?",("🌳 나무 형태", "🍩 둥근 형태"))
    
    if st.button("마인드맵 생성하기"):
        st.toast('➕ 마인드맵을 생성하고 있습니다.')
        st.session_state.gp_arr.append(start_txt)
        st.session_state.grap = graphviz.Digraph(engine=shapes[option])
        prompt = 'When I give you a keyword, return exactly 4 to 5 unique sub-keywords related to it, separated by spaces. Do not include any explanations or extra text. Match the language of the input keyword.'
        stream = chat(model="exaone3.5:7.8b",messages= [{"role": "system", "content": prompt},{"role": "user", "content": start_txt}],stream=True)
        rt = ''
        for chunk in stream:
            rt += chunk.message.content
        new_keyword = list(set(rt.split()))
        cnt = 0
        st.session_state.grap.node(start_txt,label=start_txt, style="filled",fontname="NanumGothic", fillcolor="#ffffff", color="#000000",penwidth='1')
        for new_key in new_keyword:
            if cnt >= 5:
                break
            if new_key == start_txt:
                continue
            st.session_state.grap.node(new_key,label=new_key, style="filled",fontname="NanumGothic", fillcolor="#ffffff", color="#000000",penwidth='1')
            st.session_state.grap.edge(start_txt, new_key)
            st.session_state.gp_arr.append(new_key)
            cnt += 1
        st.rerun()
else:
    ## 디자인
    st.graphviz_chart(st.session_state.grap)
    col1, col2 = st.columns([1,1])
    with col1:
        st.write('#### 🗂️ 마인드맵 생성하기')
        key_ch = st.selectbox('🗂️ 키워드 목록',st.session_state.gp_arr, key = 1)
        option = st.text_area("➕ 이어나갈 키워드를 입력 또는 선택해 주세요.",key_ch)
        ct = st.button('✨ 생성하기',use_container_width=True)
        st.write('#### ⚙️ 전체 색상 설정하기')
        c1, c2, c3 = st.columns([1,1,1])
        with c1:
            bg_fill = st.color_picker("배경 채우기 색상", "#ffffff")
        with c2:
            node_fill = st.color_picker("키워드 채우기 색상", "#ffffff")
        with c3:
            teduri_fill = st.color_picker("키워드 테두리 색상", "#000000")
        bg_c = st.button('✨ 배경 설정 적용하기',use_container_width=True)
    with col2:
        st.write('#### 🧩 키워드 색 바꾸기 (키워드 단일 선택)')
        key_ch_c = st.selectbox('🗂️ 키워드 목록',st.session_state.gp_arr,key = 2)
        option_c = st.text_area("➕ 색상을 변경할 키워드를 입력하시거나 선택해 주세요.",key_ch_c)
        nc1, nc2 = st.columns([1,1])
        with nc1:
            fill = st.color_picker("채우기 색상", "#ffffff")
        with nc2:
            teduri = st.color_picker("테두리 색상", "#000000")
        line_w = st.slider('테두리 두께', 1.0, 5.0, 1.0, 0.1)
        ch_bt = st.button('✨ 변경사항 적용하기',use_container_width=True)
    if ct:
        if option not in st.session_state.gp_arr:
           st.toast('😥 존재하지 않는 키워드 입니다.')
        else:
            st.toast('➕ 마인드맵을 생성하고 있습니다.')
            prompt = 'When I give you a keyword, return exactly 4 to 5 unique sub-keywords related to it, separated by spaces. Do not include any explanations or extra text. Match the language of the input keyword.'
            stream = chat(model="exaone3.5:7.8b",messages= [{"role": "system", "content": prompt},{"role": "user", "content": option}],stream=True)
            rt = ''
            for chunk in stream:
                rt += chunk.message.content
            new_keyword = list(set(rt.split()))
            cnt = 0
            for new_key in new_keyword:
                if new_key == option:
                    continue
                if cnt >= 5:
                    break
                st.session_state.grap.node(new_key,label=new_key, style="filled",fontname="NanumGothic", fillcolor="#ffffff", color="#000000",penwidth=str(line_w))
                st.session_state.grap.edge(option, new_key)
                st.session_state.gp_arr.append(new_key)
                cnt += 1
            st.rerun()
    if ch_bt:
        if option_c not in st.session_state.gp_arr:
           st.toast('😥 존재하지 않는 키워드 입니다.')
        else:
            st.session_state.grap.node(option_c,label=option_c, style="filled",fontname="NanumGothic", fillcolor=fill, color=teduri,penwidth=str(line_w))
            st.toast('🧩 색상이 변경되었습니다.')
            st.rerun()
    if bg_c:
        st.session_state.grap.graph_attr['bgcolor'] = bg_fill
        for node in st.session_state.gp_arr:
            st.session_state.grap.node(node,label=node, style="filled",fontname="NanumGothic", fillcolor=node_fill, color=teduri_fill)
        st.toast('🧩 전체 색상이 변경되었습니다.')
        st.rerun()
    
    ## 다운로드
    unique_id = str(uuid.uuid4())[:8]
    filepath = f"download/graph_{unique_id}.png"
    st.session_state.grap.render(filepath[:-4], format="png", cleanup=True)
    with open(filepath, "rb") as f:
        img_bytes = f.read()
    st.download_button(
        label="📥 다운로드",
        data=img_bytes,
        file_name="graph.HIRO.png",
        mime="image/png",
        use_container_width=True
    )

