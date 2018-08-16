import unittest

from mock import patch

from src import iris
from src.calculation_store import CalculationStore
from src.changelog.changelog_printer import ChangelogPrinter
from src.git.git_plugin import GitPlugin
from src.git.git_plugin import ID as COMMIT_ID
from src.git.git_plugin import MESSAGE as COMMIT_MESSAGE


class ChangesDetectorTest(unittest.TestCase):

    @patch.object(ChangelogPrinter, '_print_changelog_to_file')
    @patch.object(ChangelogPrinter, '_get_historical_changelog')
    @patch.object(CalculationStore, 'save_current_version_for_future_calculations')
    @patch.object(GitPlugin, 'get_all_commits_history')
    def test_iris_when_calculating_single_feature_commit_and_there_is_no_previous_calculation(
            self,
            get_commits_history_mock,
            save_version_mock,
            previous_changelog_mock,
            print_changelog_mock):

        # given
        commits_history = [
            {COMMIT_ID: "TEST", COMMIT_MESSAGE: "feat: test"}
        ]
        get_commits_history_mock.return_value = commits_history
        previous_changelog_mock.return_value = []

        # when
        iris.main()

        # then
        expected_version = "0.1.0"
        print_changelog_mock.assert_called_with([
            "# Version {0}\n".format(expected_version),
            "\n## Added\n\n",
            "- Test\n"
        ])
        save_version_mock.assert_called_with(expected_version, commits_history)

    @patch.object(ChangelogPrinter, '_print_changelog_to_file')
    @patch.object(ChangelogPrinter, '_get_historical_changelog')
    @patch.object(CalculationStore, 'save_current_version_for_future_calculations')
    @patch.object(GitPlugin, 'get_all_commits_history')
    def test_iris_when_calculating_single_breaking_change_commit_and_there_is_no_previous_calculation(
            self,
            get_commits_history_mock,
            save_version_mock,
            previous_changelog_mock,
            print_changelog_mock):
        # given
        commits_history = [
            {COMMIT_ID: "abc", COMMIT_MESSAGE: "bc: test"}
        ]
        get_commits_history_mock.return_value = commits_history
        previous_changelog_mock.return_value = []

        # when
        iris.main()

        # then
        expected_version = "1.0.0"
        print_changelog_mock.assert_called_with([
            "# Version {0}\n".format(expected_version),
            "\n## Added\n\n",
            "- Test\n"
        ])
        save_version_mock.assert_called_with(expected_version, commits_history)

    @patch.object(ChangelogPrinter, '_print_changelog_to_file')
    @patch.object(ChangelogPrinter, '_get_historical_changelog')
    @patch.object(CalculationStore, 'save_current_version_for_future_calculations')
    @patch.object(CalculationStore, 'get_previous_version')
    @patch.object(GitPlugin, 'get_all_commits_history')
    def test_iris_when_calculating_empty_commit_list_and_there_is_previous_calculation(
            self,
            get_commits_history_mock,
            get_previous_version_mock,
            save_version_mock,
            previous_changelog_mock,
            print_changelog_mock):
        # given
        version = "1.0.0"
        commits_history = []
        get_commits_history_mock.return_value = commits_history
        get_previous_version_mock.return_value = version
        previous_changelog_mock.return_value = [
            "# Version {0}\n".format(version),
            "\n## Added\n\n",
            "- Test\n"
        ]

        # when
        iris.main()

        # then
        print_changelog_mock.assert_called_with([
            "# Version {0}\n".format(version),
            "\n## Added\n\n",
            "- Test\n"
        ])
        save_version_mock.assert_called_with(version, commits_history)

    @patch.object(ChangelogPrinter, '_print_changelog_to_file')
    @patch.object(ChangelogPrinter, '_get_historical_changelog')
    @patch.object(CalculationStore, 'save_current_version_for_future_calculations')
    @patch.object(CalculationStore, 'get_previous_version')
    @patch.object(GitPlugin, 'get_all_commits_history')
    def test_iris_when_calculating_single_fix_commit_list_and_there_is_previous_calculation(
            self,
            get_commits_history_mock,
            get_previous_version_mock,
            save_version_mock,
            previous_changelog_mock,
            print_changelog_mock):
        # given
        version = "1.0.0"
        expected_version = "1.0.1"
        commits_history = [
            {COMMIT_ID: "abc", COMMIT_MESSAGE: "fix: fix"}
        ]
        get_commits_history_mock.return_value = commits_history
        get_previous_version_mock.return_value = version
        previous_changelog_mock.return_value = [
            "# Version {0}\n".format(version),
            "\n## Added\n\n",
            "- Test\n"
        ]

        # when
        iris.main()

        # then
        print_changelog_mock.assert_called_with([
            "# Version {0}\n".format(expected_version),
            "\n## Fixed\n\n",
            "- Fix\n",
            "\n",
            "# Version {0}\n".format(version),
            "\n## Added\n\n",
            "- Test\n"
        ])
        save_version_mock.assert_called_with(expected_version, commits_history)
