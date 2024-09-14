import subprocess

def run_other_scripts():
    try:
        subprocess.run(['python', 'git-update.py'])
        print("git-update.py executed successfully")
    except subprocess.CalledProcessError as e:
        print("Error executing git-update.py:", e)
        return

    try:
        subprocess.run(['python', 'make-local-index.py'])
        print("make-local-index.py executed successfully")
    except subprocess.CalledProcessError as e:
        print("Error executing make-local-index.py:", e)
        return

    try:
        subprocess.run(['python', 'blob-upload.py'])
        print("blob-upload.py executed successfully")
    except subprocess.CalledProcessError as e:
        print("Error executing blob-upload.py:", e)
        return

    try:
        subprocess.run(['python', 'indexer-run.py'])
        print("indexer-run.py executed successfully")
    except subprocess.CalledProcessError as e:
        print("Error executing indexer-run.py:", e)
        return

# Example usage:
run_other_scripts()
