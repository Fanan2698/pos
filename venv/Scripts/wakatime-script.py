#!c:\users\asus\desktop\boilerplate-pos\venv\scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'wakatime==13.0.7','console_scripts','wakatime'
__requires__ = 'wakatime==13.0.7'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('wakatime==13.0.7', 'console_scripts', 'wakatime')()
    )
