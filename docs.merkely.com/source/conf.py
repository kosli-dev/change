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
from pathlib import Path

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
    reference_dir = os.path.dirname(__file__) + '/reference'
    ci_names = ['generic_docker', 'bitbucket_pipeline', 'github_actions']
    create_reference_rst_files(reference_dir, ci_names)
    create_reference_ci_rst_files(reference_dir, ci_names)
    create_reference_ci_dir(reference_dir, ci_names)
    app.add_css_file("merkely-custom.css")
    app.connect('env-get-outdated', env_get_outdated)


def create_reference_rst_files(reference_dir, ci_names):
    index = "\n".join([
        f".. This file was auto-generated from {__file__}",
        "",
    ])
    for ci_name in ci_names:
        index += index_ci_entry(ci_name)
    with open(f'{reference_dir}/index.rst', 'wt') as file:
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


def create_reference_ci_rst_files(reference_dir, ci_names):
    for ci_name in ci_names:
        title = " ".join(list(s.capitalize() for s in ci_name.split('_')))
        rst = "\n".join([
            title,
            "-" * len(title),
            "",
            ".. toctree::",
            "   :maxdepth: 1",
            "",
            f"   {ci_name}/index"
        ])
        with open(f'{reference_dir}/{ci_name}.rst', 'wt') as file:
            file.write(rst)


def create_reference_ci_dir(reference_dir, ci_names):
    for ci_name in ci_names:
        dir = f"{reference_dir}/{ci_name}"
        Path(dir).mkdir(exist_ok=True)
        index = "\n".join([
            ".. toctree::",
            "   :maxdepth: 1",
            "",
            "   declare_pipeline",
            "   log_approval",
            "   log_artifact",
            "   log_deployment",
            "   log_evidence",
            "   log_test",
            "   control_deployment",
        ])
        with open(f'{reference_dir}/{ci_name}/index.rst', 'wt') as file:
            file.write(index)

        create_reference_ci_command(reference_dir, ci_name, 'declare_pipeline')
        create_reference_ci_command(reference_dir, ci_name, 'log_approval')
        create_reference_ci_command(reference_dir, ci_name, 'log_artifact')
        create_reference_ci_command(reference_dir, ci_name, 'log_deployment')
        create_reference_ci_command(reference_dir, ci_name, 'log_evidence')
        create_reference_ci_command(reference_dir, ci_name, 'log_test')
        create_reference_ci_command(reference_dir, ci_name, 'control_deployment')


def create_reference_ci_command(reference_dir, ci_name, command_name):
    title = " ".join(list(s.capitalize() for s in command_name.split('_')))
    if ci_name == 'generic_docker':
        short_ci_name = 'docker'
    elif ci_name == 'bitbucket_pipeline':
        short_ci_name = 'bitbucket'
    elif ci_name == 'github_actions':
        short_ci_name = 'github'
    rst = "\n".join([
        "",
        f"{title}",
        "=" * len(title),
        f".. describe_command:: {command_name} summary {short_ci_name}",
        "",
        "Invocation",
        "----------",
        f".. describe_command:: {command_name} invocation_full {short_ci_name}",
        "",
        "Parameters",
        "----------",
        f".. describe_command:: {command_name} parameters {short_ci_name}",
        "",
    ])
    with open(f'{reference_dir}/{ci_name}/{command_name}.rst', 'wt') as file:
        file.write(rst)

