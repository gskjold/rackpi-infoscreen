import subprocess

def fetchFormatted():
    cmd = "top -bn1 | grep load | awk '{printf \"CPU: %3d%%\", $(NF-2)*100/4}'"
    return subprocess.check_output(cmd, shell = True )
