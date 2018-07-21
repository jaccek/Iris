import getopt
import sys
from subprocess import check_output

import rx

from calculation_store import CalculationStore
from changelog.changelog_generator import ChangelogGenerator
from changes_detector import ChangesDetector


def get_commits_history():      # TODO: move operations on commits to separate module
    return check_output(["git", "log", "--pretty=format:%H|%s"]).splitlines()


def convert_commits_to_list_of_messages(commits_history):
    return list(rx.Observable.from_(commits_history)
                .map(lambda it: it.split("|", 1)[1])
                .to_blocking())


def generate_changelog(commits_messages, current_version, previous_version):
    generator = ChangelogGenerator()
    generator.generate_changelog(commits_messages, current_version, previous_version)


if __name__ == '__main__':
    # parse params
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hc", ["help", "changelog-only"])
    except getopt.GetoptError:
        print 'iris -c'
        sys.exit(2)

    changelog_only = False

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print "TODO: help"      # TODO: help
            sys.exit()
        elif opt in ("-c", "--changelog-only"):
            changelog_only = True
        else:
            print "Unknown argument: " + opt
            sys.exit(2)

    # calculate changelog
    calculation_store = CalculationStore()
    prev_version = calculation_store.get_previous_version()
    last_commit = calculation_store.get_last_commit()

    commits_history = get_commits_history()

    first_index = 0         # TODO: move to separate module
    index = 0
    for commit in commits_history:
        if commit.startswith(last_commit):
            first_index = index
            break
        index += 1
    commits_history = commits_history[:first_index]

    commits_messages = convert_commits_to_list_of_messages(commits_history)

    if changelog_only:
        version = "UNRELEASED"
    else:
        split_version = prev_version.split('.')
        changes_detector = ChangesDetector(int(split_version[0]), int(split_version[1]), int(split_version[2]))
        changes_detector.detect_changes(commits_messages)

        version = "{0}.{1}.{2}".format(changes_detector.new_major_version,
                                       changes_detector.new_minor_version,
                                       changes_detector.new_patch_version)

    generate_changelog(commits_messages, version, prev_version)

    if not changelog_only:
        calculation_store.save_current_version_for_future_calculations(version, commits_history)
