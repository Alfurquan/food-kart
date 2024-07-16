import shlex
from typer.testing import CliRunner
from foodkart.cli import app

def foodkart_cli(command_string):
    command_list = shlex.split(command_string)
    runner = CliRunner()
    result = runner.invoke(app, command_list)
    output = result.stdout.rstrip()
    return output
