Valkey — open-source, high-performance data store
=================================================

This TurnKey appliance bundles Valkey (an open, community-driven, in-memory data store) together with
a simple web UI (Redis Commander) served behind Nginx over HTTPS.

Based on the TurnKey Redis appliance, it switches the server to Valkey while keeping Redis Commander
for browsing, inspecting, and basic key management.

Included
--------
- Valkey server from Debian 13 (Trixie)
- Redis Commander (via Node.js, behind Nginx on :443)
- Nginx reverse proxy (TLS with self-signed cert)
- TurnKey control panel integration (pm2, Confconsole, Webmin)

Access
------
- Valkey: TCP 6379 (binds to 127.0.0.1 by default; protected-mode configurable).  
  A database password is generated at first boot and written to ``/etc/valkey/valkey.conf`` (``requirepass``);
  the same password is applied to Redis Commander’s Valkey connection.
- Redis Commander (web UI): ``https://<ip-or-host>/redis-commander``  
  HTTP auth user is **admin**; you set the UI password during first boot (separate from the Valkey DB password).
- Webmin: ``https://<ip-or-host>:12321`` (login user **root**)
 
Credentials
-----------
- Webmin, SSH: username root
- Redis Commander: username admin

References
----------
- TurnKey Redis appliance: https://www.turnkeylinux.org/redis
- Valkey project: https://valkey.io/
- Valkey documentation: https://valkey.io/docs/

Security status (as of 2025-10-07)
----------------------------------
Debian Trixie currently provides `valkey-server 8.1.1+dfsg1-3`_ (source upload `2025-07-09`_).
Upstream fixed the recent Lua-related CVEs (CVE-2025-49844, CVE-2025-46817,
CVE-2025-46818, CVE-2025-46819) in versions `8.1.4`_ and `8.0.6`_ on 2025-10-03,
so ``8.1.1+dfsg1-3`` predates those fixes.

This appliance will pick up the fix as soon as Trixie publishes
an updated ``valkey-server`` package. If v19 ships before Trixie updates, it will
temporarily run an upstream Valkey binary, then revert to Debian once patched. Track the status on the `Debian security tracker`_.

.. _valkey-server 8.1.1+dfsg1-3: https://packages.debian.org/trixie/amd64/valkey-server
.. _2025-07-09: https://metadata.ftp-master.debian.org/changelogs//main/v/valkey/valkey_8.1.1%2Bdfsg1-3_changelog
.. _8.1.4: https://valkey.io/download/releases/v8-1-4/
.. _8.0.6: https://valkey.io/download/releases/v8-0-6/
.. _Debian security tracker: https://security-tracker.debian.org/tracker/source-package/valkey

