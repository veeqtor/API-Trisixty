"""Module to test the wait for db command"""

from subprocess import PIPE, Popen
from utils.constants import CHARSETS


class TestWaitForDB:
    """
    Class representing the test for the wait for db command.
    """

    def test_wait_for_db_success(self):
        """
        Test the wait for db command.
        """
        p = Popen(['python', 'manage.py', 'wait_for_db'], stdin=PIPE,
                  stdout=PIPE, stderr=PIPE)
        output, err = p.communicate()
        rc = p.returncode

        assert output.decode(CHARSETS[0]) == \
            'Waiting for database...\nDatabase available!\n'
        assert rc == 0
