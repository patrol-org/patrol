#!/usr/bin/env python

from __future__ import (absolute_import, division, print_function)

import sys
import time

sys.path.insert(0, '../..')
sys.path.insert(0, '.')


def main():
    import patrol.container.directory
    import patrol.core.shared
    import patrol.container.settings
    import patrol.core.cli
    from patrol.ext.openstruct import OpenStruct
    patrol.args = OpenStruct()
    patrol.args.clean = True
    patrol.args.debug = False

    settings = patrol.container.settings.Settings()
    patrol.core.shared.SettingsAware.settings_set(settings)
    cli = patrol.core.cli.CLI()
    patrol.core.shared.CLIAware.cli_set(cli)

    time1 = time.time()
    cli.initialize()
    try:
        usr = patrol.container.directory.Directory('/usr')
        usr.load_content(schedule=False)
        for fileobj in usr.files:
            if fileobj.is_directory:
                fileobj.load_content(schedule=False)
    finally:
        cli.destroy()
    time2 = time.time()
    print("%dms" % ((time2 - time1) * 1000))


if __name__ == '__main__':
    main()
