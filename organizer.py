import os
import shutil
from pathlib import Path
import time
import schedule

TARGET_FOLDER = Path.home()/"Downloads"

CATEGORIES = {
    "Images":[".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".csv"],
    "Audio": [".mp3", ".wav", ".flac"],
    "Videos": [".mp4", ".mkv", ".mov"],
    "Archives": [".zip", ".tar", ".gz", ".7z"],
    "Executables": [".exe", ".dmg", ".pkg", ".sh"],
    "Code Files": [".html", ".py"]
}

def organize_directory():
    if not TARGET_FOLDER.exists():
        return
    for item in TARGET_FOLDER.iterdir():
        if item.is_dir():
            continue
        file_ext = item.suffix.lower()
        moved = False

        for category, extensions in CATEGORIES.items():
            if file_ext in extensions:
                category_folder = TARGET_FOLDER/category
                category_folder.mkdir(exist_ok=True)

                shutil.move(str(item), str(category_folder / item.name))
                moved = True
                break

        if not moved and file_ext != "":
            others_folder = TARGET_FOLDER/ "Others"
            others_folder.mkdir(exist_ok=True)
            shutil.move(str(item), str(others_folder/item.name))

schedule.every().day.at("20:00").do(organize_directory)

if __name__ == "__main__":
    print("Organizer service running... Press Ctrl+C to stop")
    while True:
        schedule.run_pending()
        time.sleep(60)