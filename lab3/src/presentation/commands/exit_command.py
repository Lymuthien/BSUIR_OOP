from presentation.commands.icommand import ICommand


class ExitCommand(ICommand):
    def execute(self):
        exit()
