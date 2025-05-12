import requests

# Configurações fixas
USERNAME = "USER"
PASSWORD = "SENHA"
WORKSPACE = "PROJETO"

def create_group(group_name):
    """
    Cria um grupo no Bitbucket usando a API 1.0.
    """
    url = f"https://api.bitbucket.org/1.0/groups/{WORKSPACE}/"

    # Dados do grupo a serem enviados
    payload = {
        "name": group_name
    }

    # Realiza a solicitação POST
    response = requests.post(url, data=payload, auth=(USERNAME, PASSWORD))

    if response.status_code == 200 or response.status_code == 201:
        print(f"Grupo '{group_name}' criado com sucesso!")
        print("Resposta da API:", response.json())
    else:
        print(f"Erro ao criar o grupo '{group_name}'.")
        print(f"Código de status: {response.status_code}")
        print("Resposta da API:", response.text)

if __name__ == "__main__":
    # Solicita o nome do grupo ao usuário
    group_name = input("Digite o nome do grupo a ser criado: ")
    create_group(group_name)
