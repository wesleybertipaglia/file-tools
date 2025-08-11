import os

def renomear_arquivos(txt_path, dir_path):
    # Lê os novos nomes a partir do arquivo txt
    with open(txt_path, 'r', encoding='utf-8') as f:
        novos_nomes = [linha.strip() for linha in f if linha.strip()]
    
    # Lista e ordena os arquivos no diretório
    arquivos = sorted([f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))])

    # Verifica se a quantidade de arquivos bate com os nomes
    if len(novos_nomes) != len(arquivos):
        print(f"\n❌ Erro: {len(novos_nomes)} nomes no TXT, mas {len(arquivos)} arquivos no diretório.\n")
        return

    print("\n🔄 Renomeando arquivos...")
    for antigo, novo in zip(arquivos, novos_nomes):
        ext = os.path.splitext(antigo)[1]  # mantém a extensão original
        novo_nome = novo.replace('.png', '') + ext  # remove .png do nome novo se houver
        caminho_antigo = os.path.join(dir_path, antigo)
        caminho_novo = os.path.join(dir_path, novo_nome)
        os.rename(caminho_antigo, caminho_novo)
        print(f"✅ {antigo} -> {novo_nome}")

    print("\n✅ Todos os arquivos foram renomeados com sucesso!\n")

def menu():
    while True:
        print("=== Renomeador de Arquivos ===")
        print("1. Iniciar renomeação")
        print("2. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            txt_path = input("\n📄 Caminho do arquivo .txt com os novos nomes: ").strip()
            dir_path = input("📁 Caminho da pasta com os arquivos a renomear: ").strip()

            if not os.path.isfile(txt_path):
                print("\n❌ Arquivo .txt não encontrado!\n")
                continue
            if not os.path.isdir(dir_path):
                print("\n❌ Diretório inválido!\n")
                continue

            renomear_arquivos(txt_path, dir_path)

        elif opcao == "2":
            print("\n👋 Saindo...")
            break
        else:
            print("\n❌ Opção inválida!\n")

if __name__ == "__main__":
    menu()
