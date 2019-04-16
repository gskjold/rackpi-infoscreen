import subprocess

class CardMem:
    def __init__(self):
        self.cmd = "free -m | awk 'NR==2{printf \"MEM: %3d%%\", $3*100/$2 }'"

    def lines(self):
        return {subprocess.check_output(self.cmd, shell = True )}
