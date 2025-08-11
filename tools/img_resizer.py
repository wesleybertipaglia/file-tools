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
            height = int(input("Enter height (px): ").strip())
        except ValueError:
            print("❌ Invalid width or height.")
            return

        choice = input("Resize a single image (1) or entire directory (2)? ").strip()

        if choice == "1":
            self.resize_single_image(width, height)
        elif choice == "2":
            self.resize_directory(width, height)
        else:
            print("❌ Invalid option.")

    def resize_single_image(self, width, height):
        file_path = input("Enter the image path: ").strip()
        if not os.path.isfile(file_path):
            print("❌ Invalid file.")
            return

        output_name = os.path.splitext(os.path.basename(file_path))[0] + f"_resized{os.path.splitext(file_path)[1]}"
        output_folder = os.path.dirname(file_path)
        output_path = os.path.join(output_folder, output_name)

        self.resize_image(file_path, output_path, width, height)

    def resize_directory(self, width, height):
        folder = input("Enter the folder path: ").strip()
        if not os.path.isdir(folder):
            print("❌ Invalid folder.")
            return

        output_dir = os.path.join(folder, "resized")
        os.makedirs(output_dir, exist_ok=True)

        files = sorted(os.listdir(folder))
        count = 0

        for file in files:
            file_path = os.path.join(folder, file)
            if os.path.isfile(file_path) and file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp')):
                output_name = os.path.splitext(file)[0] + f"_resized{os.path.splitext(file)[1]}"
                output_path = os.path.join(output_dir, output_name)
                self.resize_image(file_path, output_path, width, height)
                count += 1

        print(f"\n✅ Total resized: {count}")

    def resize_image(self, source, destination, width, height):
        try:
            with Image.open(source) as img:
                img = img.resize((width, height), Image.LANCZOS)
                img.save(destination)
            print(f"✅ Resized: {os.path.basename(destination)}")
        except Exception as e:
            print(f"❌ Error resizing {os.path.basename(source)}: {e}")
