import subprocess

class CardNtp:
    def __init__(self):
        # stratum offset syncdist refid
        self.cmd = "ntptrace | awk '{printf \"%d %f %f %s\", $3, $5, $8, $10}'"

    def lines(self):
        out = subprocess.check_output(self.cmd, shell = True ).split()
        return {"Stratum {} {}".format(out[0], out[3]),"Offset: {}".format(out[1]),"Sync dist: {}".format(out[2])}
