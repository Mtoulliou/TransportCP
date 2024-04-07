#!/usr/bin/env python
import os
import sys

def main():
    if __name__ == "__main__":
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TCP.settings")

        import django
        django.setup()

        # Override default port for `runserver` command
        from django.core.management.commands.runserver import Command as runserver
        runserver.default_port = "3456"

        from django.core.management import execute_from_command_line

        execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()