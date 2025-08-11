from scripts import file_lister, file_renamer, file_zipper, img_converter

TOOLS = {
    "1": ("Renomear arquivos com padrão", file_renamer.run),
    "2": ("Listar arquivos", file_lister.run),
    "3": ("Compactar arquivos", file_zipper.run),
    "4": ("Converter imagens", img_converter.run),
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
