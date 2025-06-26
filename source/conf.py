# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'OICR Genome Sequence Informatics'
copyright = '2025, GSI'
author = 'GSI'

# -- Subprojects ------------------

intersphinx_mapping = {
    "reqsystem": ("https://oicr-gsi.readthedocs.io/projects/requisition-system/stable", None),
}
intersphinx_disabled_reftypes = ["*"]

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.intersphinx"]

templates_path = ['_templates']
exclude_patterns = []

rst_prolog = """
.. |wgts-version| replace:: 6.0
.. |tar-version| replace:: 6.0
.. |shallow-version| replace:: 3.0
.. |pwgs-version| replace:: 3.0
.. |hg38-version| replace:: hg38-p12
.. |hg38-ref-remote| replace:: https://hgdownload.cse.ucsc.edu/goldenpath/hg38/bigZips/p12/
.. |hg38-ref-local| replace:: /.mounts/labs/gsi/modulator/sw/data/hg38-p12/hg38_random.fa
.. |revolve-panel| replace:: https://bitbucket.oicr.on.ca/projects/GSI/repos/interval-files/browse/accredited/EVOLVE-CHARM.TS.hg38.bed
.. |callability-exome-intervals| replace:: https://bitbucket.oicr.on.ca/projects/GSI/repos/interval-files/browse/accredited/Agilent_SureSelect_v6.EX.hg38.alias
.. |wgs-intervals| replace:: / https://bitbucket.oicr.on.ca/projects/GSI/repos/interval-files/browse/accredited/ALL.AS%2CCH%2CCM%2CNN%2CPG%2CSW%2CWG.hg38.bed
"""


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_css_files = ["custom.css"]
numfig = True