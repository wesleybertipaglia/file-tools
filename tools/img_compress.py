import os
from PIL import Image

from engine.tool_command import ToolCommand
from engine.tool_type import ToolType

class ImgCompressCommand(ToolCommand):
    def name(self):
        return "Compress Images"

    def type(self):
        return ToolType.IMAGE

    def run(self, *args, **kwargs):
        print("🗜️ Image Compressor")

        quality = input("Enter image quality (1-95, recommended 80): ").strip()
        try:
            quality = int(quality)
            if quality < 1 or quality > 95:
                raise ValueError
        except ValueError:
            print("❌ Invalid quality. Using 80.")
            quality = 80

        choice = input("Compress a single image (1) or entire directory (2)? ").strip()

        if choice == "1":
            self.compress_single_image(quality)
        elif choice == "2":
            self.compress_directory(quality)
        else:
            print("❌ Invalid option.")

    def compress_single_image(self, quality):
        file_path = input("Enter the image path: ").strip()
        if not os.path.isfile(file_path):
            print("❌ Invalid file.")
            return

        output_folder = os.path.dirname(file_path)
        output_name = os.path.basename(file_path)
        output_path = os.path.join(output_folder, f"compressed_{output_name}")

        self.compress_image(file_path, output_path, quality)

    def compress_directory(self, quality):
        folder = input("Enter the folder path containing images: ").strip()
        if not os.path.isdir(folder):
            print("❌ Invalid folder.")
            return

        output_dir = os.path.join(folder, "compressed")
        os.makedirs(output_dir, exist_ok=True)

        files = sorted(os.listdir(folder))
        count = 0
        for file in files:
            file_path = os.path.join(folder, file)
            if os.path.isfile(file_path) and file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp')):
                output_path = os.path.join(output_dir, file)
                self.compress_image(file_path, output_path, quality)
                count += 1

        print(f"\n✅ Total compressed: {count}")

    def compress_image(self, source, destination, quality):
        try:
            with Image.open(source) as img:
                save_kwargs = {}
                save_kwargs["quality"] = quality

                img.save(destination, img.format, **save_kwargs)
            print(f"📦 Compressed: {os.path.basename(destination)}")
        except Exception as e:
            print(f"❌ Error compressing {os.path.basename(source)}: {e}")
