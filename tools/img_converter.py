import os
from PIL import Image

from engine.tool_command import ToolCommand
from engine.tool_type import ToolType

class ImgConverterCommand(ToolCommand):
    VALID_FORMATS = ['JPEG', 'PNG', 'BMP', 'TIFF', 'WEBP']

    def name(self):
        return "Convert Images"

    def type(self):
        return ToolType.IMAGE

    def run(self, *args, **kwargs):
        print("📷 Image Converter")

        output_format = input(f"Choose output format {self.VALID_FORMATS} (default JPEG): ").strip().upper()
        if not output_format:
            output_format = "JPEG"

        if output_format not in self.VALID_FORMATS:
            print("❌ Invalid format. Using JPEG.")
            output_format = "JPEG"

        quality = 80
        if output_format == "JPEG":
            try:
                quality = int(input("Enter quality for JPEG (1-95, default 80): ").strip())
                if quality < 1 or quality > 95:
                    raise ValueError
            except ValueError:
                print("❌ Invalid quality. Using 80.")
                quality = 80

        choice = input("Convert a single image (1) or entire directory (2)? ").strip()

        if choice == "1":
            self.convert_single_image(output_format, quality)
        elif choice == "2":
            self.convert_directory(output_format, quality)
        else:
            print("❌ Invalid option.")

    def convert_single_image(self, fmt, quality):
        file_path = input("Enter the image path: ").strip()
        if not os.path.isfile(file_path):
            print("❌ Invalid file.")
            return

        output_name = os.path.splitext(os.path.basename(file_path))[0] + "." + fmt.lower()
        output_folder = os.path.dirname(file_path)
        output_path = os.path.join(output_folder, output_name)

        self.convert_image(file_path, output_path, fmt, quality)

    def convert_directory(self, fmt, quality):
        folder = input("Enter the folder path: ").strip()
        if not os.path.isdir(folder):
            print("❌ Invalid folder.")
            return

        output_dir = os.path.join(folder, "converted")
        os.makedirs(output_dir, exist_ok=True)

        files = sorted(os.listdir(folder))
        count = 0

        for file in files:
            file_path = os.path.join(folder, file)
            if os.path.isfile(file_path) and file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp')):
                output_name = os.path.splitext(file)[0] + "." + fmt.lower()
                output_path = os.path.join(output_dir, output_name)
                self.convert_image(file_path, output_path, fmt, quality)
                count += 1

        print(f"\n✅ Total converted: {count}")

    def convert_image(self, source, destination, fmt, quality):
        try:
            with Image.open(source) as img:
                if img.mode in ("RGBA", "P") and fmt == "JPEG":
                    img = img.convert("RGB")

                save_kwargs = {"quality": quality} if fmt == "JPEG" else {}
                img.save(destination, fmt, **save_kwargs)

            print(f"✅ Converted: {os.path.basename(destination)}")
        except Exception as e:
            print(f"❌ Error converting {os.path.basename(source)}: {e}")
