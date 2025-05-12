############################## USADO PARA VER OS GRUPOS QUE TEM EM CADA DIRETORIO #############################################

import requests
import json
import csv

# Defina suas credenciais e URL
username = "user"
password = "senha"
base_url_permissions = "https://api.bitbucket.org/2.0/workspaces/PROJETO/permissions/repositories/"
base_url_groups = "https://api.bitbucket.org/2.0/repositories/PROJETO/{repo_slug}/permissions-config/groups"
page = 1

# Carrega os repositórios do arquivo .txt
with open("ListOfRepoSlug.txt", "r") as f:
    repo_slugs = [line.strip() for line in f.readlines()]

# Lista para armazenar os dados filtrados
all_permissions = []

# Para cada repositório, faz a requisição e filtra os dados
for repo_slug in repo_slugs:
    # URL para obter permissões dos usuários
    
    url_permissions = f"{base_url_permissions}{repo_slug}?pagelen=100&"
        
    # Realiza a requisição GET para o repositório específico

    response_permissions = requests.get(url_permissions, auth=(username, password))
        
    if response_permissions.status_code == 200:
        data_permissions = response_permissions.json()
            
        # Filtra os campos 'user', 'permission' e 'repository'
        for item in data_permissions.get("values", []):
            all_permissions.append({
                "Users": item["user"]["display_name"],  # Nome do usuário
                "Permission": item["permission"],
                "Repository": repo_slug  # Nome do repositório atual
            })
    else:
        print(f"Erro ao acessar permissões do usuário em {repo_slug}: {response_permissions.status_code}")
    
    # URL para obter permissões dos grupos
    url_groups = base_url_groups.format(repo_slug=repo_slug)
    response_groups = requests.get(url_groups, auth=(username, password))
    
    if response_groups.status_code == 200:
        data_groups = response_groups.json()
        
        # Filtra os campos 'group', 'permission' e 'repository'
        for item in data_groups.get("values", []):
            all_permissions.append({
                "Grupos": item["group"]["name"],  # Nome do grupo
                "Permission": item["permission"],
                "Repository": repo_slug  # Nome do repositório atual
            })
    else:
        print(f"Erro ao acessar permissões dos grupos em {repo_slug}: {response_groups.status_code}")

# Salva o resultado filtrado em um arquivo CSV
with open("BIT- Usuarios&Grupos.csv", "w", newline='') as csvfile:
    fieldnames = ["Users","Grupos","Permission", "Repository"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()  # Escreve o cabeçalho
    writer.writerows(all_permissions)  # Escreve os dados

print("Dados salvos em 'BIT- Usuarios&Grupos.csv'")