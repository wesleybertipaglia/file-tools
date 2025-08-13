import os
import re

from engine.tool_command import ToolCommand
from engine.tool_type import ToolType

class FileRenamerPatternCommand(ToolCommand):
    PATTERNS = {
        "1": ("Remove numbers", r"\d"),
        "2": ("Remove special characters", r"[^\w\s]"),
        "3": ("Remove exact text", None),
        "4": ("Custom regex", None),
    }

    def name(self):
        return "Rename Files (Removal Pattern)"

    def type(self):
        return ToolType.FILE

    def run(self, *args, **kwargs):
        path = input("Enter file or directory path: ").strip()
        path = os.path.normpath(path)

        if not os.path.exists(path):
            print("❌ Path does not exist.")
            return

        print("\nChoose the removal pattern:")
        for key, (desc, _) in self.PATTERNS.items():
            print(f"{key} - {desc}")

        choice = input("Option: ").strip()
        if choice not in self.PATTERNS:
            print("❌ Invalid option.")
            return

        desc, pattern = self.PATTERNS[choice]

        if choice == "3":
            text_to_remove = input("Enter the exact text to remove: ").strip()
            pattern = re.escape(text_to_remove)
        elif choice == "4":
            pattern = input("Enter your custom regex: ").strip()

        start_pos = None
        end_pos = None
        if choice != "4":
            try:
                start_pos = int(input("Enter the start position (starting at 0): ").strip())
                end_input = input("Enter the end position (leave blank to go to the end): ").strip()
                end_pos = int(end_input) if end_input else -1
            except ValueError:
                print("❌ Invalid positions.")
                return

        regex = re.compile(pattern)
        renamed_count = 0

        if os.path.isfile(path):
            renamed = self.rename_file(path, regex, choice, start_pos, end_pos)
            if renamed:
                print(f"1 / 1 Renamed: {renamed}")
                renamed_count = 1
        elif os.path.isdir(path):
            files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
            total = len(files)

            for idx, filename in enumerate(files, start=1):
                full_path = os.path.join(path, filename)
                result = self.rename_file(full_path, regex, choice, start_pos, end_pos)
                if result:
                    print(f"{idx} / {total} Renamed: {result}")
                    renamed_count += 1
        else:
            print("❌ Path is not a file or directory.")
            return

        print(f"\n✅ {renamed_count} file(s) renamed using pattern: {desc}")

    def rename_file(self, full_path, regex, choice, start_pos=None, end_pos=None):
        filename = os.path.basename(full_path)
        folder = os.path.dirname(full_path)

        if choice != "4":
            target_segment = filename[start_pos:end_pos if end_pos != -1 else None]
            new_segment = regex.sub("", target_segment)
            new_name = filename[:start_pos] + new_segment + (filename[end_pos:] if end_pos != -1 else "")
        else:
            new_name = regex.sub("", filename)

        if new_name != filename:
            new_full_path = os.path.join(folder, new_name)
            os.rename(full_path, new_full_path)
            return f"{filename} → {new_name}"
        return None
