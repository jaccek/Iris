import change_type


class ChangelogPrinter:

    def __init__(self, changelog_filename = "CHANGELOG.md"):
        self._changelog_filename = changelog_filename

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

        lines.extend(self._get_historical_changelog(previous_version))

        # self._print_changelog_stdout(lines)
        self._print_changelog_to_file(lines)

    def _get_historical_changelog(self, previous_version):
        try:
            changelog_lines = self._load_existing_changelog()
        except IOError:
            changelog_lines = []

        historical_lines = []
        perv_version_found = False
        for line in changelog_lines:
            if line == "# Version " + previous_version:
                perv_version_found = True

            if perv_version_found:
                historical_lines.append(line)
                historical_lines.append("\n")

        return historical_lines

    def _load_existing_changelog(self):
        changelog_file = open(self._changelog_filename, "r")
        changelog_lines = changelog_file.read().splitlines()
        changelog_file.close()

        return changelog_lines

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

    def _print_changelog_to_file(self, lines):
        file = open(self._changelog_filename, "w+")
        for line in lines:
            file.write(line)
        file.close()
