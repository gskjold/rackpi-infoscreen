import subprocess

class CardUptime:
    def __init__(self):
        self.cmd = "cat /proc/uptime | awk '{print $1}' | awk -F'.' '{print $1}'"

    def pretty_time_delta(self, seconds):
        seconds = int(seconds)
        days, seconds = divmod(seconds, 86400)
        hours, seconds = divmod(seconds, 3600)
        minutes, seconds = divmod(seconds, 60)
        if days > 0:
            return '%dd %dh %dm' % (days, hours, minutes)
        elif hours > 0:
            return '%dh %dm %ds' % (hours, minutes, seconds)
        elif minutes > 0:
            return '%dm %ds' % (minutes, seconds)
        else:
            return '%ds' % (seconds)

    def lines(self):
        UPTIME_S = subprocess.check_output(self.cmd, shell = True )
        return {"up {}".format(self.pretty_time_delta(UPTIME_S))}
