#!/usr/bin/env python2

import os
import sys
import argparse
from ConfigParser import SafeConfigParser


def parse_arguments():
    """parse command line arguments

    set all defaults to None so we can use it to check if a flag was supplied
    (used to check if need to override config file)
    """
    parser = argparse.ArgumentParser(
            description="A simple tray application to handle ntcfg profiles",
            version="0.1")

    # notifications
    parser.add_argument('-notify', action='store_true', default=None,
                        help='show notifications [default:off]')

    # su gui
    parser.add_argument('-gsu', choices=['gksu', 'ktsuss', 'kdesu'],
                        default=None,
                        help='graphical su application to use')

    # gui group (use gtk or qt)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-gtk', action='store_true', default=None,
                        help='use gtk ui [default]')
    group.add_argument('-qt', action='store_true', default=None,
                        help='use gtk ui')

    return parser.parse_args()


def get_cfg_file(cfg_filename):
    """search in XDG path and return the configuration file"""
    # create a list of user and system wide configs
    cfg_list = [os.path.join(os.environ["XDG_CONFIG_HOME"], cfg_filename)]
    for xdg_path in os.environ["XDG_CONFIG_DIRS"]:
        cfg_list.append(os.path.join(xdg_path, cfg_filename))

    # get the first valid config file
    cfg_file = None
    for cfg in cfg_list:
        if os.path.isfile(cfg):
            cfg_file = cfg
            break

    return cfg_file


def parse_cfg_file(cfg_file, config):
    """parse config file"""
    # in no configuration file found return default options
    if cfg_file is None:
        print 'not found'
        return config

    # read config
    cfg = SafeConfigParser()
    try:
        f = open(cfg_file, 'r', 0)
        try:
            cfg.readfp(f)
        finally:
            f.close()
    except IOError:
        print 'error reading config'
        return None

    # allowed sane values
    allowed = {
        'root_cmd': ('gksudo', 'ktsuss', 'kdesu'),
    }

    for section in cfg.sections():
        for option, value in cfg.items(section):
            # ignore unkown options
            if not config.has_key(option):
                continue

            # ignore unkown values
            try:
                if value not in allowed[option]:
                    continue
            except KeyError:
                pass

            config[option] = value

    return config


def override_from_command_line(args, config):
    """docstring for override_from_command_line"""
    for option, value in args.__dict__.items():
        # if no supplied then bail
        if value is None:
            continue

        # map cmd option with config options
        if option == 'gsu':
            config['root_cmd'] = value
            continue

        if option == 'gtk':
            config['gui'] = 'gtk'
            continue

        if option == 'qt':
            config['gui'] = 'qt'
            continue

        if option == 'notify':
            config[option] = '1'

    return config


args = parse_arguments()

# config dict with default options
config = {
    'root_cmd': 'gksudo',
    'gui': 'gtk',
    'notify': '0',
    'notify_lib': 'libnotify',
    'external_cmd': 'xterm -e',
    'dzen_args': '-p 2'
}
# config filename
#cfg_filename = 'netcfg-tray.rc'
cfg_filename = 'config/netcfg-tray.rc-sample' # dev file

#config = parse_cfg_file(get_cfg_file(cfg_filename), config)
config = parse_cfg_file(cfg_filename, config)
config = override_from_command_line(args, config)
print config # debug


if __name__ == '__main__':
    # import gtk or qt tray
    if config['gui'] == 'gtk':
        try:
            from ui import gtk_tray as gui
        except ImportError:
            print 'Error importing tray application'
            sys.exit(1)
    else:
        raise NotImplementedError
        sys.exit(1)

    # import netcfg lib
    try:
        from netcfg import Netcfg
    except:
        print 'Error importing netcfg library'
        sys.exit(1)


    sys.exit(0)# debug
    netcfg = Netcfg()
    tray = gui.NetcfgTray(netcfg, config)
    gtk.main()

# vim: ts=4 sts=4 et:
