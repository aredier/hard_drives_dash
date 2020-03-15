# -*- coding: utf-8 -*-

"""Console script for chariots."""
import sys

import click

from .app import app


@click.group()
def main():
    """Console scripts for chariots."""


@main.command()
def server(config_file=None):
    """
    creates a new chariot project.
    this will open an interactive cookiecutter session with parameters to customize your projects
    """
    app.run(host='0.0.0.0', port=5000)
    
@main.command()
def worker(config_file=None):
    """
    creates a new chariot project.
    this will open an interactive cookiecutter session with parameters to customize your projects
    """
    app._worker_pool.spawn_worker()




if __name__ == '__main__':
    sys.exit(main())  # pragma: no cover
