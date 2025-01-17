# This file is part of patrol, fork of range.
# License: GNU GPL version 3, see the file "AUTHORS" for details.

from __future__ import (absolute_import, division, print_function)

from io import open
from os import devnull
from subprocess import PIPE, CalledProcessError

from ranger.ext.popen23 import Popen23

ENCODING = 'utf-8'


def check_output(popenargs, **kwargs):
    """Runs a program, waits for its termination and returns its output

    This function is functionally identical to python 2.7's subprocess.check_output,
    but is favored due to python 2.6 compatibility.

    Will be run through a shell if `popenargs` is a string, otherwise the command
    is executed directly.

    The keyword argument `decode` determines if the output shall be decoded
    with the encoding UTF-8.

    Further keyword arguments are passed to Popen.
    """

    do_decode = kwargs.pop('decode', True)
    kwargs.setdefault('stdout', PIPE)
    kwargs.setdefault('shell', isinstance(popenargs, str))

    if 'stderr' in kwargs:
        with Popen23(popenargs, **kwargs) as process:
            stdout, _ = process.communicate()
    else:
        with open(devnull, mode='w', encoding="utf-8") as fd_devnull:
            with Popen23(popenargs, stderr=fd_devnull, **kwargs) as process:
                stdout, _ = process.communicate()

    if process.returncode != 0:
        error = CalledProcessError(process.returncode, popenargs)
        error.output = stdout
        raise error

    if do_decode and stdout is not None:
        stdout = stdout.decode(ENCODING)

    return stdout


def spawn(*popenargs, **kwargs):
    """Runs a program, waits for its termination and returns its stdout

    This function is similar to python 2.7's subprocess.check_output,
    but is favored due to python 2.6 compatibility.

    The arguments may be:

        spawn(string)
        spawn(command, arg1, arg2...)
        spawn([command, arg1, arg2])

    Will be run through a shell if `popenargs` is a string, otherwise the command
    is executed directly.

    The keyword argument `decode` determines if the output shall be decoded
    with the encoding UTF-8.

    Further keyword arguments are passed to Popen.
    """
    if len(popenargs) == 1:
        return check_output(popenargs[0], **kwargs)
    return check_output(list(popenargs), **kwargs)
