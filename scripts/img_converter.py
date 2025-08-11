import os
from PIL import Image

def converter_imagens(folder, resize=False, largura=500, altura=500):
    output_dir = os.path.join(folder, "convertidas")
    os.makedirs(output_dir, exist_ok=True)

    arquivos = sorted(os.listdir(folder))
    imagens_convertidas = 0

    for filename in arquivos:
        caminho_completo = os.path.join(folder, filename)

        if not os.path.isfile(caminho_completo):
            continue

        if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp')):
            continue

        try:
            with Image.open(caminho_completo) as img:
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")

                if resize:
                    img = img.resize((largura, altura), Image.LANCZOS)

                nome_arquivo = os.path.splitext(filename)[0] + ".jpg"
                caminho_saida = os.path.join(output_dir, nome_arquivo)

                img.save(caminho_saida, "JPEG", quality=80)

                print(f"✅ Convertido: {nome_arquivo}")
                imagens_convertidas += 1

        except Exception as e:
            print(f"❌ Erro ao processar {filename}: {e}")

    print(f"\nTotal de imagens convertidas: {imagens_convertidas}")
    print(f"Imagens salvas em: {output_dir}")

def run():
    print("📷 Conversor de imagens para JPG + Compressão 80%")
    folder = input("Digite o caminho da pasta com as imagens: ").strip()

    if not os.path.isdir(folder):
        print("❌ Caminho inválido.")
        return

    resize_input = input("Deseja redimensionar as imagens? (s/n): ").strip().lower()
    resize = resize_input == "s"

    largura = altura = 500
    if resize:
        try:
            largura = int(input("Digite a largura (px): ").strip())
            altura = int(input("Digite a altura (px): ").strip())
        except ValueError:
            print("❌ Altura ou largura inválida. Usando 500x500 como padrão.")
            largura, altura = 500, 500

    converter_imagens(folder, resize=resize, largura=largura, altura=altura)
