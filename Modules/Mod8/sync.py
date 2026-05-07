import os
import shutil
import time

# Paths
BASE_DIR = os.path.dirname(__file__)

RECORDS_DIR = os.path.join(BASE_DIR, "offline_storage", "records")
SYNCED_DIR = os.path.join(BASE_DIR, "offline_storage", "synced")


def ensure_directories():
    os.makedirs(RECORDS_DIR, exist_ok=True)
    os.makedirs(SYNCED_DIR, exist_ok=True)


def simulate_server_upload(file_path):
    print(f"Uploading {os.path.basename(file_path)} to server...")
    time.sleep(1)  # simulate delay
    print("Upload successful!\n")
    return True


def sync_records():
    files = os.listdir(RECORDS_DIR)

    if not files:
        print("No records to sync.")
        return

    print(f"Found {len(files)} file(s) to sync...\n")

    for file in files:
        file_path = os.path.join(RECORDS_DIR, file)

        # Upload simulation
        success = simulate_server_upload(file_path)

        if success:
            # Move file to synced folder
            destination = os.path.join(SYNCED_DIR, file)
            shutil.move(file_path, destination)
            print(f"Moved {file} → synced folder\n")
        else:
            print(f"Failed to sync {file}\n")


if __name__ == "__main__":
    ensure_directories()
    sync_records()