import os
import shutil

# Define paths
source_dir = "runs/detect"  # Folder where training results are stored
destination_dir = "labels_summary"  # New folder to store labels

# Ensure destination folder exists
os.makedirs(destination_dir, exist_ok=True)

# Loop through training runs
for train_version in sorted(os.listdir(source_dir)):
    train_path = os.path.join(source_dir, train_version)

    # Check if it's a valid training run folder
    if os.path.isdir(train_path):
        labels_path = os.path.join(train_path, "labels.jpg")
        correlogram_path = os.path.join(train_path, "labels_correlogram.jpg")

        if os.path.exists(labels_path) and os.path.exists(correlogram_path):
            # Create a subfolder for this training version
            version_folder = os.path.join(destination_dir, train_version)
            os.makedirs(version_folder, exist_ok=True)

            # Copy images to the new folder
            shutil.copy(labels_path, os.path.join(version_folder, "labels.jpg"))
            shutil.copy(correlogram_path, os.path.join(version_folder, "labels_correlogram.jpg"))

print("Labels images copied successfully!")
