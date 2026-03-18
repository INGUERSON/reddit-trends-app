import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv, set_key

# Caminho absoluto para a chave mestra (sempre no mesmo local que este script)
KEY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "master.key")

def generate_key():
    """Gera uma chave de criptografia e salva em um arquivo."""
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)
    print(f"✅ Nova Chave Mestra gerada e salva em {KEY_FILE}")

def load_key():
    """Carrega a chave de criptografia do arquivo. No ambiente GitHub, pode não existir."""
    if not os.path.exists(KEY_FILE):
        # Se estivermos no GitHub Actions, não queremos gerar uma chave aleatória que vai falhar na descriptografia
        # de valores que foram criptografados localmente.
        if os.getenv("GITHUB_ACTIONS"):
             return None
        generate_key()
    
    with open(KEY_FILE, "rb") as key_file:
        return key_file.read()

def encrypt_value(value):
    """Criptografa uma string."""
    key = load_key()
    if not key:
        return value # Fallback se não houver chave (ambiente nuvem)
    f = Fernet(key)
    return f.encrypt(value.encode()).decode()

def decrypt_value(encrypted_value):
    """Descriptografa uma string."""
    key = load_key()
    if not key:
        print("⚠️ Erro: master.key não encontrada. Usando valor bruto (certifique-se de usar segredos Limpos no GitHub).")
        return encrypted_value
    try:
        f = Fernet(key)
        return f.decrypt(encrypted_value.encode()).decode()
    except Exception:
        print("⚠️ Falha na descriptografia (Chave Incompatível). Usando valor bruto.")
        return encrypted_value

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
