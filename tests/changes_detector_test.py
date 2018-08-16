import unittest, os, sys

sys.path.append(os.path.abspath(sys.path[0]) + '/../')
from src.changes_detector import ChangesDetector

class ChangesDetectorTest(unittest.TestCase):

    def setUp(self):
        self.major = 1
        self.minor = 109
        self.patch = 12
        self.detector = ChangesDetector(self.major, self.minor, self.patch)

    def test_does_not_find_changes_when_detecting_changes_from_empty_list_of_commits_messages(self):
        self.detector.detect_changes([])

        self.assertEqual(self.detector.new_major_version, self.major)
        self.assertEqual(self.detector.new_minor_version, self.minor)
        self.assertEqual(self.detector.new_patch_version, self.patch)

    def test_does_not_changes_major_version_when_there_are_only_patch_commits(self):
        self.detector.detect_changes([
                "fix: some bug fixed",
                "fix: second bug fixed"
        ])

        self.assertEqual(self.detector.new_major_version, self.major)

    def test_does_not_changes_minor_version_when_there_are_only_patch_commits(self):
        self.detector.detect_changes([
                "fix: some bug fixed",
                "fix: second bug fixed"
        ])

        self.assertEqual(self.detector.new_minor_version, self.minor)

    def test_increases_patch_version_by_1_when_there_are_only_patch_commits(self):
        self.detector.detect_changes([
                "fix: some bug fixed",
                "fix: second bug fixed"
        ])

        self.assertEqual(self.detector.new_patch_version, self.patch + 1)

    def test_does_not_change_major_version_when_there_are_only_features_commits(self):
        self.detector.detect_changes([
                "feat: some feature",
                "feat: second feature"
        ])

        self.assertEqual(self.detector.new_patch_version, 0)

    def test_increases_minor_version_by_1_when_there_are_only_features_commits(self):
        self.detector.detect_changes([
                "feat: some feature",
                "feat: second feature"
        ])

        self.assertEqual(self.detector.new_minor_version, self.minor + 1)

    def test_resets_patch_version_when_there_are_only_features_commits(self):
        self.detector.detect_changes([
                "feat: some feature",
                "feat: second feature"
        ])

        self.assertEqual(self.detector.new_patch_version, 0)

    def test_increases_major_version_by_1_when_there_are_only_breaking_change_commits(self):
        self.detector.detect_changes([
                "bc: some change",
                "bc: second change"
        ])

        self.assertEqual(self.detector.new_major_version, self.major + 1)

    def test_resets_minor_version_when_there_is_at_least_one_breaking_change_commit(self):
        self.detector.detect_changes([
                "bc: some change",
                "bc: second change",
                "feat: some feature",
                "fix: some bug fixed"
        ])

        self.assertEqual(self.detector.new_minor_version, 0)

    def test_resets_patch_version_when_there_is_at_least_one_breaking_change_commit(self):
        self.detector.detect_changes([
                "bc: some change",
                "bc: second change",
                "feat: some feature",
                "fix: some bug fixed"
        ])

        self.assertEqual(self.detector.new_patch_version, 0)


if __name__ == '__main__':
    unittest.main()
