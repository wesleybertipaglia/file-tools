import os
import zipfile

def run():
    folder_path = input("Digite o caminho da pasta: ").strip()
    folder_path = os.path.normpath(folder_path)

    if not os.path.isdir(folder_path):
        print(f"❌ Erro: '{folder_path}' não é uma pasta válida.")
        return

    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            zip_path = os.path.join(root, f"{os.path.splitext(file)[0]}.zip")

            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(file_path, arcname=file)

            print(f"📦 Arquivo compactado: {zip_path}")
