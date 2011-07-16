# -*- coding: utf-8 -*-

import os
import subprocess

# default paths
PROFILE_DIR = '/etc/network.d'
STATE_DIR = '/var/run/network/profiles'
NETCFG_BIN = '/usr/bin/netcfg'


class Netcfg:
    def __init__(self, profile_dir=PROFILE_DIR,
                        state_dir=STATE_DIR,
                        netcfg_bin=NETCFG_BIN):
        # paths
        self._profile_dir = profile_dir
        self._state_dir = state_dir
        self._bin = netcfg_bin
        # profile list
        self.profiles = []

        # netcfg arguments
        self.ncargs = { "up":        "-u",
                        "down":      "-d",
                        "reconnect": "-r" }

        self.get_profiles()


    def get_profiles(self):
        """scan profile dir and store profile names"""
        profiles = os.listdir(self._profile_dir)

        for profile in profiles:
            full_path = os.path.join(self._profile_dir, profile)

            if os.path.isfile(full_path):
                # TODO: check if every profile has "CONNECTION"
                # check for "CONNECTION" string to ensure it is a profile file
                self.profiles.append(profile)


    def get_current(self):
        """get current profile name from state dir"""
        profile = os.listdir(self._state_dir)
        if profile:
            return profile

        return None


    def up(self, profile, block=True, prefix=None):
        """profile up"""
        command = [self._bin, self,ncargs['up'], profile]
        if prefix:
            command.insert(0, prefix)
        return self._run_command(command, block)


    def down(self, profile, block=True, prefix=None):
        """profile down"""
        command = [self._bin, self.ncargs["down"], profile]
        if prefix:
            command.insert(0, prefix)
        return self._run_command(command, block)


    def reconnect(self, block=True, prefix=None):
        """disconnect and reconnect current profile"""
        profile = self.get_current()
        if profile is None:
            return False

        command = [self._bin, self.ncargs["reconnect"], profile]
        if prefix:
            command.insert(0, prefix)
        return self._run_command(command, block)


    def _run_command(self, command, block):
        process = subprocess.Popen(command, stdout=subprocess.PIPE)
        if block is True:
            process.wait()
        return process


if __name__ == '__main__':
    pass

# vim: set sw=4 ts=4 sts=4 et:
