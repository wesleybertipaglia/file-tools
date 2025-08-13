import os
import zipfile

from engine.tool_command import ToolCommand
from engine.tool_type import ToolType

class FileZipperCommand(ToolCommand):
    def name(self):
        return "Compress Files"

    def type(self):
        return ToolType.FILE

    def run(self, *args, **kwargs):
        path = input("File or directory: ").strip()
        path = os.path.normpath(path)

        if os.path.isdir(path):
            self.zip_all_files(path)
        elif os.path.isfile(path):
            self.zip_single_file(path)
        else:
            print(f"❌ Error: '{path}' is not a valid file or directory.")

    def zip_single_file(self, file_path):
        dir_name = os.path.dirname(file_path)
        file_name = os.path.basename(file_path)
        zip_name = os.path.splitext(file_name)[0] + ".zip"
        zip_path = os.path.join(dir_name, zip_name)

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(file_path, arcname=file_name)

        print(f"📦 File compressed: {zip_path}")

    def zip_all_files(self, folder_path):
        files_to_zip = []
        for root, _, files in os.walk(folder_path):
            for file in files:
                files_to_zip.append(os.path.join(root, file))

        total = len(files_to_zip)
        if total == 0:
            print("❌ No files found in the directory.")
            return

        for idx, file_path in enumerate(files_to_zip, start=1):
            zip_name = os.path.splitext(os.path.basename(file_path))[0] + ".zip"
            zip_path = os.path.join(os.path.dirname(file_path), zip_name)

            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(file_path, arcname=os.path.basename(file_path))

            print(f"{idx} / {total} 📦 File compressed: {zip_path}")
