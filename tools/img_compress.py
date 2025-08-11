import os
from PIL import Image

from engine.tool_command import ToolCommand
from engine.tool_type import ToolType

class ImgCompressCommand(ToolCommand):
    def name(self):
        return "Comprimir Imagens"

    def type(self):
        return ToolType.IMAGE

    def run(self, *args, **kwargs):
        print("🗜️ Compressor de imagens")

        qualidade = input("Digite a qualidade para JPEG (1-95, recomendável 80): ").strip()
        try:
            qualidade = int(qualidade)
            if qualidade < 1 or qualidade > 95:
                raise ValueError
        except ValueError:
            print("❌ Qualidade inválida. Usando 80.")
            qualidade = 80

        tipo = input("Deseja comprimir uma única imagem (1) ou todo o diretório (2)? ").strip()

        if tipo == "1":
            self.compress_single_image(qualidade)
        elif tipo == "2":
            self.compress_directory(qualidade)
        else:
            print("❌ Opção inválida.")

    def compress_single_image(self, qualidade):
        arquivo = input("Digite o caminho da imagem: ").strip()
        if not os.path.isfile(arquivo):
            print("❌ Arquivo inválido.")
            return

        pasta_saida = os.path.dirname(arquivo)
        nome_saida = os.path.basename(arquivo)
        caminho_saida = os.path.join(pasta_saida, f"comprimido_{nome_saida}")

        self.compress_image(arquivo, caminho_saida, qualidade)

    def compress_directory(self, qualidade):
        pasta = input("Digite o caminho da pasta com imagens: ").strip()
        if not os.path.isdir(pasta):
            print("❌ Pasta inválida.")
            return

        output_dir = os.path.join(pasta, "comprimidas")
        os.makedirs(output_dir, exist_ok=True)

        arquivos = sorted(os.listdir(pasta))
        cont = 0
        for arquivo in arquivos:
            caminho_arquivo = os.path.join(pasta, arquivo)
            if os.path.isfile(caminho_arquivo) and arquivo.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp')):
                caminho_saida = os.path.join(output_dir, arquivo)
                self.compress_image(caminho_arquivo, caminho_saida, qualidade)
                cont += 1

        print(f"\n✅ Total comprimidos: {cont}")

    def compress_image(self, origem, destino, qualidade):
        try:
            with Image.open(origem) as img:
                formato = img.format
                save_kwargs = {}
                if formato == "JPEG":
                    save_kwargs["quality"] = qualidade

                img.save(destino, formato, **save_kwargs)
            print(f"📦 Comprimido: {os.path.basename(destino)}")
        except Exception as e:
            print(f"❌ Erro ao comprimir {os.path.basename(origem)}: {e}")
