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
        folder = input("Enter the folder path: ").strip()

        if not os.path.isdir(folder):
            print("❌ Invalid path.")
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
                end_pos = int(input("Enter the end position (leave blank to go to the end): ").strip() or -1)
            except ValueError:
                print("❌ Invalid positions.")
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
                    print(f"Renamed: {filename} → {new_name}")
                    renamed_count += 1

        print(f"\n✅ {renamed_count} files renamed using pattern: {desc}")
