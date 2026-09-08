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