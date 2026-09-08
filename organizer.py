import os
import shutil
from pathlib import Path

CATEGORIES = {
    "Images":[".jpg", ".jpeg", ".png", ".gif", ".svg"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".csv"],
    "Audio": [".mp3", ".wav", ".flac"],
    "Videos": [".mp4", ".mkv", ".mov"],
    "Archives": [".zip", ".tar", ".gz", ".7z"],
    "Executables": [".exe", ".dmg", ".pkg", ".sh"]
}

def organize_directory(directory_path):
    target_dir = Path(directory_path)

    if not target_dir.exists():
        print(f"Error: The path {directory_path} does not exist")
        return
    for item in target_dir.iterdir():
        if item.is_dir():
            continue
        file_ext = item.suffix.lower()
        moved = False

        for category, extensions in CATEGORIES.items():
            if file_ext in extensions:
                category_folder = target_dir/category
                category_folder.mkdir(exist_ok=True)

                shutil.move(str(item), str(category_folder / item.name))
                print(f"Moved {item.name} -> {category}/")
                moved = True
                break
        if not moved and file_ext != "":
            others_folder = target_dir/ "Others"
            others_folder.mkdir(exist_ok=True)
            shutil.move(str(item), str(others_folder/item.name))
            print(f"Moved: {item.name} -> Others/")
if __name__ == "__main__":
    folder_to_clean = input("Enter the full path of the folder to organize: ").strip()
    organize_directory(folder_to_clean)