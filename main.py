from engine import tool_type, tool_registry, tool_loader

def choose_tool_type():
    tipos = list(tool_type.ToolType)
    print("Escolha o tipo:")
    for i, t in enumerate(tipos, 1):
        print(f"{i} - {t.name.title()}")
    print("0 - Sair")

    escolha = input("Opção: ").strip()
    if escolha == "0":
        return None

    try:
        idx = int(escolha) - 1
        return tipos[idx]
    except:
        print("❌ Opção inválida.")
        return None

def choose_tool(commands):
    if not commands:
        print("❌ Nenhuma ferramenta registrada para esse tipo.")
        return None

    print("\nEscolha a ferramenta:")
    for key, cmd in sorted(commands.items()):
        print(f"{key} - {cmd.name()}")

    escolha = input("Opção: ").strip()
    if escolha == "0":
        return None

    return commands.get(escolha)

def main():
    while True:
        tipo = choose_tool_type()
        if tipo is None:
            print("Saindo...")
            break

        comandos = tool_registry.get_commands_by_type(tipo)
        comando = choose_tool(comandos)
        if comando:
            comando.run()
        else:
            print("❌ Ferramenta inválida ou cancelada.")

if __name__ == "__main__":
    main()
