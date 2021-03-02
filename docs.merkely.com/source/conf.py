# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

sys.path.append(os.path.abspath("./_ext"))
sys.path.append(os.path.abspath("/app/source"))
extensions = [
    'describe_command',
    'describe_fingerprint',
    'sphinx_copybutton'
]

import sphinx_bootstrap_theme

# -- Project information -----------------------------------------------------

project = 'Merkely'
copyright = '2021, Merkely'
author = 'Merkely'

html_logo = "_static/images/w-merkely-white-01.png"

# -- General configuration ---------------------------------------------------

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# Don't show the "Created using Sphinx message in the page footer
html_show_sphinx = False

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['app']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = 'alabaster'
# html_theme = "furo"
html_theme = 'bootstrap'
html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()

html_theme_options = {
    'bootswatch_theme': "cosmo",
    'navbar_title': " ",
    'navbar_site_name': "Contents",
    'navbar_sidebarrel': False,
    'navbar_pagenav': False,
    'source_link_position': "do-not-show",
}
# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_css_files = [
    "merkely-custom.css",
]

html_extra_path = ['CNAME', '.nojekyll']

# This is a hack to get around a sphinx bug that does not
# copy static files correctly on change
# see https://github.com/sphinx-doc/sphinx/issues/2090
def env_get_outdated(app, env, added, changed, removed):
    return ['index']


def setup(app):
    source_dir = os.path.dirname(__file__)
    ci_names = ['generic_docker', 'github_actions', 'bitbucket_pipelines']
    #create_reference_rst_files(source_dir, ci_names)
    app.add_css_file("merkely-custom.css")
    app.connect('env-get-outdated', env_get_outdated)


def create_reference_rst_files(source_dir, ci_names):
    print(source_dir)
    index = ""
    for ci_name in ci_names:
        index += index_ci_entry(ci_name)
    print('X'*60)
    print(index)
    print('X'*60)
    with open(source_dir + '/reference/index.rst', 'wt') as file:
        file.write(index)


def index_ci_entry(ci_name):
    title = " ".join(list(s.capitalize() for s in ci_name.split('_')))
    return "\n".join([
        "",
        ".. toctree::",
        "   :maxdepth: 1",
        f"   :caption: {title}:",
        "",
        f"   {ci_name}",
        "",
    ])