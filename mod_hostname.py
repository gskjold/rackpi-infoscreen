import subprocess

def fetchFormatted():
    cmd = "hostname"
    return subprocess.check_output(cmd, shell = True )
