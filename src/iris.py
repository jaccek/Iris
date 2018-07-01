from subprocess import check_output

import rx

from changes_detector import ChangesDetector


def get_commits_history():
    return check_output(["git", "log", "--pretty=format:%H|%s"])


def convert_commits_to_list_of_messages(commits_history):
    lines = commits_history.splitlines()
    return list(rx.Observable.from_(lines)
                .map(lambda it: it.split("|", 1)[1])
                .to_blocking())


if __name__ == '__main__':
    commits_history = get_commits_history()
    commits_messages = convert_commits_to_list_of_messages(commits_history)

    version_detector = ChangesDetector(0, 0, 0)
    version_detector.detect_changes(commits_messages)

    version = "{0}.{1}.{2}".format(version_detector.new_major_version,
                                   version_detector.new_minor_version,
                                   version_detector.new_bugfix_version)
    print version
