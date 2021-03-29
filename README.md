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
pip install copier-templates-extensions
```

With [`pipx`](https://github.com/pipxproject/pipx):
```bash
pip install --user pipx

pipx install copier
pipx inject copier copier-templates-extensions
```

## Usage

In your template configuration,
first add our loader extension,
then add your templates extensions
using relative file paths,
and the class name after a colon:

```yaml
_extensions:
- copier_templates_extensions.TemplateExtensionLoader
- extensions/context.py:ContextUpdater
- extensions/slugify.py:SlugifyExtension
```

### Context hook extension

This package also provides a convenient extension class
allowing template writers to update the context used
to render templates, in order to add, modify or remove
items of the context.

In one of your relative path extensions modules,
create a class that inherits from `ContextHook`,
and override its `hook` method:

```python
from copier_templates_extensions import ContextHook


class ContextUpdater(ContextHook):
    def hook(self, context):
        new_context = {}
        new_context["say"] = "hello " + context["name"]
        return new_context
```

Using the above example, your context will be updated
with the `new_context` returned by the method.
If you prefer to modify the context in-place instead,
for example to *remove* items from it,
set the `update` class attribute to `False`:

```python
from copier_templates_extensions import ContextHook


class ContextUpdater(ContextHook):
    update = False

    def hook(self, context):
        context["say"] = "hello " + context["name"]
        del context["name"]
```

## How does it work?

Beware the ugly hack!
Upon loading the special *loader* extension,
the function responsible for importing
a Python object using its dotted-path (a string)
is patched in the `jinja.environment` module,
where it's used to load extensions.
The patched version adds support
for loading extensions using relative file paths.
The file system loader of the Jinja environment
and its `searchpaths` attribute are used to
find the local clone of the template and determine
the absolute path of the extensions to load.