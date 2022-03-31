
def example():
    """Example command"""
    print('This is an example CLI command.')


def init_app(app):
    # add multiple commands in a bulk
    for command in [example]:
        app.cli.add_command(app.cli.command()(command))
