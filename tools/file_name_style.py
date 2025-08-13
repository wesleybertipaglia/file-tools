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
        return "Rename Files (Text Style)"

    def type(self):
        return ToolType.FILE

    def run(self, *args, **kwargs):
        path = input("Enter file or directory path: ").strip()
        path = os.path.normpath(path)

        if not os.path.exists(path):
            print("❌ Path does not exist.")
            return

        print("\nChoose the text style:")
        for key, (style_name, _) in self.TEXT_STYLES.items():
            print(f"{key} - {style_name}")

        style_choice = input("Option: ").strip()

        if style_choice not in self.TEXT_STYLES:
            print("❌ Invalid style option.")
            return

        style_name, style_func = self.TEXT_STYLES[style_choice]

        renamed_count = 0

        if os.path.isfile(path):
            renamed = self.rename_file(path, style_func)
            if renamed:
                print(f"1 / 1 Renamed: {renamed}")
                renamed_count = 1

        elif os.path.isdir(path):
            files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
            total = len(files)

            for idx, filename in enumerate(files, start=1):
                full_path = os.path.join(path, filename)
                result = self.rename_file(full_path, style_func)
                if result:
                    print(f"{idx} / {total} Renamed: {result}")
                    renamed_count += 1
        else:
            print("❌ Path is not a file or directory.")
            return

        print(f"\n✅ {renamed_count} file(s) renamed using style: {style_name}")

    def rename_file(self, full_path, style_func):
        filename = os.path.basename(full_path)
        folder = os.path.dirname(full_path)

        name, ext = os.path.splitext(filename)
        new_name = style_func(name) + ext

        if new_name != filename:
            new_full_path = os.path.join(folder, new_name)
            os.rename(full_path, new_full_path)
            return f"{filename} → {new_name}"
        return None
