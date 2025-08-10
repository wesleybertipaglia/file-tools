from scripts import renamer, lister, zipper

TOOLS = {
    "1": ("Renomear arquivos com padrão", renamer.run),
    "2": ("Listar arquivos", lister.run),
    "3": ("Compactar arquivos", zipper.run),
}

def get_tool(choice):
    """Retorna a função associada a uma escolha de menu."""
    return TOOLS.get(choice, (None, None))[1]

def main():
    while True:
        print("\n=== FILE TOOLS ===")
        for key, (desc, _) in TOOLS.items():
            print(f"{key} - {desc}")
        print("0 - Sair")

        choice = input("Escolha uma opção: ").strip()

        if choice == "0":
            print("Saindo...")
            break

        tool_func = get_tool(choice)
        if tool_func:
            tool_func()
        else:
            print("❌ Opção inválida!")

if __name__ == "__main__":
    main()
