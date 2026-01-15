'''Check Valkey password'''

import os
import subprocess
from subprocess import PIPE

TITLE = "Check valkey password"


def run():
    # Note: 'console' is provided by the confconsole plugin framework at runtime
    try:
        requirepass_out = subprocess.check_output(['turnkey-valkey-pw', 'get'], 
                                                   timeout=5).decode().strip()
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError) as e:
        console.msgbox(TITLE,
                       "Something is wrong with valkey configuration file,"
                       " please check your valkey.conf")
        return
    
    if not requirepass_out:
        console.msgbox(TITLE,
                       "Something is wrong with valkey configuration file,"
                       " please check your valkey.conf")
    else:
        password = requirepass_out
        with open('/root/valkey_password.txt', 'w') as fob:
            fob.write(password)
        console.msgbox(TITLE,
                       "Password is:\n\n{}\nIt has also been saved as"
                       " /root/valkey_password.txt".format(password))
