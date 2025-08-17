import pickle
import random, string
from Security import security as sc
from Security import save as sv_s
import moduls.email as em
import os

def generate_email_key(length=6):
    chars = list('123456789!@#$%^&*()_+qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM}[]{:;"><?/.,`~ㅂㅁㅋㅈㄴㅌㄷㅇㅊㄱㄿㅅ휴ㅛㅗㅜㅕㅓㅡㅑㅏㅐㅣㅔ')
    password = ''.join(random.choice(chars) for _ in range(length))
    return password

def make_account(user_id, email, password):
    pass

def login(email, password):
    return False



def make_account(user_id, email, password):
    os.makedirs(f"./database/{email}", exist_ok=True)
    em.add_email(email)
    
    #암호화
    key = sv_s.load_key()
    encrypted_password = sc.encrypt_secure(key, password)

    #저장
    with open(f"./database/{email}/id.pkl", "wb") as f:
        pickle.dump(user_id, f)
    with open(f"./database/{email}/password.pkl", "wb") as f:
        pickle.dump(encrypted_password, f)
    with open(f"./database/{email}/user_memory.pkl", "wb") as f:
        pickle.dump([], f)
    with open(f"./database/{email}/chat_hisroy_name.pkl", "wb") as f:
        pickle.dump([], f)
    with open(f"./database/{email}/chat_history_talk.pkl", "wb") as f:
        pickle.dump([], f)
    with open(f"./database/{email}/chat_history_model.pkl", "wb") as f:
        pickle.dump([], f)