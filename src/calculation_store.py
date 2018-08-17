import json


class CalculationStore:

    _VERSION = "version"
    _LAST_COMMIT = "last_commit"

    def __init__(self):
        self._filename = ".iris"
        self._old_version = None

    def get_previous_version(self):
        if self._old_version is None:
            self._load_old_version()

        return self._old_version[self._VERSION]

    def get_last_commit(self):
        if self._old_version is None:
            self._load_old_version()

        return self._old_version[self._LAST_COMMIT]

    def _load_old_version(self):
        try:
            iris_file = open(self._filename, "r")
            self._old_version = json.loads(iris_file.read())
            iris_file.close()
        except (IOError, ValueError):
            self._old_version = {
                self._VERSION: '0.0.0',
                self._LAST_COMMIT: '0'
            }
        print self._old_version

    def save_current_version_for_future_calculations(self, version, last_commit_id):
        new_version = {
            self._VERSION: version,
            self._LAST_COMMIT: last_commit_id
        }

        iris_file = open(self._filename, "w")
        iris_file.write(json.dumps(new_version, sort_keys=True, indent=4))
        iris_file.close()
