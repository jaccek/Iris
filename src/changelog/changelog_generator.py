import rx

from changelog_printer import ChangelogPrinter
import change_type


class ChangelogGenerator:

    def __init__(self):
        pass

    def generate_changelog(self, commits_messages, current_version, previous_version):
        changes = {
            change_type.ADDED: [],
            change_type.CHANGED: [],
            change_type.DEPRECATED: [],
            change_type.REMOVED: [],
            change_type.FIXED: [],
            change_type.SECURITY: []
        }

        switcher = {
            "bc": change_type.ADDED,
            "chore": change_type.CHANGED,
            "deprecate": change_type.DEPRECATED,
            "feat": change_type.ADDED,
            "fix": change_type.FIXED,
            "perf": change_type.CHANGED,
            "refactor": change_type.CHANGED,
            "remove": change_type.REMOVED,
            "revert": change_type.REMOVED,
            "security": change_type.SECURITY,
            "style": change_type.CHANGED

            # skipping:
            #  "build"
            #  "ci"
            #  "docs"
            #  "test"
        }

        for commit in commits_messages:
            if ":" not in commit:
                continue
            commit_split = commit.split(":", 1)
            if commit_split[0] not in switcher.keys():
                continue
            commit_type = switcher[commit_split[0]]
            commit_message = commit_split[1].strip()
            commit_message = commit_message[0].upper() + commit_message[1:]
            changes[commit_type].append(commit_message)

        # TODO: don't print if there is no change

        changelog_printer = ChangelogPrinter()
        changelog_printer.print_changelog(changes, current_version, previous_version)
