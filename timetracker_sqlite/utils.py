import sys
import time
import datetime
import sqlite3
from subprocess import check_output, CalledProcessError
from prettytable import PrettyTable


TABLENAME = 'timetracker'


def get_git_root():
    '''
    Return the absolute path to the root directory of the git-repository.
    '''
    try:
        base = check_output(['git', 'rev-parse', '--show-toplevel'])
    except CalledProcessError:
        sys.exit(
            'ERROR! At the moment you are not inside a git-repository!\nThe app finishes its work..')
    return base.decode('utf-8').strip()


def format_comment(comment, max_line_length):
    # accumulated line length
    line_length = 0
    words = comment.split(" ")
    formatted_comment = ""
    for word in words:
        # if line_length + len(word) and a space is <= max_line_length
        if line_length + (len(word) + 1) <= max_line_length:
            # append the word and a space
            formatted_comment = formatted_comment + word + " "
            # length = length + length of word + length of space
            line_length = line_length + len(word) + 1
        else:
            # append a line break, then the word and a space
            formatted_comment = formatted_comment + "\n" + word + " "
            # reset counter of length to the length of a word and a space
            line_length = len(word) + 1
    return formatted_comment


class Db:

    def __init__(self, db_filename):
        self._connect = sqlite3.connect(db_filename)
        self._cursor = self._connect.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.commit()
        self.connection.close()

    @property
    def connection(self):
        return self._connect

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.connection.commit()


class Timetracker:

    def __init__(self, db):
        self.cursor = db.cursor
        self.create_table()

    def create_table(self):
        sql = '''CREATE TABLE IF NOT EXISTS {}(
                        timestamp INTEGER PRIMARY KEY NOT NULL,
                        minuts INTEGER NOT NULL,
                        comment TEXT,
                        paid BOOLEAN DEFAULT 0)'''.format(TABLENAME)
        self.cursor.execute(sql)

    def add_entry(self, minuts, comment):
        sql = 'INSERT INTO {} (timestamp, minuts, comment) VALUES(?, ?, ?)'.format(
            TABLENAME)
        params = [int(time.time()), minuts, comment]
        self.cursor.execute(sql, params)

    def get_format_time(self, timestamp):
        return datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M(%d.%m.%y)')

    def show_entries(self, paid=None):
        sql = "SELECT * FROM {}".format(TABLENAME)
        if paid is not None:
            sql += ' WHERE paid={}'.format(paid)
        sql += ' ORDER BY timestamp ASC'

        rows = self.cursor.execute(sql)
        table = PrettyTable()
        table.field_names = ['Date', 'Start Time',
                             'End Time', 'Hours', 'Paid', 'Comment']
        for ts, minuts, comment, paid in rows.fetchall():
            hours = round((minuts / 60), 1)
            paid = 'yes' if paid else 'no'

            start_ts = (ts - (minuts * 60))

            start_time = datetime.datetime.fromtimestamp(
                start_ts).strftime('%H:%M')
            ts_time = datetime.datetime.fromtimestamp(ts)
            start_date = ts_time.strftime('%d.%m.%y')
            end_time = ts_time.strftime('%H:%M')
            comment = format_comment(comment, 60)

            table.add_row([start_date, start_time, end_time,
                           hours, paid, comment or ''])

        table.align = 'l'
        return table

    def minutes_total(self, paid=0):
        sql = 'SELECT SUM(minuts) FROM {} WHERE paid=?'.format(TABLENAME)
        params = [str(paid), ]
        self.cursor.execute(sql, params)
        minuts = self.cursor.fetchone()[0] or 0
        return minuts

    def get_log_from_input(self):
        '''
        If an application is invoked without any arguments,
        the data for a log is retrieved through an interactive session.
        '''
        while True:
            minutes = input(
                "Enter the working time (in minutes, Ctrl-C for cancel): ")
            if not minutes.isdigit():
                print("No minutes have been entered. Try once more...")
                continue
            comment = input('Comment on the entry: ') or None
            return {'minutes': minutes, 'comment': comment}

    def mark_all_as_paid(self):
        sql = "UPDATE {} SET paid=1 WHERE paid=0".format(TABLENAME)
        self.cursor.execute(sql)

    def del_table_all_paid(self):
        sql = "DELETE FROM {} WHERE paid=1".format(TABLENAME)
        self.cursor.execute(sql)
