import subprocess

ID = "commit_id"
MESSAGE = "commit_message"


class GitPlugin:

    def __init__(self):
        pass

    @staticmethod
    def get_all_commits_history():
        commits_list = GitPlugin._get_commits_list_from_git()
        return GitPlugin._split_commits(commits_list)

    @staticmethod
    def _get_commits_list_from_git():
        return subprocess.check_output(["git", "log", "--pretty=format:%H|%s"]).splitlines()

    @staticmethod
    def _split_commits(commits_list):
        commits = []
        for commit in commits_list:
            split_commit = commit.split("|", 1)
            commits.append({
                ID: split_commit[0],
                MESSAGE: split_commit[1]
            })
        return commits
