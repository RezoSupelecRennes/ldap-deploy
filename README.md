ldap-deploy
===========

Deployment script and configuration units for Rézo Rennes' OpenLDAP server.

Provisioning
------------

To install OpenLDAP on a Debian machine, run the `provision` script.

Preparing the database
----------------------

To configure an installed OpenLDAP server and fill the main DIT with initial
data:

    cp local_settings.sample.py local_settings.py
    # edit local_settings according to your needs
    ./deploy.py

The `deploy.py` script prompts you for template values not provided in the
file.

License
-------

This work is licensed under a MIT license.  See `LICENSE` for more information.
