#!/usr/bin/env python2

import gtk, pygtk, gobject
import os, os.path, subprocess, sys
import netcfg
import ConfigParser, pdb

try:
    import pynotify
except ImportError:
    pynotify=False

profile_dir="/etc/network.d"
state_dir="/var/run/network/profiles"
helper_cmd="./netcfg-tray-helper"

# create a list of user and system wide configs
config_list = [os.path.join(os.environ["XDG_CONFIG_HOME"], "netcfg-tray/config")]
for xdg_path in os.environ["XDG_CONFIG_DIRS"]:
    config_list.append(os.path.join(xdg_path, "netcfg-tray/config"))

# get the first valid config file
config_file = None
for config in config_list:
    if os.path.isfile(config):
        config_file = config
        break

# if we can't find a configuration exit
if config_file is None:
    print "Cannot find configuration file. Bye"
    sys.exit(1)

print config_file
license_file="/usr/share/licenses/netcfg-tray/LICENSE"
TRAY_VERSION=3

if __name__ == '__main__':
    tray = NetcfgTray()
    gtk.main()
