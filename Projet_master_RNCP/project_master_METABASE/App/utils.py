import shutil
from pathlib import Path
from datetime import datetime
import subprocess
import os


def stop_metabase():
    print("[INFO] Stop Metabase docker container")
    subprocess.run(["docker", "stop", "metabase"], check=True)
    return "done"

def start_metabase():
    print("[INFO] Start Metabase docker container")
    subprocess.run(["docker", "start", "metabase"], check=True)
    return "done"

def delete_metabase_db_in_container(container_name="metabase", db_path="/metabase.db"):
    print(f"[INFO] Delete directory {db_path} inside container {container_name}...")
    try:
        subprocess.run(["docker", "exec", container_name, "rm", "-rf", db_path], check=True)
        print("[INFO] Deletion successful inside the container.")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to delete inside the container: {e}")
    return "done"


def copy_metabase_db_from_container():
    os.makedirs("./outputs", exist_ok=True)
    date_str = datetime.now().strftime("%Y_%m_%d")
    file_name = "metabase.db_" + date_str
    destination_path = Path("./outputs") / file_name
    print(f"[INFO] Copying '/metabase.db' from container metabase to {destination_path} on host...")
    try:
        # Remove destination folder if it already exists (optional)
        if destination_path.exists():
            print(f"[INFO] Removing existing directory {destination_path}...")
            subprocess.run(["rm", "-rf", str(destination_path)], check=True)
        # Copy folder from container to host
        subprocess.run(["docker", "cp", "metabase:/metabase.db", str(destination_path)], check=True)
        print("[INFO] Copy completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to copy directory from container: {e}")
    return "done"