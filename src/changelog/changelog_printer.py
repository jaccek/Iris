import change_type


class ChangelogPrinter:

    def __init__(self):
        pass

    def print_changelog(self, changes, version):
        lines = ["# Version %s\n\n" % version]

        types = [
            change_type.ADDED,
            change_type.CHANGED,
            change_type.DEPRECATED,
            change_type.REMOVED,
            change_type.FIXED,
            change_type.SECURITY
        ]

        for type in types:
            lines.extend(self._generate_section_lines(type, changes[type]))

        self._print_changelog_stdout(lines)
        self._print_changelog_to_file(lines)

    @staticmethod
    def _generate_section_lines(section, changes):
        if len(changes) == 0:
            return []

        lines = ["## %s\n\n" % section]
        for change in changes:
            lines.append("- %s\n" % change)
        lines.append("\n")
        return lines

    @staticmethod
    def _print_changelog_stdout(lines):
        for line in lines:
            print(line)

    @staticmethod
    def _print_changelog_to_file(lines):
        file = open("CHANGELOG-test.md", "w+")
        for line in lines:
            file.write(line)
        file.close()
