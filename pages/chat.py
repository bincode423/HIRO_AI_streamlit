import streamlit as st
from ollama import chat
import ollama
import base64
from time import sleep
import json
import random
import pandas as pd
import pickle

## change_beta_save
user_name = 'HIRO'

## set site
st.set_page_config(page_title="HIRO AI",  page_icon='./img/logo.png',layout="centered")

## 세션 스테이트
if 'user' not in st.session_state:
    st.session_state.user = 'not_login'
if 'generating' not in st.session_state:
    st.session_state.generating = False
if 'check_idx' not in st.session_state:
    st.session_state.check_idx = len(st.session_state.history_name)-1

## 채팅 데이터베이스
if 'history_name' not in st.session_state:
    st.session_state.history_name = ['⚡새 대화1']
if 'history_chathisroty' not in st.session_state:
    st.session_state.history_chathisroty = [[{"role": "system", "content": "Your name is HIRO AI. Your company is HIRO AI. "}]]
if 'history_model' not in st.session_state:
    st.session_state.history_model = ["HIRO 1 mini"]
if 'database' not in st.session_state:
    st.session_state.database = []

# 전체 대화 기록 출력
if st.session_state.history_chathisroty[st.session_state.check_idx]:
    for message in st.session_state.history_chathisroty[st.session_state.check_idx]:
        if message['role'] == 'user':
            st.write(f"### 🍫 사용자")
            st.write(message['content'])
            st.markdown("---")
        elif message['role'] == 'assistant':
            st.image('./img/logo.png',width=35)
            st.write('')
            if st.session_state.history_model[st.session_state.check_idx] in ['HIRO 1','HIRO 1 mini','HIRO 2','HIRO 3o','HIRO 4o','HIRO dep2']:
                st.write(message['content'])
            elif st.session_state.history_model[st.session_state.check_idx] == 'HIRO dep1':
                t, r = message['content'].split('<THINK_Bar_Space_Id>')
                t = t.lstrip("<think>")
                t = t.rstrip("</think>")
                with st.popover("⚡생각중..."): st.write(t)
                st.write(r)
            st.markdown(f":violet-badge[⚡{st.session_state.history_model[st.session_state.check_idx]}]")
            st.markdown("---")

#메인 페이지
#HIRO1 mini -> gemma3:1b   o
#HIRO1 -> gemma:2b         
#HIRO2 -> exaone3.5:7.8b   o
#HIRO 3o -> gemma3:4b       o
#HIRO 4o -> gemma3:12b      o
#HIRO dep1                  o
#HIRO dep2                  o
if st.session_state.history_model[st.session_state.check_idx] == 'HIRO 3o' or st.session_state.history_model[st.session_state.check_idx] == 'HIRO 4o':
    prompt = st.chat_input("무엇이든 물어보세요.",accept_file=True,file_type=["jpg", "jpeg", "png"])
else:
    prompt = st.chat_input("무엇이든 물어보세요.")

