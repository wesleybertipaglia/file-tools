import os
from PIL import Image

from engine.tool_command import ToolCommand
from engine.tool_type import ToolType

class ImgResizerCommand(ToolCommand):
    def name(self):
        return "Redimensionar Imagens"

    def type(self):
        return ToolType.IMAGE

    def run(self, *args, **kwargs):
        print("🔧 Redimensionador de imagens")

        try:
            largura = int(input("Digite a largura (px): ").strip())
            altura = int(input("Digite a altura (px): ").strip())
        except ValueError:
            print("❌ Altura ou largura inválida.")
            return

        tipo = input("Deseja redimensionar uma única imagem (1) ou todo o diretório (2)? ").strip()

        if tipo == "1":
            self.resize_single_image(largura, altura)
        elif tipo == "2":
            self.resize_directory(largura, altura)
        else:
            print("❌ Opção inválida.")

    def resize_single_image(self, largura, altura):
        arquivo = input("Digite o caminho da imagem: ").strip()
        if not os.path.isfile(arquivo):
            print("❌ Arquivo inválido.")
            return

        nome_saida = os.path.splitext(os.path.basename(arquivo))[0] + f"_resized{os.path.splitext(arquivo)[1]}"
        pasta_saida = os.path.dirname(arquivo)
        caminho_saida = os.path.join(pasta_saida, nome_saida)

        self.resize_image(arquivo, caminho_saida, largura, altura)

    def resize_directory(self, largura, altura):
        pasta = input("Digite o caminho da pasta: ").strip()
        if not os.path.isdir(pasta):
            print("❌ Pasta inválida.")
            return

        output_dir = os.path.join(pasta, "redimensionadas")
        os.makedirs(output_dir, exist_ok=True)

        arquivos = sorted(os.listdir(pasta))
        cont = 0

        for arquivo in arquivos:
            caminho_arquivo = os.path.join(pasta, arquivo)
            if os.path.isfile(caminho_arquivo) and arquivo.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp')):
                nome_saida = os.path.splitext(arquivo)[0] + f"_resized{os.path.splitext(arquivo)[1]}"
                caminho_saida = os.path.join(output_dir, nome_saida)
                self.resize_image(caminho_arquivo, caminho_saida, largura, altura)
                cont += 1

        print(f"\n✅ Total redimensionados: {cont}")

    def resize_image(self, origem, destino, largura, altura):
        try:
            with Image.open(origem) as img:
                img = img.resize((largura, altura), Image.LANCZOS)
                img.save(destino)
            print(f"✅ Redimensionado: {os.path.basename(destino)}")
        except Exception as e:
            print(f"❌ Erro ao redimensionar {os.path.basename(origem)}: {e}")

