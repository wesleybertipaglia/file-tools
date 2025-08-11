import os
import re

PATTERNS = {
    "1": ("Remover números", r"\d"),
    "2": ("Remover caracteres especiais", r"[^\w\s]"),
    "3": ("Remover texto exato", None),
    "4": ("Regex personalizada", None),
    "5": ("Estilo de texto", "STYLE"),
}

TEXT_STYLES = {
    "1": ("Capitalized", str.capitalize),
    "2": ("Title", str.title),
    "3": ("Lower", str.lower),
    "4": ("Upper", str.upper),
}

def run():
    folder = input("Digite o caminho da pasta: ").strip()

    if not os.path.isdir(folder):
        print("❌ Caminho inválido.")
        return

    print("\nEscolha o padrão de remoção/transformação:")
    for key, (desc, _) in PATTERNS.items():
        print(f"{key} - {desc}")

    choice = input("Opção: ").strip()

    if choice not in PATTERNS:
        print("❌ Opção inválida.")
        return

    desc, pattern = PATTERNS[choice]

    if pattern == "STYLE":
        print("\nEscolha o estilo de texto:")
        for key, (style_name, _) in TEXT_STYLES.items():
            print(f"{key} - {style_name}")
        style_choice = input("Opção: ").strip()

        if style_choice not in TEXT_STYLES:
            print("❌ Opção inválida para estilo.")
            return

        style_name, style_func = TEXT_STYLES[style_choice]

        renamed_count = 0
        for filename in os.listdir(folder):
            full_path = os.path.join(folder, filename)
            if os.path.isfile(full_path):
                name, ext = os.path.splitext(filename)
                new_name = style_func(name) + ext
                if new_name != filename:
                    new_full_path = os.path.join(folder, new_name)
                    os.rename(full_path, new_full_path)
                    print(f"Renomeado: {filename} → {new_name}")
                    renamed_count += 1

        print(f"\n✅ {renamed_count} arquivos renomeados usando estilo: {style_name}")
        return

    if choice == "3":
        text_to_remove = input("Digite o texto exato a remover: ").strip()
        pattern = re.escape(text_to_remove)
    elif choice == "4":
        pattern = input("Digite sua regex personalizada: ").strip()

    start_pos = None
    end_pos = None
    if choice != "4":
        try:
            start_pos = int(input("Digite a posição inicial (começando por 0): ").strip())
            end_pos = int(input("Digite a posição final (deixe em branco para ir até o fim): ").strip() or -1)
        except ValueError:
            print("❌ Posições inválidas.")
            return

    regex = re.compile(pattern)
    renamed_count = 0

    for filename in os.listdir(folder):
        full_path = os.path.join(folder, filename)

        if os.path.isfile(full_path):
            if choice != "4":
                target_segment = filename[start_pos:end_pos if end_pos != -1 else None]
                new_segment = regex.sub("", target_segment)
                new_name = filename[:start_pos] + new_segment + (filename[end_pos:] if end_pos != -1 else "")
            else:
                new_name = regex.sub("", filename)

            if new_name != filename:
                new_full_path = os.path.join(folder, new_name)
                os.rename(full_path, new_full_path)
                print(f"Renomeado: {filename} → {new_name}")
                renamed_count += 1

    print(f"\n✅ {renamed_count} arquivos renomeados usando padrão: {desc}")
