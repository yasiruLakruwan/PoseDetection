from pathlib import Path
import os

lists_to_genarate = [
    Path("app.py"),
    Path("src/vision/pose_detector.py"),
    Path("src/vision/bed_detector.py"),
    Path("src/vision/feature_extractor.py"),
    Path("src/state_machine/states.py"),
    Path("src/state_machine/activity_fsm.py"),
    Path("src/agent/memory.py"),
    Path("config/settings.py"),
    Path("src/logger.py"),
    Path("src/custom_exeption.py"),
    Path("utils/drawing.py"),
    Path("setup.py"),
    "videos/",
    "requirements.txt"
    ""
]


for dir in lists_to_genarate:
    dir_name,filename = os.path.split(dir)
    print(f"dir name: {dir_name}" )
    print(f"filename: {filename}")

    if dir_name:
        os.makedirs(dir_name,exist_ok=True)

    if filename:
        file_path = os.path.join(dir_name, filename)
        open(file_path,'a').close()