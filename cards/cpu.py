import subprocess

class CardCpu:
    def __init__(self):
        self.cmd = "top -bn1 | grep load | awk '{printf \"CPU: %3d%%\", $(NF-2)*100/4}'"

    def lines(self):
        return [subprocess.check_output(self.cmd, shell = True )]
