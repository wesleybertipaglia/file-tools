import os
from PIL import Image

from engine.tool_command import ToolCommand
from engine.tool_type import ToolType

class ImgConverterCommand(ToolCommand):
    FORMATOS_VALIDOS = ['JPEG', 'PNG', 'BMP', 'TIFF', 'WEBP']

    def name(self):
        return "Converter Imagens"

    def type(self):
        return ToolType.IMAGE

    def run(self, *args, **kwargs):
        print("📷 Conversor de imagens")

        formato_saida = input(f"Escolha o formato de saída {self.FORMATOS_VALIDOS} (default JPEG): ").strip().upper()
        if not formato_saida:
            formato_saida = "JPEG"

        if formato_saida not in self.FORMATOS_VALIDOS:
            print("❌ Formato inválido. Usando JPEG.")
            formato_saida = "JPEG"

        qualidade = 80
        if formato_saida == "JPEG":
            try:
                qualidade = int(input("Digite a qualidade para JPEG (1-95, padrão 80): ").strip())
                if qualidade < 1 or qualidade > 95:
                    raise ValueError
            except ValueError:
                print("❌ Qualidade inválida. Usando 80.")
                qualidade = 80

        tipo = input("Deseja converter uma única imagem (1) ou todo o diretório (2)? ").strip()

        if tipo == "1":
            self.convert_single_image(formato_saida, qualidade)
        elif tipo == "2":
            self.convert_directory(formato_saida, qualidade)
        else:
            print("❌ Opção inválida.")

    def convert_single_image(self, formato, qualidade):
        arquivo = input("Digite o caminho da imagem: ").strip()
        if not os.path.isfile(arquivo):
            print("❌ Arquivo inválido.")
            return

        nome_saida = os.path.splitext(os.path.basename(arquivo))[0] + "." + formato.lower()
        pasta_saida = os.path.dirname(arquivo)
        caminho_saida = os.path.join(pasta_saida, nome_saida)

        self.convert_image(arquivo, caminho_saida, formato, qualidade)

    def convert_directory(self, formato, qualidade):
        pasta = input("Digite o caminho da pasta: ").strip()
        if not os.path.isdir(pasta):
            print("❌ Pasta inválida.")
            return

        output_dir = os.path.join(pasta, "convertidas")
        os.makedirs(output_dir, exist_ok=True)

        arquivos = sorted(os.listdir(pasta))
        cont = 0

        for arquivo in arquivos:
            caminho_arquivo = os.path.join(pasta, arquivo)
            if os.path.isfile(caminho_arquivo) and arquivo.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp')):
                nome_saida = os.path.splitext(arquivo)[0] + "." + formato.lower()
                caminho_saida = os.path.join(output_dir, nome_saida)
                self.convert_image(caminho_arquivo, caminho_saida, formato, qualidade)
                cont += 1

        print(f"\n✅ Total convertidos: {cont}")

    def convert_image(self, origem, destino, formato, qualidade):
        try:
            with Image.open(origem) as img:
                if img.mode in ("RGBA", "P") and formato == "JPEG":
                    img = img.convert("RGB")

                save_kwargs = {"quality": qualidade} if formato == "JPEG" else {}
                img.save(destino, formato, **save_kwargs)

            print(f"✅ Convertido: {os.path.basename(destino)}")
        except Exception as e:
            print(f"❌ Erro ao converter {os.path.basename(origem)}: {e}")
