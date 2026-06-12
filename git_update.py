from pathlib import Path
import subprocess
from datetime import datetime
import platform


def git_update(commit_message=""):
    current_system = platform.system()
    if current_system == "Windows":
        repo_dir = Path(r"C:\Users\bubble\Desktop\Project\T_sensor\T_sensor")
    else:
        repo_dir = Path("/Users/bubble/Desktop/Project/T_sensor/T_sensor")
    # repo_dir = Path(__file__).resolve().parent
    formatted_time = datetime.now().strftime("%Y%m%d%H%M")

    subprocess.run(["git", "add", "."], cwd=repo_dir, check=True)

    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=repo_dir,
        capture_output=True,
        text=True,
    )

    if result.stdout.strip():
        subprocess.run(
            [
                "git",
                "commit",
                "-m",
                f"feat: auto update {formatted_time} {commit_message}",
            ],
            cwd=repo_dir,
            check=True,
        )

        branch_result = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=repo_dir,
            capture_output=True,
            text=True,
            check=True,
        )
        current_branch = branch_result.stdout.strip()

        subprocess.run(
            ["git", "push", "origin", current_branch],
            cwd=repo_dir,
            check=True,
        )

        print(f"Git push completed on branch: {current_branch}")
    else:
        print("No changes to commit.")


if __name__ == "__main__":
    git_update(commit_message="git test.py")
