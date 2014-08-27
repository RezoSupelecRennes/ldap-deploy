#!/usr/bin/env python3

import jinja2
import subprocess

from ldapmod.filler import Filler

AUTH_BIND = 0
AUTH_EXTERNAL = 1

class LDAPModifier(object):
    """Wrapper for ldapadd and ldapmodify using Jinja2 templates

    An LDIF file can contain Jinja2 template variables that will be determined
    when loaded. Bindings can be passed as arguments or given interactively.

    >>> l = LDAPModifier(bind_dn='cn=admin,dc=example,dc=org' bind_passwd='very secret')
    >>> john_bindings = { 'user': 'john.doe', 'name': 'John Doe' }
    >>> l.add('user_template.ldif', AUTH_BIND, john_bindings)
    passwd: not that secret
    """

    BIND_ARGS = ['-x', '-H', 'ldapi:///']
    EXTERNAL_ARGS = ['-Y', 'EXTERNAL', '-H', 'ldapi:///']

    def __init__(self, bind_dn, bind_passwd, bind_args=BIND_ARGS, external_args=EXTERNAL_ARGS):
        self.bind_passwd = bind_passwd
        self.bind_dn = bind_dn
        self.bind_args = bind_args
        self.external_args = external_args
        self.filler = Filler()

    def mod(self, path, auth, add=False, bindings={}):
        if add:
            base = ['ldapadd']
        else:
            base = ['ldapmodify']

        if auth == AUTH_BIND:
            auth_args = self.bind_args + ['-D', self.bind_dn, '-w', self.bind_passwd]
        elif auth == AUTH_EXTERNAL:
            auth_args = self.external_args
            base = ['sudo'] + base
        else:
            raise RuntimeError('Invalid argument: auth={}'.format(auth))

        ldif = self.filler.loadi(path, bindings=bindings).encode('utf-8')

        p = subprocess.Popen(base + auth_args,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
        (out, err) = p.communicate(input=ldif)

        print(out.decode('utf-8'), '\n', err.decode('utf-8'))

    def add(self, path, auth, bindings={}):
        self.mod(path, auth, add=True, bindings=bindings)
