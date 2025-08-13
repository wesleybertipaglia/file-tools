import os
from engine.tool_command import ToolCommand
from engine.tool_type import ToolType

class FileRenamerFromListCommand(ToolCommand):
    def name(self):
        return "Rename Files from List"

    def type(self):
        return ToolType.FILE

    def run(self, *args, **kwargs):
        txt_path = input("📄 Enter the path to the .txt file with new names: ").strip()
        dir_path = input("📁 Enter the folder path with files to rename: ").strip()

        if not os.path.isfile(txt_path):
            print("❌ .txt file not found.")
            return

        if not os.path.isdir(dir_path):
            print("❌ Invalid directory path.")
            return

        self.rename_files(txt_path, dir_path)

    def rename_files(self, txt_path, dir_path):
        with open(txt_path, 'r', encoding='utf-8') as f:
            new_names = [line.strip() for line in f if line.strip()]

        files = sorted([f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))])

        if len(new_names) != len(files):
            print(f"\n❌ Error: {len(new_names)} names in the TXT file, but {len(files)} files in the directory.\n")
            return

        print("\n🔄 Renaming files...")
        for idx, (old_name, new_name) in enumerate(zip(files, new_names), 1):
            original_ext = os.path.splitext(old_name)[1]
            name_from_txt = os.path.splitext(new_name)[0]
            final_name = name_from_txt + original_ext

            old_path = os.path.join(dir_path, old_name)
            new_path = os.path.join(dir_path, final_name)

            os.rename(old_path, new_path)
            print(f"{idx} ✅ {old_name} → {final_name}")

        print(f"\n✅ All {len(files)} files have been successfully renamed!\n")
