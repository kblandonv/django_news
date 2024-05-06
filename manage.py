#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """
    Run administrative tasks.

    This function is responsible for running administrative tasks for the Django project.
    It sets the Django settings module and executes the command line arguments passed to it.

    Raises:
        ImportError: If Django is not installed or not available on the PYTHONPATH environment variable.

    """
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_news.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
