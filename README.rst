Valkey — open-source, high-performance data store
=================================================

This TurnKey appliance bundles Valkey (an open, community-driven, in-memory data store) together with
a simple web UI (Redis Commander) served behind  Nginx over HTTPS.

Based on the TurnKey Redis appliance, it switches the server to Valkey while keeping Redis Commander
for browsing, inspecting, and basic key management.

Included
--------
- Valkey server (from Debian bookworm-backports)
- Redis Commander (via Node.js, behind Nginx on :443)
- Nginx reverse proxy (TLS with self-signed cert)
- TurnKey control panel integration (pm2, Confconsole, Webmin)

Access
------
- Valkey: TCP 6379 (binds to 127.0.0.1 by default; protected-mode configurable).  
  A password is generated at first boot and written to `/etc/valkey/valkey.conf` (`requirepass`);
  the same password is applied to Redis Commander’s Valkey connection.
- Redis Commander: `https://<ip-or-host>/redis-commander`  
  HTTP auth user is **admin**; you set its password during first boot.
- Webmin: `https://<ip-or-host>:12321` (login user **root**)
 
Credentials
-----------
- Webmin, SSH: username root
- Redis Commander: username admin

References
----------
- TurnKey Redis appliance: https://www.turnkeylinux.org/redis
- Valkey project: https://valkey.io/
- Valkey documentation: https://valkey.io/docs/
