#!/usr/bin/env python3

from ldapmod import LDAPModifier, AUTH_BIND, AUTH_EXTERNAL

import settings

def main(path, auth, add):
    l = LDAPModifier(bind_dn=settings.BIND_DN, bind_passwd=settings.BIND_PASSWD)
    l.mod(path, auth, add=add)

if __name__ == '__main__':
    import sys

    if len(sys.argv) != 4:
        sys.exit('Usage: {} path {{bind|external}} {{mod|add}}'.format(sys.argv[0]))

    path = sys.argv[1]
    auth_str = sys.argv[2]
    op_str = sys.argv[3]

    if auth_str == 'bind':
        auth = AUTH_BIND
    elif auth_str == 'external':
        auth = AUTH_EXTERNAL
    else:
        sys.exit('Error: auth must be bind or external')

    if op_str == 'mod':
        add = False
    elif op_str == 'add':
        add = True
    else:
        sys.exit('Error: mode must be add or mod')

    main(path, auth, add)
