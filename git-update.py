import subprocess

def git_pull(repo_path):
    try:
        subprocess.check_call(['git', '-C', repo_path, 'pull', 'upstream', 'main'])
        print("Pull successful")
    except subprocess.CalledProcessError as e:
        print("Error pulling changes:", e)

# Example usage:
repo_path = '../docs-help-pr/'
git_pull(repo_path)