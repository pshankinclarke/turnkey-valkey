#!/usr/bin/python3
"""Set Redis-commander password and Valkey bind and protected-mode
directives.

Option:
    --bind=             unless provided, will ask interactively.
                            [localhost|all]
    --pass=             unless provided, will ask interactively.
                            WARNING: set good password if unprotected!
    --protected_mode=   unless provided, will ask interactively.
                            [1|0]
"""

import sys
import getopt
import subprocess
import os

from netinfo import get_ifnames, InterfaceInfo
from libinithooks.dialog_wrapper import Dialog


def usage(s=None):
    if s:
        print("Error:", s, file=sys.stderr)
    print(f"Syntax: {sys.argv[0]} [options]", file=sys.stderr)
    print(__doc__, file=sys.stderr)
    sys.exit(1)


def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "h",
                                       ['help', 'pass=',
                                        'bind=', 'protected_mode='])
    except getopt.GetoptError as e:
        usage(e)

    password = ""
    bind = ""
    protected_mode = ""
    for opt, val in opts:
        if opt in ('-h', '--help'):
            usage()
        elif opt == '--bind':
            bind = val
        elif opt == '--pass':
            password = val
        elif opt == '--protected_mode':
            protected_mode = val

    # Create Dialog instance once for reuse
    d = Dialog('TurnKey Linux - First boot configuration')

    if not password:
        password = d.get_password(
             "Redis-commander 'admin' password",
             "Enter password for 'admin' access to redis-commander UI")

    if not bind:
        bind = d.menu(
            "Interface(s) for Valkey to bind to",
            ("Interface for Valkey to bind to?\n\nIf you wish to securely"
             " allow remote connections using 'all', ensure the system"
             " firewall is enabled & block all traffic on port 6379,"
             " except for the desired remote IP(s).\n\nManually edit the"
             " config file to set a custom interface."),
            choices=(
                ("localhost", "Valkey will not respond to remote computer"),
                ("all", "Valkey will allow all connections"),
                ("local", "Enter custom range")))
    if bind == "all":
        bind_ip = "0.0.0.0"
    elif bind == "local":
        localaddr = InterfaceInfo(get_ifnames()[0]).address
        bind_ip = d.get_input("Bind IP Range", "Enter bind ip range", localaddr)
    else:
        bind_ip = "127.0.0.1"

    if not protected_mode:
        protected_mode = d.yesno(
                'Keep protected-mode enabled?',
                "In protected  mode Valkey only replies to queries from"
                " localhost. Clients connecting from other addresses will"
                " receive an error, noting why & how to configure Valkey.\n"
                "\nUnless you set really good password, this is recommended",
                'Yes', 'No')

    protected_mode_str = {True: "yes", False: "no", "1": "yes", "0": "no"}
    protected_mode = protected_mode_str[protected_mode]
    conf = "/etc/valkey/valkey.conf"
    redis_commander_conf = "/opt/tklweb-cp/ecosystem.config.js"
    
    # Update valkey.conf using Python file I/O instead of subprocess sed calls
    import re
    with open(conf, 'r') as f:
        conf_content = f.read()
    
    conf_content = re.sub(r'^bind .*', f'bind {bind_ip}', conf_content, flags=re.MULTILINE)
    conf_content = re.sub(r'^protected-mode .*', f'protected-mode {protected_mode}', conf_content, flags=re.MULTILINE)
    
    with open(conf, 'w') as f:
        f.write(conf_content)
    
    # Update redis-commander config using Python file I/O
    with open(redis_commander_conf, 'r') as f:
        rc_content = f.read()
    
    rc_content = re.sub(r'HTTP_PASSWORD": ".*?"', f'HTTP_PASSWORD": "{password}"', rc_content)
    
    with open(redis_commander_conf, 'w') as f:
        f.write(rc_content)

    # restart valkey and redis commander if running so change takes effect
    if subprocess.run(["systemctl", "is-active", "--quiet", "valkey-server.service"],
                      timeout=5).returncode == 0:
        subprocess.run(["service", "valkey-server", "restart"], timeout=30)

    # reload and restart pm2 so changes take affect
    # and save them to /home/node/.pm2/dump.pm2
    if subprocess.run(["systemctl", "is-active", "--quiet", "pm2-node.service"],
                      timeout=5).returncode == 0:
        env = os.environ.copy()
        env["PM2_HOME"] = "/home/node/.pm2"
        env["PATH"] = "/usr/local/bin:/usr/bin:/bin:/usr/local/sbin:/usr/sbin:/sbin"
        try:
            subprocess.run(["systemctl", "reload","pm2-node.service"], timeout=10)
            subprocess.run(["su", "-s","/bin/sh", "-c", "pm2 reload /opt/tklweb-cp/ecosystem.config.js", "node"], 
                         check=True, env=env, timeout=30)
            subprocess.run(["su", "-s","/bin/sh", "-c", "pm2 save", "node"], 
                         check=True, env=env, timeout=15)
            subprocess.run(["service", "pm2-node", "restart"], timeout=30)
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError) as e:
            # Log specific error but continue
            print(f"Warning: PM2 restart failed: {e}", file=sys.stderr)
            pass


if __name__ == "__main__":
    main()
