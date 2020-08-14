# netbox-remote-authn-ldap-authz
Remote authentication and LDAP authorization for Netbox

Allows you to use your own authentication system in front of Netbox for authentication while keep using LDAP within Netbox to acquire users' groups for example, for authorization.

This code is based on Netbox 2.8.9 and hasn't been thoroughly tested.

## Usage

Work has been done using Docker but you can adapt it for a non-Docker deployment.

Make sure you use the LDAP version of Netbox Docker image, like _netboxcommunity/netbox:v2.8.9-ldap_ for example.

Bind mount the files to the Netbox Docker containers. Example:
```
    volumes:
    - ./startup_scripts:/opt/netbox/startup_scripts:z,ro
    - ./initializers:/opt/netbox/initializers:z,ro
    - ./configuration/configuration.py:/etc/netbox/config/configuration.py:z,ro
    - ./configuration/gunicorn_config.py:/etc/netbox/config/gunicorn_config.py:z,ro
    - ./reports:/etc/netbox/reports:z,ro
    - ./scripts:/etc/netbox/scripts:z,ro
    - ./nginx-config:/etc/netbox-nginx:z
    - ./static-files:/opt/netbox/netbox/static:z
    - ./media-files:/opt/netbox/netbox/media:z
    - ./custom/remote_ldap_config.py:/etc/netbox/config/remote_ldap_config.py:z,ro
    - ./custom/remote_ldap_config.docker.py:/opt/netbox/netbox/netbox/remote_ldap_config.py:z,ro
    - ./custom/settings.py:/opt/netbox/netbox/netbox/settings.py:z,ro
    - ./custom/middleware.py:/opt/netbox/netbox/utilities/middleware.py:z,ro
    - ./custom/auth_backends.py:/opt/netbox/netbox/utilities/auth_backends.py:z,ro
```

Configure authentication and authorization with environment variables for your Netbox containers. Here's an example:

```
    environment:
      LOGIN_REQUIRED: "True"
      REMOTE_AUTH_HEADER: "HTTP_X_POMERIUM_CLAIM_USER"
      AUTH_LDAP_SERVER_URI: "ldaps://ldap.contoso.com"
      AUTH_LDAP_BIND_DN: "uid=netbox,ou=services,ou=accounts,ou=contoso,dc=contoso,dc=com"
      AUTH_LDAP_BIND_PASSWORD: "mysuperpassword"
      AUTH_LDAP_USER_SEARCH_BASEDN: "ou=people,ou=accounts,ou=contoso,dc=contoso,dc=com"
      AUTH_LDAP_GROUP_SEARCH_BASEDN: "ou=groups,ou=contoso,dc=contoso,dc=com"
      AUTH_LDAP_FIND_GROUP_PERMS: "True"
      AUTH_LDAP_REQUIRE_GROUP_DN: "cn=netbox-users,ou=groups,ou=contoso,dc=contoso,dc=com"
      AUTH_LDAP_IS_ADMIN_DN: "cn=netbox-admins,ou=groups,ou=contoso,dc=contoso,dc=com"
      AUTH_LDAP_IS_SUPERUSER_DN: "cn=netbox-superusers,ou=groups,ou=contoso,dc=contoso,dc=com"
      AUTH_LDAP_USER_SEARCH_ATTR: "uid"
      AUTH_LDAP_GROUP_SEARCH_CLASS: "groupOfNames"
      AUTH_LDAP_GROUP_TYPE: "GroupOfNamesType"
      AUTH_LDAP_ATTR_FIRSTNAME: "givenName"
      AUTH_LDAP_ATTR_LASTNAME: "sn"
      AUTH_LDAP_ATTR_MAIL: "mail"
      LDAP_IGNORE_CERT_ERRORS: "False"
```

In this example, the HTTP header is _X-Pomerium-Claim-User_.

You must be sure that your front-end web server always sets or strips that header based on the appropriate authentication checks, never permitting an end-user to submit a fake (or spoofed) header value. Since the HTTP headers _X-Auth-User_ and _X-Auth_User_ (for example) both normalize to the _HTTP_X_AUTH_USER_, you must also check that your web server doesn’t allow a spoofed header using underscores in place of dashes.

For additional information about LDAP configuration, you can read the documation here: https://django-auth-ldap.readthedocs.io/en/latest/
