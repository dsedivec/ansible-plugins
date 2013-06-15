# Various plug-ins for Ansible

These are a small collection of modules and plug-ins I created while
coming up with [Ansible](http://www.ansible.cc/) playbooks for my
network.  Ansible is a lightweight and simple system for managing
system configurations.

## What's here

* [`augtool` module][augtool_mod]: Modify configuration files using
  [Augeas' augtool][augtool] from Ansible.  Augeas is great when you
  want to edit a configuration file rather than replace it (e.g. with
  Ansible's built-in `template` module).

* [`load_gpg_vars` module][log_gpg_vars_mod]: Load host variables from
  an encrypted YAML file.  This is a quirky module but it can be
  useful for keeping information such as passwords for new user
  accounts you want to set up when provisioning a system.

* [`symlink` module][symlink_mod]: A module that solely creates symbolic
  links.  Its main selling point, and where it differs from Ansible's
  built-in `file` module, is that it lets you create relative links.

* `dns` lookup plug-in: Lets you resolve host names to their IP
  addresses.  This very simple module just calls `gethostbyname` for
  now, so it surely won't cover all use cases, and it definitely
  doesn't support IPv6.  For example, this will be replaced with the
  IP for `www.ansible.cc`:

        {{ lookup('dns', 'www.ansible.cc') }}

  I used this when making IPTables rules, which needed an IP address,
  but where I didn't want to "hard code" the IP in my playbook.

* `regexp_escape` filter plug-in: Gives you a `regexp_escape` filter.
  This can be useful when, for example, you're interpolating variables
  into the `regexp` argument of the built-in `lineinfile` module.

[augtool_mod]: http://dsedivec.github.io/ansible-plugins/#augtool
[augtool]: http://augeas.net/tour.html
[log_gpg_vars_mod]: http://dsedivec.github.io/ansible-plugins/#load_gpg_vars
[symlink_mod]: http://dsedivec.github.io/ansible-plugins/#symlink
