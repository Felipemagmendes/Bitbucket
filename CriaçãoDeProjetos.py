import requests

#Dados da API
USERNAME = "USER"
APP_PASSWORD = "SENHA"
WORKSPACE = "PROJETO"

def configurar_branch_restrictions(project_key, repo_slug):
    url = f"https://api.bitbucket.org/2.0/repositories/{WORKSPACE}/{repo_slug}/branch-restrictions"

    # Configurações para a branch 'master'
    payload_master = {
        "kind": "require_passing_builds_to_merge",
        "branch_match_kind": "glob",
        "pattern": "master",
        "value": 1
    }

    headers = {
        "Content-Type": "application/json"
    }

    # Enviar solicitação POST para configurar a branch 'master'
    response_master = requests.post(url, json=payload_master, auth=(USERNAME, APP_PASSWORD), headers=headers)

    if response_master.status_code == 201:
        print("Restrições para a branch 'master' configuradas com sucesso!")
    else:
        print(f"Falha ao configurar restrições para a branch 'master'. Código de status: {response_master.status_code}")
        print("Mensagem:", response_master.json())

    # Configurações para outras branches
    payload_branch_model = {
        "kind": "require_passing_builds_to_merge",
        "branch_match_kind": "branching_model",
        "value": 1
    }

    response_branch_model = requests.post(url, json=payload_branch_model, auth=(USERNAME, APP_PASSWORD), headers=headers)

    if response_branch_model.status_code == 201:
        print("Restrições para o modelo de branching configuradas com sucesso!")
    else:
        print(f"Falha ao configurar restrições para o modelo de branching. Código de status: {response_branch_model.status_code}")
        print("Mensagem:", response_branch_model.json())


#Função para criar o projeto
def criar_projeto(project_name, project_key):

    url = f"https://api.bitbucket.org/2.0/workspaces/{WORKSPACE}/projects"

    # Dados do projeto
    payload = {
        "name": project_name,
        "key": project_key,
        "is_private": True
    }

    #Solicitação
    headers = {
        "Content-Type": "application/json"
    }

    # Enviar solicitação POST
    response = requests.post(url, json=payload, auth=(USERNAME, APP_PASSWORD), headers=headers)

    # Verificar resposta
    if response.status_code == 201:
        print("Projeto criado com sucesso!")
        print("Detalhes do projeto:")
        print(response.json())
        return project_key
    else:
        print(f"Falha ao criar o projeto. Código de status: {response.status_code}")
        print("Mensagem:", response.json())
        return None

#DEU RUIM
def create_group(group_name):
    """
    Cria um grupo no workspace especificado.
    """
    url = f"https://api.bitbucket.org/1.0/groups/{WORKSPACE}"

    payload = {
        "name": group_name  # Nome do grupo a ser criado
    }

    response = requests.post(url, data=payload, auth=(USERNAME, APP_PASSWORD))

    if response.status_code == 200 or response.status_code == 201:
        print(f"Grupo '{group_name}' criado com sucesso!")
        print("Detalhes do grupo:")
        print(response.json())
        return group_name
    else:
        print(f"Erro ao criar o grupo '{group_name}'. Código de status: {response.status_code}")
        print(response.json())
        return None

def associar_grupo_com_projeto(project_key, group_slug, permission):
    """
    Associa um grupo a um projeto com uma permissão específica usando a API 2.0.
    """
    url = f"https://api.bitbucket.org/2.0/workspaces/{WORKSPACE}/projects/{project_key}/permissions-config/groups/{group_slug}"

    payload = {
        "permission": permission
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.put(url, json=payload, auth=(USERNAME, APP_PASSWORD), headers=headers)

        if response.status_code == 200 or response.status_code == 201:
            print(f"\nGrupo '{group_slug}' associado ao projeto '{project_key}' com permissão '{permission}'.")
        else:
            print(f"\nErro ao associar o grupo '{group_slug}' ao projeto '{project_key}'.")
            print(f"Código de status: {response.status_code}")
            print("Resposta da API:", response.text)
    except Exception as e:
        print(f"\nErro inesperado ao associar o grupo '{group_slug}' ao projeto '{project_key}': {e}")

if __name__ == "__main__":

    #Solicita o nome e a chave do projeto ao usuário
    project_name = input("Digite o nome do novo projeto: ")
    project_key = input("Digite uma chave para o projeto (abreviação, ex: PRJ): ")

    #Chama a função para criar o projeto
    project_key_criada = criar_projeto(project_name, project_key)

    if project_key_criada:
        while True:
            group_name = input("\nDigite o nome do grupo a ser criado (ou 'sair' para finalizar): ")
            if group_name.lower() == "sair":
                print("Encerrando a criação de grupos.")
                break

            # Criar o grupo
            nome_grupo_criado = create_group(group_name)

            if nome_grupo_criado:
                group_slug = nome_grupo_criado.lower().replace (" ", "-")
                while True:
                    permission = input("Escolha a permissao para o grupo ( admin, write ou read ): ")
                    if permission in ["admin", "write", "read"]:
                        break
                    else:
                        print("Permissao invalida")
                associar_grupo_com_projeto(project_key_criada, nome_grupo_criado, permission)
                configurar_branch_restrictions(project_key_criada, group_name)
            else:
                print("Deu ruim2")
    else:
        print("Deu ruim")