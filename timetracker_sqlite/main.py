#!/usr/bin/env python3

import os
import sys
import sqlite3
import click
# from .config import DB_FILE
from .utils import Db, Timetracker, get_git_root

DB_FILE = os.path.join(get_git_root(), 'timetracker.sqlite')


@click.command()
@click.option('--show-all', '-a', is_flag=True, help='Show all entries')
@click.option('--show-paid', '-p', is_flag=True, help='Show paid')
@click.option('--show-unpaid', '-u', is_flag=True, help='Show unpaid')
@click.option('--stats', '-s', is_flag=True, help='Show unpaid hours')
@click.option('--mark-paid', '-m', is_flag=True, help='Mark all hours worked as paid')
@click.option('--del-paid', is_flag=True, help='Delete records marked as paid')
def main(show_all=None, show_paid=None, show_unpaid=None, stats=None,
         mark_paid=None, del_paid=None):
    with Db(DB_FILE) as db:
        tt = Timetracker(db)
        try:
            args_count = len(sys.argv)
            if args_count < 2:
                data = tt.get_log_from_input()
                tt.add_entry(data['minutes'], data['comment'])
            elif args_count > 2:
                sys.exit('Too many options')
            else:
                if stats:
                    minutes = tt.minutes_total()
                    msg = 'Time worked (unpaid): %s hours' % round(
                        minutes / 60, 1)
                    click.echo(msg)
                elif show_all:
                    click.echo(tt.show_entries())
                elif show_paid:
                    click.echo(tt.show_entries(1))
                elif show_unpaid:
                    click.echo(tt.show_entries(0))
                elif mark_paid:
                    tt.mark_all_as_paid()
                elif del_paid:
                    tt.del_table_all_paid()
        except sqlite3.Error as e:
            click.echo('ERROR!!!', e)


if __name__ == '__main__':
    main()
