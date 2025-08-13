import os
from PIL import Image

from engine.tool_command import ToolCommand
from engine.tool_type import ToolType

class ImgResizerCommand(ToolCommand):
    def name(self):
        return "Resize Images"

    def type(self):
        return ToolType.IMAGE

    def run(self, *args, **kwargs):
        print("🔧 Image Resizer")

        try:
            width = int(input("Enter width (px): ").strip())
        except ValueError:
            print("❌ Invalid width.")
            return

        use_ratio = input("Do you want to specify a proportion (y/n)? ").strip().lower()
        if use_ratio == 'y':
            ratio_input = input("Enter the proportion (e.g., 16/9): ").strip()
            try:
                x, y = map(int, ratio_input.split("/"))
                height = int((width * y) / x)
                print(f"📐 Calculated height based on ratio {x}/{y}: {height}px")
            except Exception:
                print("❌ Invalid ratio.")
                return
        else:
            try:
                height = int(input("Enter height (px): ").strip())
            except ValueError:
                print("❌ Invalid height.")
                return

        path = input("Enter file or directory path: ").strip()
        path = os.path.normpath(path)

        if os.path.isfile(path):
            self.resize_single_image(path, width, height)
        elif os.path.isdir(path):
            self.resize_directory(path, width, height)
        else:
            print("❌ Path is not a valid file or directory.")

    def resize_single_image(self, file_path, width, height):
        if not self.is_image(file_path):
            print("❌ Not a supported image format.")
            return

        output_name = os.path.splitext(os.path.basename(file_path))[0] + f"_resized{os.path.splitext(file_path)[1]}"
        output_folder = os.path.dirname(file_path)
        output_path = os.path.join(output_folder, output_name)

        self.resize_image(file_path, output_path, width, height, show_status=True)

    def resize_directory(self, folder, width, height):
        output_dir = os.path.join(folder, "resized")
        os.makedirs(output_dir, exist_ok=True)

        files = sorted([
            f for f in os.listdir(folder)
            if os.path.isfile(os.path.join(folder, f)) and self.is_image(f)
        ])

        total = len(files)
        if total == 0:
            print("❌ No supported image files found in the directory.")
            return

        for idx, file in enumerate(files, start=1):
            file_path = os.path.join(folder, file)
            output_name = os.path.splitext(file)[0] + f"_resized{os.path.splitext(file)[1]}"
            output_path = os.path.join(output_dir, output_name)

            success = self.resize_image(file_path, output_path, width, height, show_status=False)

            if success:
                print(f"{idx} / {total} ✅ Resized: {output_name}")
            else:
                print(f"{idx} / {total} ❌ Failed: {file}")

        print(f"\n✅ Total resized: {total}")

    def resize_image(self, source, destination, width, height, show_status=True):
        try:
            with Image.open(source) as img:
                img = img.resize((width, height), Image.LANCZOS)
                img.save(destination)
            if show_status:
                print(f"✅ Resized: {os.path.basename(destination)}")
            return True
        except Exception as e:
            if show_status:
                print(f"❌ Error resizing {os.path.basename(source)}: {e}")
            return False

    def is_image(self, filename):
        return filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp'))