if prompt and prompt != '':
    if st.session_state.generating == True:
        st.toast('답변을 정지하였습니다.')
        st.session_state.generating = False
    else:
        # 답변 설정
        st.session_state.generating = True
        
        # 대화 기록에 사용자 입력 추가
        st.session_state.history_chathisroty[st.session_state.check_idx].append({'role': 'user', 'content': prompt})
        
        # 사용자 입력추가
        st.write(f"### 🍫 사용자")
        if st.session_state.history_model[st.session_state.check_idx] in ['HIRO 3o','HIRO 4o']:
            if prompt["files"]:
                st.image(prompt["files"][0],width=100)
        st.write(prompt)
        st.markdown("---")

        # AI로고
        st.image('./img/logo.png',width=35)
        st.write('')
        
        # 환경 설정
        with st.spinner("📝 모델을 불러오고 있습니다"):
            ## 제목 생성
            if len(st.session_state.history_chathisroty[st.session_state.check_idx]) == 2:
                stream = chat(model="exaone3.5:7.8b",
                            messages= [{"role": "system", "content": "너는 사용자의 질문을 기반으로 3글자 이상 5단어 이하로 질문에 제목을 생성해야해. 제목만 생성해서 줘야 해."},{"role": "user", "content": prompt}],stream=True)
                title = '👉 '
                for chunk in stream:
                    title += chunk.message.content
                st.session_state.history_name[st.session_state.check_idx] = title
                
            ## 사용자 정보
            stream = chat(model="exaone3.5:7.8b",
                        messages= [{"role": "system", "content": "너는 사용자가 기억해 달라는 것 또는 꼭 기억해야 하는 것(사용자에 학교, 가족관계, 직업 등)만 한국어로 짧게 알려줘야 해(최대 20글자, 예(질문 : 나는 개발자가 되고 싶어 ,정리: 사용자는 개발자가 되기를 원한다.)). 만약에 꼭 필요하지 않거나, 기억해야 할 만한 것이 없으면 그냥 'Nothing here'만 반환해"},{"role": "user", "content": prompt}],stream=True)
            dater = ''
            for chunk in stream:
                dater += chunk.message.content
            if dater.strip() != 'Nothing here':
                st.session_state.database.append(dater)
                with st.popover("🔖 저장된 메모리 업데이트됨"):
                    st.info(f"'{dater}'가 추가됨", icon="ℹ️")
                    df = pd.DataFrame(st.session_state.database, columns=['메모리 목록'])
                    st.write('### 메모리 목록')
                    st.dataframe(df.reset_index(drop=True), hide_index=True)
        
        
        
        
        #모델별로 다른 응답 생성
        if st.session_state.history_model[st.session_state.check_idx] in ['HIRO 1','HIRO 1 mini','HIRO 2']:
            placeholder_response = st.empty()
            response_text = ""  
            model = {
                'HIRO 1': 'gemma:2b',
                'HIRO 1 mini': 'gemma3:1b',
                'HIRO 2': 'exaone3.5:7.8b'
            }
            with st.spinner("✨ 응답 생성을 대기하고 있습니다"):    
                ## 응답 생성
                stream = chat(
                    model=model[st.session_state.history_model[st.session_state.check_idx]],
                    messages= st.session_state.history_chathisroty[st.session_state.check_idx],
                    stream=True
                )
                for chunk in stream:
                    response_text += chunk.message.content
                    break
            for chunk in stream:
                response_text += chunk.message.content
                placeholder_response.markdown(f"<span style='font-size:16px'>{response_text}</span>", unsafe_allow_html=True)
            st.session_state.history_chathisroty[st.session_state.check_idx].append({'role': 'assistant', 'content': response_text})
        
        elif st.session_state.history_model[st.session_state.check_idx] in ['HIRO 3o','HIRO 4o']:
            placeholder_response = st.empty()
            response_text = ""  
            model = {
                'HIRO 3o': 'gemma3:4b',
                'HIRO 4o': 'gemma3:12b'
            }
            with st.spinner("✨ 응답 생성을 대기하고 있습니다"):    
                ## 응답 생성
                if prompt and prompt["files"]:
                    stream = chat(
                        model=model[st.session_state.history_model[st.session_state.check_idx]],
                        messages= st.session_state.history_chathisroty[st.session_state.check_idx],
                        image=prompt["files"][0],
                        stream=True
                    )
                else:
                    image = None
                    stream = chat(
                        model=model[st.session_state.history_model[st.session_state.check_idx]],
                        messages= st.session_state.history_chathisroty[st.session_state.check_idx],
                        stream=True
                    )
                for chunk in stream:
                    response_text += chunk.message.content
                    break
            for chunk in stream:
                response_text += chunk.message.content
                placeholder_response.markdown(f"<span style='font-size:16px'>{response_text}</span>", unsafe_allow_html=True)
            st.session_state.history_chathisroty[st.session_state.check_idx].append({'role': 'assistant', 'content': response_text})
        
        
        
        
        
        
        
        #####################################################################################   
        elif st.session_state.history_model[st.session_state.check_idx] == 'HIRO dep1':
            with st.spinner("✨ 응답 생성을 대기하고 있습니다"):
                stream = chat(
                    model="DeepSeek-R1",
                    messages= st.session_state.history_chathisroty[st.session_state.check_idx],
                    stream=True
                )
                with st.popover("⚡생각중..."):
                    placeholder_think = st.empty()
                placeholder_response = st.empty()
                think_text = ""
                thinking_now = True
                response_text = ""
                for chunk in stream:
                    think_text += chunk.message.content
                    if '</think>' in think_text:
                        thinking_now = False
                    break
            for chunk in stream:
                if thinking_now == False:
                    response_text += chunk.message.content
                    placeholder_response.markdown(f"<span style='font-size:16px'>{response_text}</span>", unsafe_allow_html=True)
                else:
                    think_text += chunk.message.content
                    placeholder_think.markdown(f"<span style='font-size:16px;'>{think_text}</span>", unsafe_allow_html=True)
                    if '</think>' in think_text:
                        thinking_now = False
            
            # AI의 응답을 대화 기록에 추가
            st.session_state.history_chathisroty[st.session_state.check_idx].append({'role': 'assistant', 'content': think_text+'<THINK_Bar_Space_Id>'+response_text})
        
        
        
        
        
        
        
        #####################################################################################   
        elif st.session_state.history_model[st.session_state.check_idx] == "HIRO dep2":
            ## --토대 마련--
            with st.popover("⚡응답을 생성 중 입니다..."):
                placeholder_tree = st.empty()
            tree = ''
            stream = chat(model="exaone3.5:7.8b",messages= st.session_state.history_chathisroty[st.session_state.check_idx],stream=True)
            for chunk in stream:
                tree += chunk.message.content
                placeholder_tree.markdown(f"<span style='font-size:16px;'>{tree}</span>", unsafe_allow_html=True)
            
            # --보완하기--
            with st.popover("📝 응답의 보완점을 찾고 있습니다..."):
                placeholder_rerun = st.empty()
            rerun = ''
            st.session_state.history_chathisroty[st.session_state.check_idx].append({'role': 'user', 'content':f'"{tree}"이것은 사용자가 {prompt}이라 했을 때에 답변인데, 수정해야할 부분만 알려줘!'})
            stream = chat(model="exaone3.5:7.8b",
                          messages= st.session_state.history_chathisroty[st.session_state.check_idx]
                          ,stream=True)
            for chunk in stream:
                rerun += chunk.message.content
                placeholder_rerun.markdown(f"<span style='font-size:16px;'>{rerun}</span>", unsafe_allow_html=True)
            st.session_state.history_chathisroty[st.session_state.check_idx].pop()
            
            #--완성하기--
            placeholder_answer = st.empty()
            answer = ''
            st.session_state.history_chathisroty[st.session_state.check_idx].append({'role': 'user', 'content':f'전에 너가 {tree}이라고 응답을 해 주었는데, 사용자는 {rerun}라고 수정을 해 달래. 그러니까 이것을 가지고 최종적으로 답변을 생성해줘. 주제는 {prompt}야'})
            stream = chat(model="exaone3.5:7.8b",
                          messages= st.session_state.history_chathisroty[st.session_state.check_idx]
                          ,stream=True)
            for chunk in stream:
                answer += chunk.message.content
                placeholder_answer.markdown(f"<span style='font-size:16px;'>{answer}</span>", unsafe_allow_html=True)
            st.session_state.history_chathisroty[st.session_state.check_idx].pop()
            st.session_state.history_chathisroty[st.session_state.check_idx].append({'role': 'assistant', 'content':answer})
            
            
        
        
        st.markdown(f":violet-badge[⚡{st.session_state.history_model[st.session_state.check_idx]}]")
        st.markdown('----')
        st.session_state.generating = False


elif st.session_state.history_chathisroty[st.session_state.check_idx][-1]['role'] == 'system':
    ## 디자인 지정
    st.markdown(
        """
        <style>
        .gradient-text {
            text-align: center;
            margin-top: 30vh;
            font-size: 3em;
            font-weight: bold;
            background: linear-gradient(270deg, #9d00ff, #0055ff, #00ffee, #9d00ff);
            background-size: 600% 600%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: gradient-flow 6s ease infinite;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # 문구
    st.markdown(
        f"""
        <div class="gradient-text">만나서 반갑습니다, {user_name}님</div>
        """,
        unsafe_allow_html=True
    )