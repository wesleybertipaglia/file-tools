from engine.tool_registry import register_command
from tools import file_lister, file_zipper, file_name_style, file_name_remover
from tools import img_compress, img_converter, img_resizer

# file commands
register_command("1", file_lister.ListFilesCommand())
register_command("2", file_zipper.FileZipperCommand())
register_command("3", file_name_style.FileRenamerStyleCommand())
register_command("4", file_name_remover.FileRenamerPatternCommand())

# img commands
register_command("1", img_compress.ImgCompressCommand())
register_command("2", img_converter.ImgConverterCommand())
register_command("3", img_resizer.ImgResizerCommand())
