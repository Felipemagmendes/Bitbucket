############################## USADO PARA VER AS PESSOAS QUE TEM EM CADA DIRETORIO #############################################

import requests
import json
import csv

# Defina suas credenciais e URL
username = "USER"
password = "SENHA_DE_APP"
base_url = "URL_BASE"

# Carrega os repositórios do arquivo .txt
with open("ListOfRepoSlug.txt", "r") as f:
    repo_slugs = [line.strip() for line in f.readlines()]

# Lista para armazenar os dados filtrados
all_permissions = []

# Para cada repositório, faz a requisição e filtra os dados
for repo_slug in repo_slugs:
    # Define a URL completa para o repositório atual
    url = f"{base_url}{repo_slug}"
    
    # Realiza a requisição GET para o repositório específico
    response = requests.get(url, auth=(username, password))
    
    # Verifica se a requisição foi bem-sucedida
    if response.status_code == 200:
        data = response.json()
        
        # Filtra os campos 'user', 'permission' e 'repository'
        for item in data.get("values", []):
            all_permissions.append({
                "Users": item["user"]["display_name"],  # Nome do usuário
                "Permission": item["permission"],
                "Repository": repo_slug  # Nome do repositório atual
            })
    else:
        print(f"Erro ao acessar {repo_slug}: {response.status_code}")

# Salva o resultado filtrado em um arquivo CSV
with open("BIT - Permissões_Diretórios.csv", "w", newline='') as csvfile:
    fieldnames = ["Users", "Permission", "Repository"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()  # Escreve o cabeçalho
    writer.writerows(all_permissions)  # Escreve os dados

print("Dados salvos em 'BIT - Permissões_Diretórios.csv'")