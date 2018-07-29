import unittest

from mock import patch

from src import iris
from src.calculation_store import CalculationStore
from src.changelog.changelog_printer import ChangelogPrinter


class ChangesDetectorTest(unittest.TestCase):

    @patch.object(ChangelogPrinter, 'print_changelog')
    @patch.object(CalculationStore, 'save_current_version_for_future_calculations')
    @patch.object(iris, 'get_commits_history')
    def test_iris_when_calculating_single_feature_commit_and_there_is_no_previous_calculation_and(
            self, get_commits_history_mock, save_version_mock, print_changelog_mock):
        # given
        get_commits_history_mock.return_value = [
            "TEST|feat: test"
        ]

        # when
        iris.main()

        # then
        expected_changes = {
            'Added': ["Test"],
            'Fixed': [],
            'Deprecated': [],
            'Changed': [],
            'Security': [],
            'Removed': []
        }
        print_changelog_mock.assert_called_with(expected_changes, "0.1.0", "0.0.0")
