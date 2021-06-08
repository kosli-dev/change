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
sys.path.append(os.path.abspath("/app/source/docs"))
extensions = [
    'describe_command',
    'describe_fingerprint',
    'sphinx_copybutton'
]

# import sphinx_bootstrap_theme

# -- Project information -----------------------------------------------------

project = 'Merkely'
copyright = '2021, Merkely'
author = 'Merkely'

html_logo = "_static/images/w-merkely-docs-white.svg"

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
html_theme = 'pydata_sphinx_theme'

html_theme_options = {
    'globaltoc_collapse': True,
    'navbar_center': ['back_to_site'],
    'navbar_end': ['search-field'],
    "collapse_navigation": True,
    "show_prev_next": False,
    "page_sidebar_items": [],
    "search_bar_text": "Search…",
    "footer_items": [],
    "favicons": [
        {
            "rel": "icon",
            "href": "/images/favicon.png",
        }
    ]
}

html_sidebars = {
    '**': ["global_toc"],
    'index': []
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_css_files = [
    'merkely-custom.css',
    'merkely-pygments.css',
]
html_js_files = [
    'merkely-custom.js',
]

html_extra_path = ['CNAME', '.nojekyll']

highlight_language = 'yaml'

# This is a hack to get around a sphinx bug that does not
# copy static files correctly on change
# see https://github.com/sphinx-doc/sphinx/issues/2090
def env_get_outdated(app, env, added, changed, removed):
    return ['index']


from docs import create_data, doc_rst, doc_txt, doc_ref


def setup(app):
    # Auto generate Command reference rst files.
    doc_ref.curl_ref_files()
    data = create_data()
    doc_txt.create_txt_files(data)
    doc_rst.create_rst_files()
    app.connect('env-get-outdated', env_get_outdated)


