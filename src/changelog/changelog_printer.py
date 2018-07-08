import change_type


class ChangelogPrinter:

    def __init__(self):
        pass

    def print_changelog(self, changes, version, previous_version):
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

        # load actual changelog
        # TODO: what if changelog doesn't exists yet?
        changelog_file = open("CHANGELOG-test.md", "r")     # TODO: changelog file name
        changelog_lines = changelog_file.read().splitlines()
        changelog_file.close()

        # add actual changelog to end of generated changelog
        found = False
        for line in changelog_lines:
            if line == "# Version " + previous_version:
                found = True

            if found:
                lines.append(line)
                lines.append("\n")

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
        file = open("CHANGELOG-test.md", "w+")      # TODO: changelog filename
        for line in lines:
            file.write(line)
        file.close()
