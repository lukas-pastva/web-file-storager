#!/usr/bin/env python
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

from django.core.management import execute_from_command_line  # noqa: E402  pylint: disable=C0413

if __name__ == "__main__":
    execute_from_command_line(sys.argv)
