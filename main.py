from engine import tool_type, tool_registry, tool_loader

def choose_tool_type():
    types = list(tool_type.ToolType)
    print("Choose the type:")
    for i, t in enumerate(types, 1):
        print(f"{i} - {t.name.title()}")
    print("0 - Exit")

    choice = input("Option: ").strip()
    if choice == "0":
        return None

    try:
        idx = int(choice) - 1
        return types[idx]
    except:
        print("❌ Invalid option.")
        return None

def choose_tool(commands):
    if not commands:
        print("❌ No tools registered for this type.")
        return None

    print("\nChoose the tool:")
    for key, cmd in sorted(commands.items()):
        print(f"{key} - {cmd.name()}")

    choice = input("Option: ").strip()
    if choice == "0":
        return None

    return commands.get(choice)

def main():
    while True:
        tool_type_selected = choose_tool_type()
        if tool_type_selected is None:
            print("Exiting...")
            break

        commands = tool_registry.get_commands_by_type(tool_type_selected)
        command = choose_tool(commands)
        if command:
            command.run()
        else:
            print("❌ Invalid or cancelled tool.")

if __name__ == "__main__":
    main()
