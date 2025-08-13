import os
import re
import shutil
from collections import defaultdict

from engine.tool_command import ToolCommand
from engine.tool_type import ToolType

class RomCleanerCommand(ToolCommand):
    def name(self):
        return "ROM Cleaner & Organizer"

    def type(self):
        return ToolType.ROM

    def run(self, *args, **kwargs):
        path = input("Enter file or directory path: ").strip()
        path = os.path.normpath(path)

        if not os.path.exists(path):
            print("❌ Path does not exist.")
            return

        if os.path.isfile(path):
            folder = os.path.dirname(path)
            files = [os.path.basename(path)]
        elif os.path.isdir(path):
            folder = path
            files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
        else:
            print("❌ Invalid path.")
            return

        print("\n🔄 Renaming files...")
        renamed = self.rename_files(folder, files)

        print("\n📁 Moving duplicates...")
        duplicates = self.move_duplicates(folder)

        print(f"\n✅ Done! {renamed} file(s) renamed, {duplicates} duplicate(s) moved.")

    def rename_files(self, folder, files):
        count = 0
        total = len(files)

        for idx, file in enumerate(sorted(files), 1):
            original_name, ext = os.path.splitext(file)
            normalized_name = self.normalize_name(original_name) + ext.lower()
            src = os.path.join(folder, file)
            dst = os.path.join(folder, normalized_name)

            if src == dst:
                continue

            i = 1
            while os.path.exists(dst):
                normalized_name_alt = f"{self.normalize_name(original_name)}_{i}{ext.lower()}"
                dst = os.path.join(folder, normalized_name_alt)
                i += 1

            os.rename(src, dst)
            print(f"{idx} / {total} Renamed: {file} → {os.path.basename(dst)}")
            count += 1

        return count

    def move_duplicates(self, folder):
        groups = self.group_roms(folder)
        duplicates_dir = os.path.join(folder, "duplicates")
        os.makedirs(duplicates_dir, exist_ok=True)
        moved = 0

        for group_name, files in groups.items():
            if len(files) <= 1:
                continue
            files.sort(key=lambda f: len(f))
            for duplicate in files[1:]:
                src = os.path.join(folder, duplicate)
                dst = os.path.join(duplicates_dir, duplicate)
                shutil.move(src, dst)
                print(f"📦 Moved duplicate: {duplicate}")
                moved += 1

        return moved

    def group_roms(self, folder):
        files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
        groups = defaultdict(list)

        for file in files:
            name, ext = os.path.splitext(file)
            normalized = self.normalize_name(name)
            key = f"{normalized}{ext.lower()}"
            groups[key].append(file)

        return groups

    def detect_region(self, name):
        name = name.lower()
        if "usa" in name:
            return "(U)"
        elif "europe" in name or "eur" in name or "(e)" in name:
            return "(E)"
        elif "japan" in name or "jap" in name or "(j)" in name:
            return "(J)"
        return "(U)"

    def normalize_name(self, name):
        name = re.sub(r"\[.*?\]", "", name)
        name = re.sub(r"\(unl.*?\)", "", name, flags=re.IGNORECASE)
        name = re.sub(r"\(rev.*?\)", "", name, flags=re.IGNORECASE)
        name = re.sub(r"\(v[\d\.]+\)", "", name, flags=re.IGNORECASE)
        name_clean = re.sub(r"\(.*?\)", "", name).strip()
        region = self.detect_region(name)
        return f"{name_clean.strip()} {region}".strip()
