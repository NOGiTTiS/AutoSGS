"""
AutoSGS - Main Application Entry Point
"""

import sys
from autosgs.ui.app import run_app


def main():
    try:
        run_app()
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    main()
