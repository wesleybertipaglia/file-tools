import os
import zipfile

from engine.tool_command import ToolCommand
from engine.tool_registry import register_command
from engine.tool_type import ToolType

class FileZipperCommand(ToolCommand):
    def name(self):
        return "Compress Files"

    def type(self):
        return ToolType.FILE

    def run(self, *args, **kwargs):
        folder_path = input("Enter the folder path: ").strip()
        folder_path = os.path.normpath(folder_path)

        if not os.path.isdir(folder_path):
            print(f"❌ Error: '{folder_path}' is not a valid folder.")
            return

        print("\nChoose an option:")
        print("1. Compress a single file")
        print("2. Compress all files in the directory")
        choice = input("Enter 1 or 2: ").strip()

        if choice == "1":
            self.zip_single_file(folder_path)
        elif choice == "2":
            self.zip_all_files(folder_path)
        else:
            print("❌ Invalid option.")

    def zip_single_file(self, folder_path):
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

        if not files:
            print("❌ No files found in the folder.")
            return

        print("\nAvailable files:")
        for i, file in enumerate(files, 1):
            print(f"{i}. {file}")

        try:
            choice = int(input("\nEnter the number of the file you want to zip: "))
            if choice < 1 or choice > len(files):
                print("❌ Invalid choice.")
                return
        except ValueError:
            print("❌ Invalid input. Please enter a number.")
            return

        file_to_zip = files[choice - 1]
        file_path = os.path.join(folder_path, file_to_zip)
        zip_path = os.path.join(folder_path, f"{os.path.splitext(file_to_zip)[0]}.zip")

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(file_path, arcname=file_to_zip)

        print(f"📦 File compressed: {zip_path}")

    def zip_all_files(self, folder_path):
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zip_path = os.path.join(root, f"{os.path.splitext(file)[0]}.zip")

                with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    zipf.write(file_path, arcname=file)

                print(f"📦 File compressed: {zip_path}")
