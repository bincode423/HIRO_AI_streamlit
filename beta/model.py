#모듈 호출하기
import ollama
from ollama import chat

model_1 = 'exaone3.5:7.8b'
model_2 = "llama3.2-ko"

user_input = input()

# 첫 메시지 생성
print('✨  응답')
stream = chat( model=model_1, messages= [{'role': 'user', 'content':user_input}], stream=True )
bot_answer = ''
for chunk in stream:
    print(chunk.message.content,end='',flush=True)
    bot_answer += chunk.message.content
print('\n')

#보완점 찾기
print('🗝️  응답의 보완점')
stream = chat( model=model_1, messages= [{'role': 'user', 'content':f'"{bot_answer}"이것은 사용자가 {user_input}이라 했을 때에 답변인데, 좀 더 부족한 부분이 있으면 알려줘.'}], stream=True )
repect = ''
for chunk in stream:
    print(chunk.message.content,end='',flush=True)
    repect += chunk.message.content
print('\n')

# 수정된 응답
print('✨  수정된 응답')
stream = chat( model=model_1, messages= [{'role': 'user', 'content':f'전에 너가 {bot_answer}이라고 응답을 해 주었는데, 사용자는 {repect}라고 수정을 해 달래. 그러니까 이것을 가지고 최종적으로 답변을 생성해줘'}], stream=True )
bot_answer = ''
for chunk in stream:
    print(chunk.message.content,end='',flush=True)
    bot_answer += chunk.message.content
print('\n')