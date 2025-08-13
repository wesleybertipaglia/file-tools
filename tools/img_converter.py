import os
from PIL import Image

from engine.tool_command import ToolCommand
from engine.tool_type import ToolType

class ImgConverterCommand(ToolCommand):
    VALID_FORMATS = ['JPEG', 'JPG', 'PNG', 'BMP', 'TIFF', 'WEBP']

    def name(self):
        return "Convert Images"

    def type(self):
        return ToolType.IMAGE

    def run(self, *args, **kwargs):
        print("📷 Image Converter")

        output_format = input(f"Choose output format {self.VALID_FORMATS} (default JPG): ").strip().upper()
        if not output_format:
            output_format = "JPG"

        if output_format not in self.VALID_FORMATS:
            print("❌ Invalid format. Using JPG.")
            output_format = "JPG"

        quality = 80
        if output_format == "JPG" or output_format == "JPEG":
            try:
                quality_input = input("Enter quality (1-95, default 80): ").strip()
                if quality_input:
                    quality = int(quality_input)
                    if quality < 1 or quality > 95:
                        raise ValueError
            except ValueError:
                print("❌ Invalid quality. Using 80.")
                quality = 80

        path = input("Enter the image file or directory path: ").strip()
        path = os.path.normpath(path)

        if os.path.isfile(path):
            self.convert_single_image(path, output_format, quality)
        elif os.path.isdir(path):
            self.convert_directory(path, output_format, quality)
        else:
            print(f"❌ Error: '{path}' is not a valid file or directory.")

    def convert_single_image(self, file_path, fmt, quality):
        output_name = os.path.splitext(os.path.basename(file_path))[0] + "." + fmt.lower()
        output_folder = os.path.dirname(file_path)
        output_path = os.path.join(output_folder, output_name)

        self.convert_image(file_path, output_path, fmt, quality)

    def convert_directory(self, folder, fmt, quality):
        output_dir = os.path.join(folder, "converted")
        os.makedirs(output_dir, exist_ok=True)

        images = sorted([
            f for f in os.listdir(folder)
            if os.path.isfile(os.path.join(folder, f)) and f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp'))
        ])

        total = len(images)
        if total == 0:
            print("❌ No valid image files found in the directory.")
            return

        for idx, file in enumerate(images, start=1):
            file_path = os.path.join(folder, file)
            output_name = os.path.splitext(file)[0] + "." + fmt.lower()
            output_path = os.path.join(output_dir, output_name)
            success = self.convert_image(file_path, output_path, fmt, quality, show_status=False)
            if success:
                print(f"{idx} / {total} ✅ Converted: {output_name}")
            else:
                print(f"{idx} / {total} ❌ Failed: {file}")

        print(f"\n✅ Total converted: {total}")

    def convert_image(self, source, destination, fmt, quality, show_status=True):
        try:
            with Image.open(source) as img:
                if img.mode in ("RGBA", "P") and fmt == "JPEG":
                    img = img.convert("RGB")

                save_kwargs = {"quality": quality} if fmt == "JPEG" else {}
                img.save(destination, fmt, **save_kwargs)

            if show_status:
                print(f"✅ Converted: {os.path.basename(destination)}")
            return True
        except Exception as e:
            if show_status:
                print(f"❌ Error converting {os.path.basename(source)}: {e}")
            return False
