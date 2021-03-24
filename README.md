# Copier Templates Extensions

[![ci](https://github.com/pawamoy/copier-templates-extensions/workflows/ci/badge.svg)](https://github.com/pawamoy/copier-templates-extensions/actions?query=workflow%3Aci)
[![documentation](https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=flat)](https://pawamoy.github.io/copier-templates-extensions/)
[![pypi version](https://img.shields.io/pypi/v/copier-templates-extensions.svg)](https://pypi.org/project/copier-templates-extensions/)
[![gitter](https://badges.gitter.im/join%20chat.svg)](https://gitter.im/copier-templates-extensions/community)

Special Jinja2 extension for Copier that allows to load extensions using file paths relative to the template root instead of Python dotted paths.

## Requirements

Copier Templates Extensions requires Python 3.6 or above.

<details>
<summary>To install Python 3.6, I recommend using <a href="https://github.com/pyenv/pyenv"><code>pyenv</code></a>.</summary>

```bash
# install pyenv
git clone https://github.com/pyenv/pyenv ~/.pyenv

# setup pyenv (you should also put these three lines in .bashrc or similar)
export PATH="${HOME}/.pyenv/bin:${PATH}"
export PYENV_ROOT="${HOME}/.pyenv"
eval "$(pyenv init -)"

# install Python 3.6
pyenv install 3.6.12

# make it available globally
pyenv global system 3.6.12
```
</details>

## Installation

With `pip`:
```bash
python3.6 -m pip install copier-templates-extensions
```

With [`pipx`](https://github.com/pipxproject/pipx):
```bash
python3.6 -m pip install --user pipx

pipx install --python python3.6 copier-templates-extensions
```

## Usage

:warning: This is not yet functional.
We need something from Copier first:
a way to get the path to the template on the disk.
For example, Copier could set an environment variable
with the path to the temporary cloned template as value.

---

In your template configuration,
first add this extension,
then add your templates extensions
using relative file paths,
and the class name after a colon:

```yaml
_extensions:
- copier_templates_extensions.Ext
- extensions/context.py:ContextUpdateExtension
- extensions/slugify.py:SlugifyExtension
```