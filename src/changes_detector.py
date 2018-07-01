class ChangesDetector:

    def __init__(self, major, minor, bugfix):
        self._newMajor = major
        self._newMinor = minor
        self._newBugfix = bugfix

    @property
    def new_major_version(self):
        return self._newMajor

    @property
    def new_minor_version(self):
        return self._newMinor

    @property
    def new_bugfix_version(self):
        return self._newBugfix

    def detect_changes(self, commit_messages):
        major_increase = 0
        minor_increase = 0
        bugfix_increase = 0

        for commit in commit_messages:
            if commit.lower().startswith("fix:"):
                bugfix_increase = 1
            if commit.lower().startswith("feat:"):
                minor_increase = 1
            if commit.lower().startswith("breaking change:"):
                major_increase = 1

        if major_increase > 0:
            self._newMajor += major_increase
            self._newMinor = 0
            self._newBugfix = 0
        elif minor_increase > 0:
            self._newBugfix = 0
            self._newMinor += minor_increase
        else:
            self._newBugfix += bugfix_increase
