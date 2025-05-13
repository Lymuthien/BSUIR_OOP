from .icommand import ICommand


class ExitCommand(ICommand):
    def execute(self):
        exit()
