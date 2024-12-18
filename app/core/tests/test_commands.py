'''
Test custom Django managment commands.
'''

from unittest.mock import patch
from unittest.mock import MagicMock
from psycopg2 import OperationalError as Psycops2Error
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch("core.management.commands.wait_for_db.Command.check")
class CommandTests(SimpleTestCase):
    '''Test commands.'''

    def test_wait_db_ready(self, patched_check: MagicMock):
        '''Test waiting for database if database ready.'''
        patched_check.return_value = True
        call_command('wait_for_db')
        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep: MagicMock, patched_check: MagicMock):
        '''Test waiting for database when getting OperationalError.'''
        patched_check.side_effect = [Psycops2Error] * 2 + [OperationalError] * 3 + [True]
        call_command('wait_for_db')
        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
