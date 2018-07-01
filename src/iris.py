import os
import sys

from subprocess import call, check_output


def get_commits_history():
    return check_output(["git", "log", "--pretty=format:%H|%s"])


if __name__ == '__main__':
    commits_history = get_commits_history()
    print commits_history
