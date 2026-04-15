import yt_dlp
import os

try:
    print("🕵️ Buscando session ID no Edge, Firefox, etc (feche os browsers primeiro se der erro)...")
    sessionid = None
    
    for browser_name in ['edge', 'firefox', 'chrome']:
        try:
            print(f"Tentando extrair do: {browser_name}...")
            cookies = yt_dlp.cookies.extract_cookies_from_browser(browser_name, None)
            
            for cookie in cookies:
                if 'instagram.com' in cookie.domain and cookie.name == 'sessionid':
                    sessionid = cookie.value
                    print(f"✅ SUCESSO! Encontrado no navegador {browser_name}!")
                    break
        except Exception as e:
            continue
            
        if sessionid:
            break
            
    if sessionid:
        
        # Apensa o session id no .env automaticamente
        with open('.env', 'a') as f:
            f.write(f"\nIG_SESSIONID={sessionid}\n")
            
        print("💾 Taa-da! Adicionei no seu arquivo .env automaticamente. Pode rodar seu bot normalmente agora!")
    else:
        print("\n❌ Nao consegui ler de nenhum navegador de forma automatica.")
        print("Siga os passos manuais:")
        print("1. Abra instagram.com, aperte F12")
        print("2. Clique em Application (ou Aplicativo) la no topo")
        print("3. Na esquerda, clique em Cookies > https://www.instagram.com")
        print("4. Procure a linha chamada 'sessionid', copie a salada de letras gigante ao lado dela.")
        print("5. Cole no seu arquivo .env como IG_SESSIONID=codigo_aqui")

except Exception as e:
    print(f"\n❌ Erro geral: {e}")
