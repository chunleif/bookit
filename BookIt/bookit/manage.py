#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookit.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    if len(sys.argv) == 1 and "chloe" in sys.argv[0]:
        argv = ['/Users/chloe-/Desktop/21T2_9900/github/capstoneproject-comp9900-w16a-bigleg/bookit/manage.py', 'runserver', '0.0.0.0:80', '--noreload']
    else:
        argv = sys.argv
    execute_from_command_line(argv)


if __name__ == '__main__':
    main()
