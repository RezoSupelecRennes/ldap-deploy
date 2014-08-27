#!/usr/bin/env python3

from ldapmod import LDAPModifier, AUTH_BIND as bind, AUTH_EXTERNAL as external
import settings

l = LDAPModifier(bind_dn=settings.BIND_DN, bind_passwd=settings.BIND_PASSWD)

l.mod('conf/rootpw.ldif', external)
l.mod('conf/acl.ldif', external)
l.mod('conf/overlay/memberof.ldif', external)
l.mod('conf/overlay/refint.ldif', external)
l.add('/etc/ldap/schema/ppolicy.ldif', external)
l.mod('conf/overlay/ppolicy.ldif', external)
l.add('rez-rennes.fr/ou.ldif', bind)
l.add('rez-rennes.fr/access.ldif', bind)

for role in settings.ROLES:
    l.add('rez-rennes.fr/role.ldif', bind, bindings=role)
