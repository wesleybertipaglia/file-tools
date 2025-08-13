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

        quality_input = input("Enter image quality (1-95, recommended 80): ").strip()
        try:
            quality = int(quality_input)
            if quality < 1 or quality > 95:
                raise ValueError
        except ValueError:
            print("❌ Invalid quality. Using 80.")
            quality = 80

        path = input("Enter image file or directory path: ").strip()
        path = os.path.normpath(path)

        if os.path.isfile(path):
            self.compress_single_image(path, quality)
        elif os.path.isdir(path):
            self.compress_directory(path, quality)
        else:
            print("❌ Invalid path. Must be a file or directory.")

    def compress_single_image(self, file_path, quality):
        if not self.is_image(file_path):
            print("❌ Not a supported image format.")
            return

        output_folder = os.path.dirname(file_path)
        output_name = f"compressed_{os.path.basename(file_path)}"
        output_path = os.path.join(output_folder, output_name)

        self.compress_image(file_path, output_path, quality)

    def compress_directory(self, folder, quality):
        output_dir = os.path.join(folder, "compressed")
        os.makedirs(output_dir, exist_ok=True)

        images = sorted([
            f for f in os.listdir(folder)
            if os.path.isfile(os.path.join(folder, f)) and self.is_image(f)
        ])

        total = len(images)
        if total == 0:
            print("❌ No supported image files found in the directory.")
            return

        for idx, file in enumerate(images, start=1):
            source_path = os.path.join(folder, file)
            output_path = os.path.join(output_dir, file)
            success = self.compress_image(source_path, output_path, quality, show_status=False)

            if success:
                print(f"{idx} / {total} 📦 Compressed: {file}")
            else:
                print(f"{idx} / {total} ❌ Failed: {file}")

        print(f"\n✅ Total compressed: {total}")

    def compress_image(self, source, destination, quality, show_status=True):
        try:
            with Image.open(source) as img:
                save_kwargs = {"quality": quality}

                if img.format == "JPEG" and img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")

                img.save(destination, img.format, **save_kwargs)

            if show_status:
                print(f"📦 Compressed: {os.path.basename(destination)}")
            return True
        except Exception as e:
            if show_status:
                print(f"❌ Error compressing {os.path.basename(source)}: {e}")
            return False

    def is_image(self, filename):
        return filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'))
