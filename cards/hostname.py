import subprocess

class CardHostname:
    def __init__(self):
        self.cmd = "hostname"
    def lines(self):
        return [subprocess.check_output(self.cmd, shell = True )]
