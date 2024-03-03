Guidelines for Code Modification
================================

Coding Style
------------

* Use syntax compatible with Python `2.6+` and `3.1+`.
* Use docstrings with `pydoc` in mind
* Follow the PEP8 style guide: https://www.python.org/dev/peps/pep-0008/
* Always run `make test` before submitting a new PR. `pylint`, `flake8`,
  `pytest`, `doctest` and `shellcheck` need to be installed. (If you don't
  change any shell scripts you can run `make test_py` and you don't need the
  `shellcheck` dependency but it's an awesome tool, so check it out : )
* When breaking backward compatibility with old configuration files or plugins,
  please include a temporary workaround code that provides a compatibility
  layer and mark it with a comment that includes the word `COMPAT`. For
  examples, grep the code for the word `COMPAT`. :)


Patches
-------

Open a pull request on GitHub.

Version Numbering
-----------------

Three numbers, `A.B.C`, where
* `A` changes when configuration incompatibilities occur
* `B` changes when newer features are added
* `C` changes with each release


Starting Points
---------------

Good places to read about patrol internals are:

* `patrol/core/actions.py`
* `patrol/container/fsobject.py`

About the UI:

* `patrol/gui/widgets/browsercolumn.py`
* `patrol/gui/widgets/view_miller.py`
* `patrol/gui/ui.py`


Common Changes
==============

Adding options
--------------

* Add a default value in `rc.conf`, along with a comment that describes the option.
* Add the option to the `ALLOWED_SETTINGS` dictionary in the file
  `patrol/container/settings.py` in alphabetical order.
* Add an entry in the man page by editing `doc/patrol.pod`, then rebuild the man
  page by running `make man` in the patrol root directory

The setting is now accessible with `self.settings.my_option`, assuming self is a
subclass of `patrol.core.shared.SettingsAware`.


Adding colorschemes
-------------------

* Copy `patrol/colorschemes/default.py` to `patrol/colorschemes/myscheme.py`
  and modify it according to your needs. Alternatively, create a subclass of
  `patrol.colorschemes.default.Default` and override the `use` method, as it is
  done in the `Jungle` colorscheme.

* Add this line to your `~/.config/patrol/rc.conf`:
  `set colorscheme myscheme`


Change which programs start which file types
--------------------------------------------

Edit the configuration file `~/.config/patrol/rifle.conf`. The default one can
be obtained by running `patrol --copy-config rifle`.


Change which file extensions have which mime type
-------------------------------------------------

Modify `ranger/data/mime.types`. You may also add your own entries to `~/.mime.types`
