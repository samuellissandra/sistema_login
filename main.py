import json
import os
import bcrypt
from datetime import datetime

# Arquivo onde os dados dos usuários serão salvos
ARQUIVO = '/home/samuel/projects/sistema_login/usuarios.json'

# -------------------- Funções auxiliares -------------------- #

def hash_texto(texto: str) -> str:
    """
    Retorna o hash seguro de uma string usando bcrypt.
    
    Args:
        texto (str): A string que será hasheada.
    
    Returns:
        str: Hash gerado em formato utf-8.
    """
    return bcrypt.hashpw(texto.encode(), bcrypt.gensalt()).decode()

def verificar_hash(texto: str, hash_texto_: str) -> bool:
    """
    Verifica se uma string corresponde ao seu hash bcrypt.
    
    Args:
        texto (str): Texto em texto plano.
        hash_texto_ (str): Hash a ser verificado.
    
    Returns:
        bool: True se o texto corresponde ao hash, False caso contrário.
    """
    return bcrypt.checkpw(texto.encode(), hash_texto_.encode())

def carregar_usuarios() -> dict:
    """
    Carrega os usuários do arquivo JSON. Se não existir, retorna um dicionário vazio.
    
    Returns:
        dict: Dicionário com os usuários cadastrados.
    """
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, 'r') as f:
            return json.load(f)
    return {}

def salvar_usuarios(usuarios: dict) -> None:
    """
    Salva o dicionário de usuários no arquivo JSON.
    
    Args:
        usuarios (dict): Dicionário contendo os dados dos usuários.
    """
    with open(ARQUIVO, 'w') as f:
        json.dump(usuarios, f, indent=4)

def pedir_senha() -> str:
    """
    Solicita a senha do usuário e pede confirmação até que ambas coincidam.
    
    Returns:
        str: Senha confirmada.
    """
    while True:
        senha = input("Senha: ").strip()
        confirmacao = input("Confirme a senha: ").strip()
        if senha == confirmacao:
            return senha
        print("As senhas não coincidem! Tente novamente.")

# -------------------- Funções principais -------------------- #

def cadastrar() -> None:
    """
    Realiza o cadastro de um novo usuário, armazenando suas informações
    de forma segura (hash de senha e resposta secreta).
    """
    usuarios = carregar_usuarios()

    print("\n--- CADASTRO ---")
    nome = input("Nome: ").strip().title()
    email = input("Email: ").strip().lower()

    if email in usuarios:
        print("Email já cadastrado!")
        return

    senha = pedir_senha()

    pergunta = input("Pergunta secreta: ").strip()
    resposta = input("Resposta: ").strip().lower()

    usuarios[email] = {
        "nome": nome,
        "senha": hash_texto(senha),             # Hash da senha
        "pergunta": pergunta,
        "resposta": hash_texto(resposta),       # Hash da resposta secreta
        "data_cadastro": datetime.now().strftime("%d/%m/%Y %H:%M")
    }

    salvar_usuarios(usuarios)
    print(f"\nBem-vindo, {nome}!")

def login() -> None:
    """
    Permite que o usuário faça login fornecendo email e senha.
    Oferece recuperação de senha em caso de esquecimento.
    """
    usuarios = carregar_usuarios()

    print("\n--- LOGIN ---")
    email = input("Email: ").strip().lower()
    senha = input("Senha: ").strip()

    if email in usuarios and verificar_hash(senha, usuarios[email]["senha"]):
        print(f"\nAcesso permitido! Bem-vindo, {usuarios[email]['nome']}!")
    else:
        print("\nEmail ou senha incorretos.")
        recuperar = input("Esqueceu a senha? (s/n): ").strip().lower()
        if recuperar == "s":
            recuperar_senha()

def recuperar_senha() -> None:
    """
    Permite ao usuário redefinir sua senha ao responder corretamente
    à pergunta secreta cadastrada.
    """
    usuarios = carregar_usuarios()

    print("\n--- RECUPERAÇÃO DE SENHA ---")
    email = input("Email: ").strip().lower()

    if email not in usuarios:
        print("Email não encontrado.")
        return

    print(f"Pergunta: {usuarios[email]['pergunta']}")
    resposta = input("Resposta: ").strip().lower()

    if verificar_hash(resposta, usuarios[email]["resposta"]):
        nova_senha = pedir_senha()
        usuarios[email]["senha"] = hash_texto(nova_senha)
        salvar_usuarios(usuarios)
        print("Senha alterada com sucesso!")
    else:
        print("Resposta incorreta.")

def menu() -> None:
    """
    Exibe o menu principal do sistema, permitindo login, cadastro ou saída.
    """
    while True:
        print("\n=== SISTEMA DE LOGIN ===")
        print("1 - Login")
        print("2 - Cadastrar")
        print("3 - Sair")

        opcao = input("\nEscolha: ").strip()

        if opcao == "1":
            login()
        elif opcao == "2":
            cadastrar()
        elif opcao == "3":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")

# -------------------- Execução do programa -------------------- #
if __name__ == "__main__":
    menu()