import subprocess

def pretty_time_delta(seconds):
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

def fetchFormatted():
    cmd = "cat /proc/uptime | awk '{print $1}' | awk -F'.' '{print $1}'"
    UPTIME_S = subprocess.check_output(cmd, shell = True )
    return pretty_time_delta(UPTIME_S)
