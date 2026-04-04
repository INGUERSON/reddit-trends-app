import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv, set_key

KEY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "master.key")

def generate_key():
      key = Fernet.generate_key()
      with open(KEY_FILE, "wb") as key_file:
                key_file.write(key)
            print(f"Nova Chave Mestra gerada e salva em {KEY_FILE}")

def load_key():
      if not os.path.exists(KEY_FILE):
                if os.getenv("GITHUB_ACTIONS"):
                              return None
                          generate_key()
    with open(KEY_FILE, "rb") as key_file:
              return key_file.read()

def encrypt_value(value):
      key = load_key()
    if not key:
              return value
    f = Fernet(key)
    return f.encrypt(value.encode()).decode()

def decrypt_value(encrypted_value):
      key = load_key()
    if not key:
              print("Erro: master.key nao encontrada. Usando valor bruto.")
        return encrypted_value
    try:
              f = Fernet(key)
        return f.decrypt(encrypted_value.encode()).decode()
except Exception:
        print("Falha na descriptografia. Usando valor bruto.")
        return encrypted_value

def secure_env_fields(fields_to_encrypt):
      load_dotenv()
    env_path = ".env"
    for field in fields_to_encrypt:
              value = os.getenv(field)
        if value and not value.startswith("gAAAAA"):
                      print(f"Criptografando campo: {field}")
                      encrypted = encrypt_value(value)
                      set_key(env_path, field, encrypted)
              print("Operacao de Blindagem concluida.")

if __name__ == "__main__":
      secure_env_fields(["IG_PASSWORD", "OPENAI_API_KEY"])
