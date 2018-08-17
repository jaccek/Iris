import subprocess

ID = "commit_id"
MESSAGE = "commit_message"


class GitPlugin:

    def __init__(self):
        pass

    @staticmethod
    def get_commits_newer_than(last_commit):
        commits = GitPlugin._get_all_commits_history()
        return GitPlugin._filter_calculated_commits(commits, last_commit)

    @staticmethod
    def _get_all_commits_history():
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

    @staticmethod
    def _filter_calculated_commits(commits, last_commit):
        first_index = len(commits)
        index = 0
        for commit in commits:
            if commit[ID] is last_commit:
                first_index = index
                break
            index += 1
        return commits[:first_index]
