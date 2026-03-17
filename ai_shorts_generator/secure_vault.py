import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv, set_key

# Caminho para a chave mestra
KEY_FILE = "master.key"

def generate_key():
    """Gera uma chave de criptografia e salva em um arquivo."""
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)
    print(f"✅ Nova Chave Mestra gerada e salva em {KEY_FILE}")

def load_key():
    """Carrega a chave de criptografia do arquivo."""
    if not os.path.exists(KEY_FILE):
        generate_key()
    return open(KEY_FILE, "rb").read()

def encrypt_value(value):
    """Criptografa uma string."""
    f = Fernet(load_key())
    return f.encrypt(value.encode()).decode()

def decrypt_value(encrypted_value):
    """Descriptografa uma string."""
    f = Fernet(load_key())
    return f.decrypt(encrypted_value.encode()).decode()

def secure_env_fields(fields_to_encrypt):
    """Criptografa campos específicos no .env se eles não estiverem criptografados."""
    load_dotenv()
    env_path = ".env"
    
    for field in fields_to_encrypt:
        value = os.getenv(field)
        if value and not value.startswith("gAAAAA"): # Prefixo padrão do Fernet
            print(f"🛡️ Criptografando campo: {field}")
            encrypted = encrypt_value(value)
            set_key(env_path, field, encrypted)
            
    print("✅ Operação de Blindagem concluída.")

if __name__ == "__main__":
    # Exemplo de uso: criptografar senhas no .env
    secure_env_fields(["IG_PASSWORD", "OPENAI_API_KEY"])
