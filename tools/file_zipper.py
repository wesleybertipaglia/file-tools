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
            self.zip_all_items_in_root(path)
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

    def zip_all_items_in_root(self, folder_path):
        items = os.listdir(folder_path)
        if not items:
            print("❌ No items found in the directory.")
            return

        total = len(items)

        for idx, item in enumerate(items, start=1):
            item_path = os.path.join(folder_path, item)
            zip_name = os.path.splitext(item)[0] + ".zip"
            zip_path = os.path.join(folder_path, zip_name)

            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                if os.path.isfile(item_path):
                    zipf.write(item_path, arcname=item)
                elif os.path.isdir(item_path):
                    for sub_item in os.listdir(item_path):
                        sub_item_path = os.path.join(item_path, sub_item)
                        arcname = os.path.join(item, sub_item)
                        if os.path.isfile(sub_item_path):
                            zipf.write(sub_item_path, arcname=arcname)

            print(f"{idx} / {total} 📦 Compressed: {zip_path}")
