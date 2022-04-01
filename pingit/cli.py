import click
import subprocess
import os

from flask_cli import FlaskCLI

from pingit.app import app

FlaskCLI(app)


@app.cli.command()
@click.option('--host', default='0.0.0.0')
@click.option('--port', default=5000)
def start_dev_server(host, port):
    """Start development server."""
    click.echo(
        "Starting development server on host={host} port={port}".format(
            host=host, port=port)
    )
    app.run(host=host, port=port, debug=True)


@app.cli.command()
@click.option('--host', default='0.0.0.0')
@click.option('--port', default=5000)
def start_server(host, port):
    """Start server."""
    click.echo(
        "Starting server on host={host} port={port}".format(
            host=host, port=port)
    )
    command = (
        "gunicorn --bind {host}:{port} --pid gunicorn.pid app:app".format(
            host=host, port=port)
    )
    os.popen(command)


@app.cli.command()
def stop_server():
    """Stop server."""
    click.echo("Stopping all servers...")
    subprocess.run("pkill -9 -f gunicorn", shell=True)
