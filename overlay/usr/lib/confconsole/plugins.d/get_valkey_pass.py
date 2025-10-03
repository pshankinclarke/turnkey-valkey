'''Check Valkey password'''

import os
import subprocess
from subprocess import PIPE

TITLE = "Check valkey password"


def run():
    requirepass = subprocess.Popen(['turnkey-valkey-pw', 'get'], stdout=PIPE)
    requirepass_out, requirepass_err = requirepass.communicate()
    if not requirepass_out:
        console.msgbox(TITLE,
                       "Something is wrong with valkey configuration file,"
                       " please check your valkey.conf")
    else:
        password = requirepass_out.decode()
        with open('/root/valkey_password.txt', 'w') as fob:
            fob.write(password)
        console.msgbox(TITLE,
                       "Password is:\n\n{}\nIt has also been saved as"
                       " /root/valkey_password.txt".format(password))
