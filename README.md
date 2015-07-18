# Various plug-ins for Ansible

These are a small collection of modules and plug-ins I created while
coming up with [Ansible](http://www.ansibleworks.com/) playbooks for
my network.  Ansible is a lightweight and simple system for managing
system configurations.

This software has the same license as Ansible, GPLv3.

## What's here

* [`augtool` module][augtool_mod]: Modify configuration files using
  [Augeas' augtool][augtool] from Ansible.  Augeas is great when you
  want to edit a configuration file rather than replace it (e.g. with
  Ansible's built-in `template` module).

* [`load_gpg_vars` module][load_gpg_vars_mod]: Load host variables from
  an encrypted YAML file.  This is a quirky module but it can be
  useful for keeping information such as passwords for new user
  accounts you want to set up when provisioning a system.

  Note: this should probably be replaced by [`ansible-vault`][vault]
  once Ansible 1.5 is released.

* `dns` lookup plug-in: Lets you resolve host names to their IP
  addresses.  This very simple module just calls `gethostbyname` for
  now, so it surely won't cover all use cases, and it definitely
  doesn't support IPv6.  For example, this will be replaced with the
  IP for `www.ansible.cc`:

        {{ lookup('dns', 'www.ansible.cc') }}

  I used this when making IPTables rules, which needed an IP address,
  but where I didn't want to "hard code" the IP in my playbook.

* `hash` filter plug-in: If you have
  [passlib](http://pythonhosted.org/passlib/) installed, you can use
  this filter plug-in to hash passwords.  For example:

        {{ plain_text_password|hash("sha512_crypt", salt_size=16) }}

  See <http://pythonhosted.org/passlib/lib/passlib.hash.html> for a
  list of supported hashes and their arguments.

  This filter could be particularly useful in conjunction with plain
  text passwords kept in a GPG file using the `load_gpg_vars` module,
  above.  See [that module's documentation][load_gpg_vars_mod] for an
  example.

* `regexp_escape` filter plug-in: Gives you a `regexp_escape` filter.
  This can be useful when, for example, you're interpolating variables
  into the `regexp` argument of the built-in `lineinfile` module.

* `vault_from_gpg_agent.py` script that allows `ansible`'s `vault` to
  read its password via `gpg-agent`. See this [mailing_list_post] for
  the rationale. The script can be used like this:

        ansible-playbook setup.yml --vault-password-file vault_from_gpg_agent.py
  
  The script must be executable (`chmod +x vault_from_gpg_agent.py`).

[augtool_mod]: http://dsedivec.github.io/ansible-plugins/#augtool
[augtool]: http://augeas.net/tour.html
[load_gpg_vars_mod]: http://dsedivec.github.io/ansible-plugins/#load_gpg_vars
[symlink_mod]: http://dsedivec.github.io/ansible-plugins/#symlink
[vault]: http://blog.ansibleworks.com/2014/02/19/ansible-vault/
[mailing_list_post]: http://grokbase.com/t/gg/ansible-project/14810bdwye/read-vault-password-using-gpg-agent
