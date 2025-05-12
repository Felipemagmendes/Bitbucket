import requests

# Configurações de autenticação
username = "user"  # Substitua por seu nome de usuário
password = "senha"  # Substitua por sua senha
workspace = "projeto"  # Substitua pelo seu workspace

# Função para obter todas as chaves de projeto de um workspace e salvá-las em um arquivo
def get_project_keys():
    url = f"https://api.bitbucket.org/2.0/workspaces/{workspace}/projects"
    project_keys = []
    
    # Abre o arquivo para gravação
    with open("Bit - ProjectKeys.txt", "w") as file:
        # Paginação (caso haja muitos projetos)
        while url:
            response = requests.get(url, auth=(username, password))
            response.raise_for_status()
            
            data = response.json()
            projects = data.get("values", [])
            
            # Extrair a chave de cada projeto e gravar no arquivo
            for project in projects:
                project_key = project.get("key")
                project_name = project.get("name")
                print(f"Projeto: {project_name} - Key: {project_key}")
                
                # Salva a chave do projeto no arquivo
                if project_key:
                    file.write(f"{project_key}\n")
                    project_keys.append(project_key)
            
            # Verifica se há uma próxima página de resultados
            url = data.get("next")
    
    return project_keys

# Executa a função e salva as chaves de projeto em project_keys.txt
project_keys = get_project_keys()
print("\nChaves de todos os projetos salvas em 'project_keys.txt'")