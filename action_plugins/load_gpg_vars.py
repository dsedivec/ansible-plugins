# Copyright 2013 Dale Sedivec
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import subprocess
import collections
import itertools

import yaml

from ansible import utils, errors
from ansible.runner import return_data


class ActionModule (object):
    BYPASS_HOST_LOOP = True
    NEEDS_TMPPATH = False

    def __init__(self, runner):
        self.runner = runner

    def run(self, conn, tmp, module_name, module_args, inject,
            complex_args=None, **kwargs):
        args = {}
        if complex_args:
            args.update(complex_args)
        args.update(utils.parse_kv(module_args))
        path = args.get("path")
        if not path:
            raise errors.AnsibleError('"path" is a required argument')
        gpg_path = args.get("gpg", "gpg")
        gpg = subprocess.Popen([gpg_path, "-q", "-d", path],
                               stdout=subprocess.PIPE)
        stdout, _stderr = gpg.communicate()
        if gpg.returncode != 0:
            raise errors.AnsibleError("error calling gpg")
        try:
            gpg_vars = utils.parse_yaml(stdout)
        except yaml.YAMLError, ex:
            utils.process_yaml_error(ex, stdout, path)
        if not callable(getattr(gpg_vars, "iteritems", None)):
            raise errors.AnsibleError(
                "GPG vars file must be a YAML associative array, not a %r" %
                (gpg_vars.__class__.__name__,))
        host_vars = collections.defaultdict(dict, gpg_vars.pop("hosts", ()))
        # Here on is heavily cribbed from group_by.
        runner = self.runner
        inventory = runner.inventory
        changed = False
        for host_name in runner.host_set:
            host = inventory.get_host(host_name)
            all_vars = itertools.chain(gpg_vars.iteritems(),
                                       host_vars[host_name].iteritems())
            for key, value in all_vars:
                if host.vars.get(key) != value:
                    host.set_variable(key, value)
                    changed = True
            # Totally cribbed from group_by.  Looks like this is
            # necessary to invalidate the inventory's cached variables
            # for the host.
            del inventory._vars_per_host[host_name]
        return return_data.ReturnData(conn=conn, comm_ok=True,
                                      result={"changed": changed})
