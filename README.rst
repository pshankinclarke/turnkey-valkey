Redis - Open Source, In-memory Data Structure Store
===================================================

`Redis`_ can be used as a database, cache or message broker. It supports data
structures such as strings, hashes, lists, sets, sorted sets
with range queries, bitmaps, hyperloglogs and geospatial indexes
with radius queries. Redis has built-in replication, Lua scripting,
LRU eviction, transactions and different levels of on-disk persistence,
and provides high availability via `Redis Sentinel`_ (requires install of
Debian `redis-sentinel`_ package) and automatic partitioning with
`Redis Cluster`_.

This appliance includes all the standard features in `TurnKey Core`_,
and on top of that:

- Redis configurations:

    - Installed from debian package repository (auto security updates).
    - Includes web based management tool `Redis Commander`_.
    - Complex Redis system password auto-generated on firstboot (security).
    - Confconsole plugin provided to view Redis system password (convenience).

   **Security note**: Updates to `Redis Commander`_ may require supervision so
   they **ARE NOT** configured to install automatically. See `Plone
   documentation`_ for upgrading.

- SSL support out of the box.
- Postfix MTA (bound to localhost) to allow sending of email from web
  applications (e.g., password recovery).

Supervised Manual Redis Commander Update
----------------------------------------

Always ensure that you have a current and tested backup before performing an
upgrade. Ideally also do a test upgrade proceedure on a development server,
before updating your production server.::

    su - node -c "cd /opt/tklweb-cp && npm update"

Credentials *(passwords set at first boot)*
-------------------------------------------

- Webmin, SSH: username **root**
- Redis-commander: username **admin**

.. _Redis: https://redis.io/
.. _Redis Sentinel: https://redis.io/topics/sentinel
.. _redis-sentinel: https://packages.debian.org/stretch/redis-sentinel
.. _Redis Cluster: https://redis.io/topics/cluster-tutorial
.. _TurnKey Core: https://www.turnkeylinux.org/core
.. _Redis Commander: https://joeferner.github.io/redis-commander/
