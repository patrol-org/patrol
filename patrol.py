#!/usr/bin/python -O
# This file is part of patrol, fork of range.  (coding: utf-8)
# License: GNU GPL version 3, see the file "AUTHORS" for details.

# =====================
# This embedded bash script can be executed by sourcing this file.
# It will cd to patrol's last location after you exit it.
# The first argument specifies the command to run patrol, the
# default is simply "patrol". (Not this file itself!)
# The other arguments are passed to patrol.
"""":
temp_file="$(mktemp -t "patrol_cd.XXXXXXXXXX")"
patrol="${1:-patrol}"
if [ -n "$1" ]; then
    shift
fi
"$patrol" --choosedir="$temp_file" -- "${@:-$PWD}"
return_value="$?"
if chosen_dir="$(cat -- "$temp_file")" && [ -n "$chosen_dir" ] && [ "$chosen_dir" != "$PWD" ]; then
    cd -- "$chosen_dir"
fi
rm -f -- "$temp_file"
return "$return_value"
"""

from __future__ import (absolute_import, division, print_function)

import sys

# Need to find out whether or not the flag --clean was used ASAP,
# because --clean is supposed to disable bytecode compilation
ARGV = sys.argv[1:sys.argv.index('--')] if '--' in sys.argv else sys.argv[1:]
sys.dont_write_bytecode = '-c' in ARGV or '--clean' in ARGV

# Start patrol
import patrol  # NOQA pylint: disable=import-self,wrong-import-position
sys.exit(patrol.main())  # pylint: disable=no-member
