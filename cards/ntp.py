import subprocess

class CardNtp:
    def __init__(self):
        # stratum offset syncdist refid
        self.cmd = "ntptrace | awk '{printf \"%d %f %f %s\", $3, $5, $8, $10}'"

    def lines(self):
        res = subprocess.check_output(self.cmd, shell = True ).decode("utf-8")
        out = str(res).split()
        if len(out) > 0:
            stratum = int(out[0])
        else:
            stratum = -1
        if len(out) > 1:
            offset = out[1]
        else:
            offset = -1
        if len(out) > 2:
            syncdist = out[2]
        else:
            syncdist = -1
        if len(out) > 3:
            refid = out[3]
        else:
            refid = ""
        return ["NTP Stratum %d %s" % (stratum, refid)," offset: {}".format(offset)," sync dist: {}".format(syncdist)]
