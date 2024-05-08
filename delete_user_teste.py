import os
import subprocess
import winreg

# Habilita política de execução de script
resultado = subprocess.run(["powershell", "Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser"], capture_output=True)

# Verifica se a execução foi bem-sucedida
if resultado.returncode == 0:
    print("Política de execução de script habilitada com sucesso!")
else:
    print("Erro ao habilitar política de execução de script:")
    print(resultado.stderr.decode())

# Você também pode verificar a saída padrão para obter informações adicionais se necessário
print("Saída padrão:", resultado.stdout.decode())
# Remove diretórios de usuários
diretorio = "C:\\Users"
pastas = os.listdir(diretorio)
print("Excluindo diretórios...")

for pasta in pastas:
    if pasta.isdigit():
        pasta_atual = os.path.join(diretorio, pasta)
        subprocess.run(["powershell", f"Remove-Item -Path '{pasta_atual}' -Recurse -Force"])


for pasta in pastas:
    if not pasta.isdigit():
        #print("pastas cpf apagadas")
        with winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE) as hkey:
            with winreg.OpenKey(hkey, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList") as subkey:
                num_subkeys = winreg.QueryInfoKey(subkey)[0]
                for i in range(num_subkeys):
                    subkey_name = winreg.EnumKey(subkey, i)
                    try:
                        with winreg.OpenKey(subkey, subkey_name) as profile_key:
                            profile_image_path, _ = winreg.QueryValueEx(profile_key, "ProfileImagePath")
                            profile_image_path = profile_image_path.lower()
                            if any(keyword in profile_image_path for keyword in ["administrador", "suporte", "suportedti", "windows"]):
                                print("NÃO REMOVE", subkey_name)
                            else:
                                print("REMOVE!!!")
                                winreg.DeleteKey(hkey, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList\\" + subkey_name)
                    except Exception as e:
                        print("Erro ao acessar chave de registro:", e)       


