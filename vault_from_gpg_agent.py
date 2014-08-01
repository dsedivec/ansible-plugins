#!/usr/bin/env python
#
# Store your Ansible vault password in gpg-agent.
#
# Usage:
#
# 1. Make sure you have gpg-agent installed and running.
#    https://www.gnupg.org/documentation/manuals/gnupg/Invoking-GPG_002dAGENT.html
#    (If you're on a Mac, https://gpgtools.org/ makes this very easy.)
#
# 2. Make sure you have gpg-connect-agent on your path.  This comes
#    with gpg-agent.  To test gpg-agent and gpg-connect-agent, try:
#
#        echo NOP | gpg-connect-agent
#
#    This should respond with just "OK".
#
# 3. Copy this script somewhere and set vault_password_file to point
#    at it, or use the --vault-password-file option on the command
#    line.
#
# gpg-agent caches the passphrase for 15 minutes by default.  See
# https://www.gnupg.org/documentation/manuals/gnupg/Agent-Options.html
# if you want to change this.  Run this script with the --clear option
# to clear your passphrase from gpg-agent.
#
# Note that the path to this script is used as the cache key for this
# password in gpg-agent.  For example, if you move this script to a
# new path then you may be re-prompted for your password.

import subprocess
import sys
import urllib
import os.path
import hashlib
import base64
import argparse


def get_passphrase(gpg_agent, my_path, cache_id):
    description = urllib.quote(
        "Please enter the ansible vault password for %s" % (my_path,))
    command = "GET_PASSPHRASE %s X X %s\n" % (cache_id, description)
    stdout = gpg_agent.communicate(command)[0]
    if gpg_agent.returncode != 0:
        raise Exception("gpg-connect-agent exited %r" %
                        (gpg_agent.returncode,))
    elif not stdout.startswith("OK"):
        raise Exception("gpg-agent says: %s" % (stdout.rstrip(),))
    else:
        # You'll get an exception here if we get anything we didn't expect.
        passphrase = stdout[3:-1].decode("hex")
        print passphrase


def clear_passphrase(gpg_agent, cache_id):
    stdout = gpg_agent.communicate("CLEAR_PASSPHRASE %s\n" % (cache_id,))[0]
    if gpg_agent.returncode != 0:
        raise Exception("gpg-connect-agent exited %r" %
                        (gpg_agent.returncode,))
    elif not stdout.startswith("OK"):
        raise Exception("gog-agent says: %s" % (stdout.rstrip(),))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--clear", default=False, action="store_true",
                        help="Clear password from GPG agent")
    gpg_agent = subprocess.Popen(["gpg-connect-agent"], stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE)
    args = parser.parse_args()
    my_path = os.path.realpath(sys.argv[0])
    # Per the source, cache-id is limited to 50 bytes, so we hash our
    # path and Base64 encode the path.
    hashed_path = base64.b64encode(hashlib.sha1(my_path).digest())
    cache_id = "ansible-vault:%s" % (hashed_path,)
    if args.clear:
        clear_passphrase(gpg_agent, cache_id)
    else:
        get_passphrase(gpg_agent, my_path, cache_id)


if __name__ == "__main__":
    main()
