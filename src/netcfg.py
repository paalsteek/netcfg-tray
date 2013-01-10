# netcfg interface...
import os.path
import os
import subprocess

helper_cmd="netcfg-tray-helper"
profile_dir="/etc/network.d/"
state_dir="/run/network/profiles/"

profiles=dict()

def read_config(config):
    import shlex
    cfg = shlex.split(open(config, "r").read())
    options = {}
    for line in cfg:
        (var, delim, value) = line.partition('=')  
        if delim and var.lstrip()[0] != "#":
            options[var] = value
    return options


def read_rcconf(variable):
    if os.path.exists("/etc/conf.d/netcfg"):
      rc=open("/etc/conf.d/netcfg")
    elif os.path.exists("/etc/rc.conf"):
      rc=open("/etc/rc.conf")
    for line in rc.readlines():
        line=line.strip()
        if line[:len(variable)] == variable:
            key,val=line.split("=",1)
            return val.strip("'\"")

def update_profiles():
    process = subprocess.Popen(["netcfg", "list"], stdout=subprocess.PIPE)
    for prof in process.communicate()[0].split():
      profiles[prof] = Profile(prof)
    process = subprocess.Popen(["netcfg", "current"], stdout=subprocess.PIPE)
    for prof in process.communicate()[0].split():
      profiles[prof].set_active(True)

def get_profiles():
    return profiles.values()
   
   
def get_active_profiles():
    return filter(Profile.active, profiles.values())
    
def get_inactive_profiles():
    return filter(Profile.inactive, profiles.values())
    
def up(profile, cmd=None, block=True, check=False):
    return run("up", profile, cmd, block, check)

    
def down(profile, cmd=None, block=True, check=False):
    return run("down", profile, cmd, block, check)


def run(func, profile, cmd=None, block=True, check=False):
    script = [helper_cmd, func, profile.name]
    if cmd:
        script.insert(0, cmd)
    process = subprocess.Popen(script, stdout=subprocess.PIPE)
    if block:
        process.wait()
    return process    
    

def auto_status(connection):
    return os.access("/var/run/daemons/net-auto-"+connection, os.F_OK)
       

def auto_interface(connection):
    
    return read_rcconf(connection.upper()+"_INTERFACE")

    
class Profile (dict):

    def __init__(self,profile_name):
        self.name=profile_name
        self.filename=os.path.join(profile_dir, profile_name)
        self.active=False

    def set_active(self, active):
        self.active=active

    def active(self):
        return self.active

    def inactive(self):
        return not self.active


