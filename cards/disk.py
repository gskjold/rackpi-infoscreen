import subprocess

class CardDisk:
    def __init__(self, mount_point):
        self.mount_point = mount_point
        self.cmd = "df {} -h --output=size,used,avail,pcent | tail -n1".format(mount_point)

    def lines(self):
        res = subprocess.check_output(self.cmd, shell = True ).decode("utf-8")
        out = res.split()
        if(len(out) > 0):
            size = out[0]
        else:
            size = "n/a"
        if(len(out) > 1):
            used = out[1]
        else:
            used = "n/a"
        if(len(out) > 2):
            avail = out[2]
        else:
            avail = "n/a"
        if(len(out) > 3):
            pcent = out[3]
        else:
            pcent = "n/a"
        return ["Mount: {} {}".format(self.mount_point, size), " usage: {} {}".format(used, pcent)]
