import os
import shutil

def copy_files_with_hierarchy(source_dir, destination_dir, delimiter='.'):
    # Ensure destination directory exists
    os.makedirs(destination_dir, exist_ok=True)

    # empty the destination directory before copying files
    try:
        if os.path.isfile(destination_dir) or os.path.islink(destination_dir):
            os.unlink(destination_dir)  # Remove the file or symbolic link
        print("Folder emptied successfully")
    except Exception as e:
        print("Error emptying folder:", e)

    
    # Walk through the source directory and copy files to destination directory
    for root, _, files in os.walk(source_dir):
        for file in files:
            source_path = os.path.join(root, file)

            # Check if the current file is within the excluded subfolder
            if "archive" in root:
                print(f"Skipping '{file}' as it is in an excluded subfolder.")
                continue
            
            # Construct the destination file name using subdirectory names
            relative_path = os.path.relpath(root, source_dir)
            new_file_name = relative_path.replace(os.sep, delimiter) + delimiter + file
            
            destination_path = os.path.join(destination_dir, new_file_name)
            
            # Copy the file to the destination directory
            shutil.copyfile(source_path, destination_path)
            print(f"Copied '{source_path}' to '{destination_path}'")

# Define source and destination directories
source_directory = '../docs-help-pr'
destination_directory = './local-index'

# Call the function to copy files with hierarchy
copy_files_with_hierarchy(source_directory, destination_directory)
