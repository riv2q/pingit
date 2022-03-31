from multiprocessing import Process

from flask_cli import FlaskCLI

from pingit import app


FlaskCLI(app)


@app.cli.command()
def start_server():
    """Start application daemon."""
    server = Process(Target=app.run(threaded=True))
    server.start()
    print("Server Started")


@app.cli.command()
def stop_server():
    """Stop application daemon."""
    server = Process(target=app.run)
    if server.is_alive() is True:
        server.terminate()
        server.join()
    print("Server stoped")
