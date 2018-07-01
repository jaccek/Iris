
class ChangesDetector:

    def __init__(self, major, minor, bugfix):
        self._newMajor = major
        self._newMinor = minor
        self._newBugfix = bugfix

    @property
    def newMajorVersion(self):
        return self._newMajor

    @property
    def newMinorVersion(self):
        return self._newMinor

    @property
    def newBugfixVersion(self):
        return self._newBugfix

    def detectChanges(self, commitMessages):
        majorIncrease = 0
        minorIncrease = 0
        bugfixIncrease = 0

        for commit in commitMessages:
            if commit.lower().startswith("fix:"):
                bugfixIncrease = 1
            if commit.lower().startswith("feat:"):
                minorIncrease = 1
            if commit.lower().startswith("breaking change:"):
                majorIncrease = 1

        if majorIncrease > 0:
            self._newMajor += majorIncrease
            self._newMinor = 0
            self._newBugfix = 0
        elif minorIncrease > 0:
            self._newBugfix = 0
            self._newMinor += minorIncrease
        else:
            self._newBugfix += bugfixIncrease
