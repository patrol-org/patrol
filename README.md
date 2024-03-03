patrol 0.1.0
============

<img src="https://patrol-org.github.io/logo.png" width="150">

[![Build status](https://img.shields.io/github/actions/workflow/status/patrol-org/patrol/build.yml)](https://github.com/patrol-org/patrol/actions/workflows/build.yml)
![GitHub Release](https://img.shields.io/github/v/release/patrol-org/patrol)

patrol is a console data explorer with VI key bindings.  It provides a
minimalistic and nice curses interface with a view on the data hierarchy.
It is a fork of the [ranger](https://github.com/patrol-org/patrol) file manager adding a client-server protocol to handle arbitrary data.

![screenshot](https://raw.githubusercontent.com/patrol-org/patrol-assets/master/screenshots/screenshot.png)

This file describes patrol and how to get it to run.  For instructions on the
usage, please read the man page (`man patrol` in a terminal).  See `HACKING.md`
for development-specific information.

For configuration, check the files in `patrol/config/` or copy the
default config to `~/.config/patrol` with `patrol --copy-config`
(see [instructions](#getting-started)).

The `examples/` directory contains several scripts and plugins that demonstrate how
patrol can be extended or combined with other programs.  These files can be
found in the git repository or in `/usr/share/doc/patrol`. -->

A note to packagers: Versions meant for packaging are published as GitHub releases.


About
-----
* Authors:     see `AUTHORS` file
* License:     GNU General Public License Version 3
* Website:     https://patrol-org.github.io/
* Download:    https://patrol-org.github.io/patrol-stable.tar.gz
* Bug reports: https://github.com/patrol-org/patrol/issues
* git clone    https://github.com/patrol-org/patrol.git


Design Goals
------------
* An easily maintainable data explorer in a high level language
* A quick way to switch node and browse the data tree
* Keep it small but useful, do one thing and do it well
* Console-based, with smooth integration into the unix shell


Features
--------
* UTF-8 Support  (if your Python copy supports it)
* Multi-column display
* Support any data with client-server provider
* VIM-like console and hotkeys
* Tabs, bookmarks, mouse support...


Dependencies
------------
* Python (`>=2.6` or `>=3.1`) with the `curses` module
  and (optionally) wide-unicode support
* A pager (`less` by default)

### Optional dependencies

For general usage:

* `python-bidi` (Python package) to display right-to-left file names correctly
  (Hebrew, Arabic)

For enhanced functionalities (with builtin providers):

* [`jc`](https://github.com/kellyjonbrazil/jc) for many cli commands

Installing
----------
Use the package manager of your operating system to install patrol.
You can also install patrol through PyPI: `pip install patrol-cli`.
However, it is recommended to use [`pipx`](https://pypa.github.io/pipx/) instead
(to benefit from isolated environments). Use
`pipx run --spec patrol-cli ranger` to install and run ranger in one step.

### Installing from a clone
Note that you don't *have* to install patrol; you can simply run `patrol.py`.

To install patrol manually:
```
sudo make install
```

This translates roughly to:
```
sudo python setup.py install --optimize=1 --record=install_log.txt
```

This also saves a list of all installed files to `install_log.txt`, which you can
use to uninstall patrol.


Getting Started
---------------
After starting patrol, you can use the Arrow Keys or `h` `j` `k` `l` to
navigate, `Enter` to act on a node or `q` to quit.  The third column shows a
preview of the current node children.  The second is the main column and the first shows
the node parents.

Patrol can automatically copy default configuration files to `~/.config/patrol`
if you run it with the switch `--copy-config=( rc | ... | all )`.
See `patrol --help` for a description of that switch.  Also check
`patrol/config/` for the default configuration.


Going Further
---------------
* To get the most out of patrol, read the [Official User Guide](https://github.com/patrol-org/patrol/wiki/Official-user-guide).
* For frequently asked questions, see the [FAQ](https://github.com/patrol-org/patrol/wiki/FAQ%3A-Frequently-Asked-Questions).
* For more information on customization, see the [wiki](https://github.com/patrol-org/patrol/wiki).
