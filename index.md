---
layout: default
title: Modules
---

{% raw %}
<hr>

# <a id="augtool"></a> augtool


Uses the augtool utility to modify configuration files through the Augeas library.


<table class="table table-bordered table-striped">
<tr>
<th class="head">parameter</th>
<th class="head">required</th>
<th class="head">default</th>
<th class="head">choices</th>
<th class="head">comments</th>
</tr>
<tr>
<td>commands</td>
<td>yes</td>
<td></td>
<td><ul></ul></td>
<td>Either a list of augtool commands, or else a newline-separated list of commands</td>
</tr>
<tr>
<td>backup</td>
<td>no</td>
<td>True</td>
<td><ul><li>True</li><li>False</li></ul></td>
<td>Whether or not to make a backup of the files changed (passes <code>--backup</code> to augtool)</td>
</tr>
</table>

#### Examples

```
# YAML gives us a nice way of providing multiple augtool commands,
# separated by newlines.
#
# I'm escaping the $'s so Ansible doesn't eat them and augtool sees them.
action: augtool
args:
  commands: |
    defvar vsftpd /files/etc/vsftpd/vsftpd.conf
    set \$vsftpd/xferlog_std_format NO
    set \$vsftpd/log_ftp_protocol YES

# Or provide the commands as a list.
action: augtool
args:
  commands:
    - rm /files/etc/mdadm.conf/array[uuid = "{{ uuid }}"]
    - rm /files/etc/fstab/*[file = "/srv/storage/storage1"]

# Or provide the commands from a template.
action: augtool
args:
  commands: {{ lookup('template', 'samba.augtool.j2') }}

```

#### Notes
Unfortunately, this module really has no idempotency itself.  It's up to you to write idempotent augtool scripts.  Thankfully, that's pretty easy to do.

{% endraw %}
{% raw %}
<hr>

# <a id="load_gpg_vars"></a> load\_gpg\_vars


Decrypts and reads host variables from a PGP-encrypted YAML file. The YAML file is expected to be a YAML associative array mapping variables to their values.  Each variable is set as a host variable on every host this module is run against.

One name is special: if a `hosts` key is found, it is expected to have an associative array beneath it, the keys of which are host names and the values of which are themselves associative arrays of variables to be set on that specific host.  This allows setting variables on specific hosts, though note that only the hosts you run this module against will be affected regardless of the contents of the `hosts` key.

`gpg` is used to decrypt the file.  In theory either version 1 or version 2 will work, though this module has mostly been tested with version 2.  You may want to use `gpg-agent` to prompt for your passphrase, and also to cache your passphrase so that you don't have to retype it every time you run this module.


<table class="table table-bordered table-striped">
<tr>
<th class="head">parameter</th>
<th class="head">required</th>
<th class="head">default</th>
<th class="head">choices</th>
<th class="head">comments</th>
</tr>
<tr>
<td>path</td>
<td>yes</td>
<td></td>
<td><ul></ul></td>
<td>Path to the PGP-encrypted YAML file</td>
</tr>
<tr>
<td>gpg</td>
<td>no</td>
<td>gpg</td>
<td><ul></ul></td>
<td>Name of, or path to, <code>gpg</code></td>
</tr>
</table>

#### Examples

```
load_gpg_vars: path=secrets.yaml.gpg

# Example secrets.yaml.gpg file:
my_var_1: foo
my_var_2:
  - item 1
  - item 2
  - item 3
hosts:
  alice:
    my_var_3: alice secret key
  bob:
    my_var_3: bob secret key
    my_var_4:
      first_key: first val
      second_key: second val

#
# A slightly more realistic example: clients authenticating to the
# file server to mount a shared file system.
#

- hosts: all
  tasks:
    - load_gpg_vars: path=secrets.yaml.gpg

- hosts: file-servers
  tasks:
    - user: >
        state=present name=client shell=/sbin/nologin
        password={{ client_password|hash("sha512_crypt") }}

- hosts: clients
  tasks:
    - copy: dest=/etc/mount.credentials owner=root mode=0600
      args:
        content: |
          username=client
          password={{ client_password }}

# In secrets.yaml.gpg:
client_password: password1

```


{% endraw %}
{% raw %}
<hr>

# <a id="symlink"></a> symlink


This module exists solely because the standard *file* module will not create a symbolic link with a relative target.  This module will only overwrite existing symbolic links; if `path` exists but is not a symbolic link then this module will fail.


<table class="table table-bordered table-striped">
<tr>
<th class="head">parameter</th>
<th class="head">required</th>
<th class="head">default</th>
<th class="head">choices</th>
<th class="head">comments</th>
</tr>
<tr>
<td>src</td>
<td>yes</td>
<td></td>
<td><ul></ul></td>
<td>The path the symbolic link will refer to</td>
</tr>
<tr>
<td>force</td>
<td>no</td>
<td>no</td>
<td><ul><li>yes</li><li>no</li></ul></td>
<td>If true, the link will be created even if the src doesn't exist, or if the dest is a file that needs to be unlinked before being replaced with a symlink.</td>
</tr>
<tr>
<td>path</td>
<td>yes</td>
<td></td>
<td><ul></ul></td>
<td>The path to the symbolic link</td>
</tr>
</table>

#### Examples

```
- name: Use local PAM authentication files
  symlink: src={{ item }}-auth-local path=/etc/pam.d/{{ item }}-auth
  with_items:
    - system
    - password

```


{% endraw %}