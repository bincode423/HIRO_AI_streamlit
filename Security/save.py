import pickle
import os

def generate_secure_key():
    return os.urandom(64)

def save_key(key: bytes, filename: str = "key.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(key, f)

def load_key(filename: str = "./Security/key.pkl") -> bytes:
    with open(filename, "rb") as f:
        return pickle.load(f)

if __name__ == '__main__':
    key = generate_secure_key()
    save_key(key)