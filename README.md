# Copier Templates Extensions

[![ci](https://github.com/pawamoy/copier-templates-extensions/workflows/ci/badge.svg)](https://github.com/pawamoy/copier-templates-extensions/actions?query=workflow%3Aci)
[![documentation](https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=flat)](https://pawamoy.github.io/copier-templates-extensions/)
[![pypi version](https://img.shields.io/pypi/v/copier-templates-extensions.svg)](https://pypi.org/project/copier-templates-extensions/)
[![gitpod](https://img.shields.io/badge/gitpod-workspace-blue.svg?style=flat)](https://gitpod.io/#https://github.com/pawamoy/copier-templates-extensions)
[![gitter](https://badges.gitter.im/join%20chat.svg)](https://gitter.im/copier-templates-extensions/community)

Special Jinja2 extension for Copier that allows to load extensions using file paths relative to the template root instead of Python dotted paths.

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
_jinja_extensions:
- copier_templates_extensions.TemplateExtensionLoader
- extensions/context.py:ContextUpdater
- extensions/slugify.py:SlugifyExtension
```

With this example, you are supposed to have an `extensions`
directory at the root of your template containing two modules:
`context.py` and `slugify.py`.

```
📁 template_root
├── 📄 abc.txt.jinja
├── 📄 copier.yml
└── 📁 extensions
    ├── 📄 context.py
    └── 📄 slugify.py
```

See [Context hook extension](#context-hook-extension)
to see how the `ContextUpdater` class can be written.

The `SlugifyExtension` class could be written like this:

```python
import re
import unicodedata

from jinja2.ext import Extension


# taken from Django
# https://github.com/django/django/blob/main/django/utils/text.py
def slugify(value, allow_unicode=False):
    """
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')


class SlugifyExtension(Extension):
    def __init__(self, environment):
        super().__init__(environment)
        environment.filters["slugify"] = slugify
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

In your Jinja templates, you will now have access
to the `{{ say }}` variable directly.

This can be extremely useful in template projects
where you don't want to ask too many questions to the users
and instead infer some values from their answers.

Consider the following example:
you ask your users if they want to generate
a CLI app or a web API.
Depending on their answer,
the main Python module should be named
`cli.py` or `app.py`.

Without the context hook,
you would need to write a Jinja macro somewhere,
or update the context directly in Jinja,
and import this file (still using Jinja)
*in the filename of the module*:

```jinja
{# using macros #}
{%- macro module_name() %}
  {%- if project_type == "webapi" %}app{% else %}cli{% endif %}
{%- endmacro %}
```

```jinja
{# or enhancing the context #}
{#- Initiate context with a copy of Copier answers -#}
{%- set ctx = _copier_answers.copy() -%}

{#- Populate our new variables -#}
{%- set _ = ctx.update({"module_name": ("app" if project_type == "webapi" else "cli") -%}
```

```
📁 template_root
├── 📄 copier.yml
├── 📄 macros      # the macros file
├── 📄 context     # the context file
├── 📁 extensions
│   └── 📄 slugify.py
└── 📁 {{project_name|slugify}}
    │
    │   # using the macros
    ├── 📄 {% import 'macros' as macros with context %}{{macros.module_name()}}.py.jinja
    │
    │   # or using the enhanced context
    └── 📄 {% from 'context' import ctx with context %}{{ctx.module_name}}.py.jinja
```

As you can see, both forms are really ugly to write:

- the `macros` or `context` can only be placed in the root,
  as slashes `/` are not allowed in filenames
- you must use spaces and single-quotes
  (double-quotes are not valid filename characters on Windows)
  in your templated filenames, which is not clean
- filenames are very long

**Using our context hook instead makes it so easy and clean!**

```python
from copier_templates_extensions import ContextHook


class ContextUpdater(ContextHook):
    def hook(self, context):
        return {"module_name": "app" if context["project_type"] == "webapi" else "cli"}
```

```
📁 template_root
├── 📄 copier.yml
├── 📁 extensions
│   ├── 📄 slugify.py
│   └── 📄 context.py
└── 📁 {{project_name|slugify}}
    └── 📄 {{module_name}}.py.jinja
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
