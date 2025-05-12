#Pega todos os projetos e lista seus diretórios


import requests
import csv

# Defina as variáveis de autenticação e workspace
username = "user"
password = "senha"
workspace = "projeto"  # Substitua pelo seu workspace
projects_url = f"url"

# Função para obter os dados dos repositórios, com filtragem dos campos desejados
def get_repositories_info():
    page = 1
    all_repositories = []

    while True:
        url = f"https://api.bitbucket.org/2.0/repositories/{workspace}"
        params = {"pagelen": 100, "page": page}
        response = requests.get(url, auth=(username, password), params=params)
        response.raise_for_status()
        data = response.json()

        # Itera sobre cada repositório para coletar "full_name" e "name" do projeto
        for repo in data.get("values", []):
            repository_name = repo.get("name")
            project_name = repo.get("project", {}).get("name")

            # Armazena os dados filtrados
            if repository_name and project_name:
                all_repositories.append({
                    "Repository": repository_name,
                    "Project": project_name
                })

        # Verifica se há mais páginas para continuar a busca
        if "next" not in data:
            break
        page += 1

    return all_repositories

# Chamar a função e obter a lista de repositórios
repositories_info = get_repositories_info()

# Salvar os dados em um arquivo CSV
with open("BIT - Projetos&Repositórios.csv", "w", newline='') as csvfile:
    fieldnames = ["Project", "Repository"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()  # Escreve o cabeçalho
    writer.writerows(repositories_info)  # Escreve os dados

print("Todos os repositórios foram salvos em 'BIT - Projetos&Repositórios.csv'")

