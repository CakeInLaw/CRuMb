from sys import argv

from core.commands.commands import run_command

if len(argv) == 1:
    command_name = 'flet'
else:
    command_name = argv.pop(1)
run_command(command_name)
