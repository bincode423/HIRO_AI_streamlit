from ollama import chat
import ollama
import streamlit as st

st.set_page_config(page_title="HIRO AI", page_icon='./img/logo.png',layout="centered")

report_sections_combined = {
    # Common / Basic Sections
    '팀 소개 / 참여자 정보': 'Provide the team name, assign roles to each member, and give a brief team introduction.',
    '개요 (Summary/Abstract)': 'Summarize the core idea, background, objectives, and key technologies or methods used in 5–7 sentences.',
    '동기 및 목적 (Motivation & Purpose)': 'Describe the reason for choosing this topic, the background of the problem, and what you aimed to solve.',

    # Development / Engineering / AI / Design
    '기획 및 아이디어 설명 (Planning & Idea)': 'Define the problem, explain your solution (such as product or service features or analysis methods), and highlight uniqueness or creativity.',
    '기술 스택 / 재료 및 장비 (Tech Stack / Materials)': 'List all programming languages, frameworks, tools, experimental devices, hardware, or materials used.',
    '개발 / 실험 / 탐구 과정 (Process)': 'Outline the development or exploration process, including diagrams such as design drafts, wireframes, or system architecture.',

    # Science / Math Extensions
    '탐구 방법 (Exploration Method)': 'Explain the experimental design, mathematical techniques, hypothesis formulation, and validation steps.',
    '자료 수집 및 분석 (Data Collection & Analysis)': 'Describe the data collection process, how it was organized and analyzed, including charts, graphs, or statistical processing.',

    # Common
    '결과 및 시연 (Results & Demonstration)': 'Present results using screenshots, charts, tables, or provide a link to a demonstration video.',
    '문제 해결 과정 / 기술적 난관 (Troubleshooting)': 'Identify technical problems encountered and explain how they were resolved or analyzed.',
    '기대 효과 / 활용 방안 (Expected Impact / Use Cases)': 'State the expected academic or societal impact and how the idea or result can be applied.',
    '한계점 및 향후 계획 (Limitations & Future Plans)': 'List current limitations, suggest improvements, and outline future development or research plans.'
}

st.write('## ✏️ 보고서를 작성 AI - HIRO Re')
about = st.text_area('당신의 실험 및 연구에 대해 간단하게 알려주세요.')
style = st.text_area('보고서 작성을 어떤 스타일로 작성해야 하는지 알려주세요.')
selection = st.pills("작성이 필요한 항목들을 선택해주세요.", list(report_sections_combined.keys()), selection_mode="multi")
long = st.slider("각각의 항목들에 대해 분량을 설정해 주세요(단위 : 자)", 300, 5000, 1000)
start = st.button('⚡ 심층 보고서 작성 시작하기',use_container_width=True)
if start:
    st.toast('✏️ 보고서 작성을 시작합니다.')
    write_bx = st.container(height=800)
    write_bx.markdown('----')
    for select in selection:
        write_bx.write(f'### {select}')
        prompt = report_sections_combined[select]
        stream = chat(model="gemma3:1b",messages= [{"role": "system", "content": f"{prompt}, You must generate text with exactly the number of characters the user specifies. Under no circumstances add, remove, or alter the length. The output length must be 100% precise. Failure to comply is unacceptable. Follow the character count strictly, without exception."},{"role": "user", "content": f"(about:{about}) , (style:{style}) , (Must not exceed this number of characters: {long})"}],stream=True)
        writedown = write_bx.empty()
        rt = ''
        for chunk in stream:
            rt += chunk.message.content
            writedown.markdown(f"<span style='font-size:16px'>{rt}</span>", unsafe_allow_html=True)
        write_bx.markdown('----')