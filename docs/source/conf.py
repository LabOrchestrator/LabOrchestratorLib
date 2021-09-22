# Configuration file for the Sphinx documentation builder.
import sys
import re
from os.path import abspath, dirname, join

# add src to path

CURDIR = dirname(abspath(__file__))
ROOT = dirname(dirname(dirname(abspath(__file__))))

sys.path.insert(0, join(ROOT, "src"))

with open(join(ROOT, 'src', 'lab_orchestrator_lib', '__init__.py'), "r", encoding="utf-8") as f:
    VERSION = re.search('^__version__ = "(.*)"', f.read()).group(1)

# -- Project information

project = 'LabOrchestratorLib'
copyright = '2021, Marco Schlicht'
author = 'Marco Schlicht'

release = VERSION
version = VERSION

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'sphinx_autodoc_typehints',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'

# -- Options for EPUB output
epub_show_urls = 'footnote'

