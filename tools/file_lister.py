import os

from engine import tool_command
from engine import tool_type

class ListFilesCommand(tool_command.ToolCommand):
    def name(self):
        return "List Files"

    def type(self):
        return tool_type.ToolType.FILE

    def run(self, *args, **kwargs) -> str:
        folder_path = input("Enter the folder path: ").strip()

        if not os.path.isdir(folder_path):
            print("❌ Invalid path.")
            return

        files = sorted(os.listdir(folder_path))

        print("\nFiles in the folder:")
        for filename in files:
            print(f" - {filename}")

        save_to_file = input("\nDo you want to save this list to a .txt file? (y/n): ").strip().lower()

        if save_to_file == "y":
            file_name = input("Enter the TXT file name (without extension): ").strip()
            if not file_name:
                file_name = "file_list"

            output_path = os.path.join(folder_path, f"{file_name}.txt")

            try:
                with open(output_path, "w", encoding="utf-8") as f:
                    for filename in files:
                        f.write(filename + "\n")
                print(f"✅ List saved to: {output_path}")
            except Exception as e:
                print(f"❌ Error saving file: {e}")