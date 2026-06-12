import subprocess
from datetime import datetime


def git_update(commit_message=""):

    repo_dir = "/Users/bubble/Desktop/Project/T_sensor/T_sensor"

    formatted_time = datetime.now().strftime("%Y%m%d%H%M")

    subprocess.run(
        ["git", "add", "."],
        cwd=repo_dir,
        check=True,
    )

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

        subprocess.run(
            ["git", "push", "origin", "master"],
            cwd=repo_dir,
            check=True,
        )

        print("Git push completed.")

    else:
        print("No changes to commit.")


if __name__ == "__main__":
    git_update(commit_message="git test.py")
