'''
Django command to wait for the database to be available
'''
from time import sleep
from psycopg2 import OperationalError as Psycopg2Error
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        '''Entrypoint for command.'''
        self.stdout.write(self.style.WARNING('Waiting for Database...'))
        db_up = False
        max_try = 10
        error_message = None
        while (db_up is False) and (max_try > 0):
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2Error, OperationalError) as e:
                self.stdout.write('Database unavaliable. Waiting 1 second...')
                sleep(1)
                max_try -= 1
                error_message = e
        if max_try == 0:
            self.stdout.write(self.style.ERROR('Database not avaliable.'))
            self.stdout.write(self.style.ERROR(error_message))

        else:
            self.stdout.write(self.style.SUCCESS('Database avaliable!'))
