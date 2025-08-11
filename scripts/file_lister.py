import os

def run():
    folder = input("Digite o caminho da pasta: ").strip()

    if not os.path.isdir(folder):
        print("❌ Caminho inválido.")
        return

    arquivos = sorted(os.listdir(folder))

    print("\nArquivos na pasta:")
    for filename in arquivos:
        print(f" - {filename}")

    salvar = input("\nDeseja salvar essa lista em um arquivo .txt? (s/n): ").strip().lower()

    if salvar == "s":
        nome_arquivo = input("Digite o nome do arquivo TXT (sem extensão): ").strip()
        if not nome_arquivo:
            nome_arquivo = "lista_arquivos"

        caminho_saida = os.path.join(folder, f"{nome_arquivo}.txt")

        try:
            with open(caminho_saida, "w", encoding="utf-8") as f:
                for filename in arquivos:
                    f.write(filename + "\n")
            print(f"✅ Lista salva em: {caminho_saida}")
        except Exception as e:
            print(f"❌ Erro ao salvar: {e}")
