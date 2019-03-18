A handy tool with a command line interface for logging time worked. At
any time you can see how much you have spent time on a particular
project and how much you have earned on it.

Installation
------------

.. code:: bash

   pip install salary-timetracker-sqlite

Usage
-----

.. code:: bash

   tts [OPTIONS]

   To add a new entry just enter 'tts'. If there are no options, an interactive session is started.

   Options:
     -a, --show-all     Show all entries
     -p, --show-paid    Show paid
     -u, --show-unpaid  Show unpaid
     -s, --stats        Show unpaid hours
     -m, --mark-paid    Mark all hours worked as paid
     --del-paid         Delete records marked as paid
     --help             Show this message and exit.
