import requests
import json
import os
import subprocess
import shutil
from datetime import datetime

# Autenticaçaõ do usuário
username = "USER"
password = "SENHA_DE_APP"
workspace = "nome_do_workspace"

# Pega as info da API 
def get_repositories_info(page):
    url = f"https://api.bitbucket.org/2.0/repositories/{workspace}"
    params = {"pagelen": 100, "page": page}
    response = requests.get(url, auth=(username, password), params=params)
    response.raise_for_status()  # exceção
    return response.json()

# Cria pasta de backup com a data do dia
backup_date = datetime.now().strftime("%d_%m_%y")
backup_folder = f"Backup_{backup_date}"
os.makedirs(backup_folder, exist_ok=True)

# pega quantos repositórios tem
print("Getting Repositories size")
response_data = get_repositories_info(page=100000)  # Página para obter a contagem total
total_size = response_data.get("size", 0)
print(f"Number of repositories: {total_size}\n")

# Lista para armazenar os slugs dos repositórios
repo_slugs = []

# Loop para buscar os slugs de repositórios por páginas
print("Getting Repositories slug")
page = 1
remaining_size = total_size

while remaining_size > 0:
    response_data = get_repositories_info(page)
    values = response_data.get("values", [])

    # Pegando o nome dos slugs
    for repo in values:
        slug = repo.get("full_name", "")
        if workspace in slug:
            repo_slugs.append(slug)
    
    page += 1
    remaining_size -= 100

# salvando em um arquivo
with open(os.path.join(backup_folder, "ListOfRepoSlug.txt"), "w") as file:
    file.write("\n".join(filter(None, repo_slugs)) + "\n")

# Calcular o tamanho do diretório em MB (Sem uso pra versão final)
def get_directory_size_mb(directory):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size / (1024 * 1024)  # Convertendo para MB

def manter_quatro_ultimos_backups(diretorio_base):
    # Lista os subdiretórios na pasta base
    subpastas = [os.path.join(diretorio_base, nome) for nome in os.listdir(diretorio_base) if os.path.isdir(os.path.join(diretorio_base, nome))]
    # Ordena pelas datas de criação/modificação (mais recentes primeiro)
    subpastas.sort(key=os.path.getmtime, reverse=True)
    # Mantém apenas os 4 mais recentes
    for pasta in subpastas[4:]:
        print(f"Removendo backup antigo: {pasta}")
        subprocess.run(["rm", "-rf", pasta])

manter_quatro_ultimos_backups(backup_folder)



# Clonando os repositórios da lista
print("Cloning Repositories")
with open(os.path.join(backup_folder, "ListOfRepoSlug.txt"), "r") as file:
    for count, line in enumerate(file, start=1):
        line = line.strip()  # Remove espaços em branco
        if line:
            print(f"{count}. Cloning {line}")
            clone_url = f"https://{username}:{password}@bitbucket.org/{line}"
            repo_name = line.split('/')[-1]  # Caso queira trocar o local do repositório
            repo_path = os.path.join(backup_folder, repo_name) # Armazena no diretório criado agora
            subprocess.run(["git", "clone", "--mirror", clone_url, repo_path])

            # Calculando o tamanho do repositório clonado
            repo_size_mb = get_directory_size_mb(repo_name)
            print(f"Completed - Size: {repo_size_mb:.2f} MB")



print("All repositories cloned and backup completed successfully.")
