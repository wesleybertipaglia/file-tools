import os
import shutil

from engine.tool_command import ToolCommand
from engine.tool_type import ToolType

class FlattenDirectoryCommand(ToolCommand):
    def name(self):
        return "Flatten Directory (Move Files to Root)"

    def type(self):
        return ToolType.FILE

    def run(self, *args, **kwargs):
        path = input("Enter the root folder path: ").strip()
        path = os.path.normpath(path)

        if not os.path.exists(path):
            print("❌ Path does not exist.")
            return

        if os.path.isfile(path):
            print("❌ Path is a file. Please provide a directory.")
            return

        files_moved = self.move_all_files_to_root(path)
        print(f"\n✅ Total files moved: {files_moved}")

    def move_all_files_to_root(self, root_dir):
        count = 0
        index = 1

        for current_dir, _, files in os.walk(root_dir):
            if current_dir == root_dir:
                continue

            for file in files:
                src = os.path.join(current_dir, file)
                dst = os.path.join(root_dir, file)

                if os.path.exists(dst):
                    name, ext = os.path.splitext(file)
                    i = 1
                    while os.path.exists(dst):
                        new_name = f"{name}_{i}{ext}"
                        dst = os.path.join(root_dir, new_name)
                        i += 1

                shutil.move(src, dst)
                print(f"{index} 📁 Moved: {file}")
                count += 1
                index += 1

        return count
