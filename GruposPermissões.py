############################## USADO PARA VER AS PESSOAS QUE TEM EM CADA DIRETORIO #############################################

import requests
import json
import csv

# Defina suas credenciais 
username = "LOGIN"
password = "SENHA_APP"
base_url = "URL_API"

# Carrega os repositórios do arquivo .txt
with open("project_keys.txt", "r") as f:
    repo_slugs = [line.strip() for line in f.readlines()]

# Lista para armazenar os dados filtrados
all_permissions = []

# Para cada repositório, faz a requisição para buscar os grupos
for repo_slug in repo_slugs:
    # Define a URL completa para o endpoint de grupos do repositório atual
    url = f"{base_url}/{repo_slug}/permissions-config/groups?page=2"
    
    # Realiza a requisição GET para o endpoint específico
    response = requests.get(url, auth=(username, password))
    
    # Verifica se a requisição foi bem-sucedida
    if response.status_code == 200:
        data = response.json()
        
        # Filtra os campos 'group', 'permission' e 'repository'
        for item in data.get("values", []):
            all_permissions.append({
                "Group": item["group"]["name"],  # Nome do grupo
                "Permission": item["permission"],
                "Repository": repo_slug  # Nome do repositório atual
            })
    else:
        print(f"Erro ao acessar grupos de {repo_slug}: {response.status_code}")

# Salva o resultado filtrado em um arquivo CSV
with open("BIT - Permissões dos grupos.csv", "w", newline='') as csvfile:
    fieldnames = ["Group", "Permission", "Repository"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()  # Escreve o cabeçalho
    writer.writerows(all_permissions)  # Escreve os dados

print("Dados salvos em 'FilteredGroupPermissions.csv'")