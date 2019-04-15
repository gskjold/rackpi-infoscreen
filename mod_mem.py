import subprocess

def fetchFormatted():
    cmd = "free -m | awk 'NR==2{printf \"MEM: %3d%%\", $3*100/$2 }'"
    return subprocess.check_output(cmd, shell = True )
