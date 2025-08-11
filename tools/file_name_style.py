import os

from engine.tool_command import ToolCommand
from engine.tool_registry import register_command
from engine.tool_type import ToolType

class FileRenamerStyleCommand(ToolCommand):
    TEXT_STYLES = {
        "1": ("Capitalized", str.capitalize),
        "2": ("Title", str.title),
        "3": ("Lower", str.lower),
        "4": ("Upper", str.upper),
    }

    def name(self):
        return "Renomear Arquivos (Estilo de Texto)"

    def type(self):
        return ToolType.FILE

    def run(self, *args, **kwargs):
        folder = input("Digite o caminho da pasta: ").strip()

        if not os.path.isdir(folder):
            print("❌ Caminho inválido.")
            return

        print("\nEscolha o estilo de texto:")
        for key, (style_name, _) in self.TEXT_STYLES.items():
            print(f"{key} - {style_name}")

        style_choice = input("Opção: ").strip()

        if style_choice not in self.TEXT_STYLES:
            print("❌ Opção inválida para estilo.")
            return

        style_name, style_func = self.TEXT_STYLES[style_choice]

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


register_command("4", FileRenamerStyleCommand())
