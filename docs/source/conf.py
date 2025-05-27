import os
import sys
from datetime import datetime

# Add the project root to the path for autodoc
sys.path.insert(0, os.path.abspath("../../src"))

# Project information
project = "moneyx"
copyright = f"{datetime.now().year}, devAbreu"
author = "devAbreu"

# The full version, including alpha/beta/rc tags
release = "0.1.1"

# Extensions
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
    "myst_parser",
]

# Templates
templates_path = ["_templates"]
exclude_patterns = []

# HTML output
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

# Intersphinx mappings
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "babel": ("https://babel.pocoo.org/en/latest/", None),
}

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False

# AutoDoc settings
autodoc_member_order = "bysource"
autodoc_typehints = "description"
autodoc_typehints_format = "short"

# MyST settings
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "tasklist",
]
