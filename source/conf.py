# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
import subprocess

# ---------------------------------------------------------------------------
# Per-assay configuration
#
# On Read the Docs, the assay is detected automatically from the project slug
# (READTHEDOCS_PROJECT env var, always set by RTD).  The RTD project slug must
# contain the assay name: e.g. "oicr-gsi-wgts", "oicr-tar", "pwgs-pipeline".
#
# For local per-assay builds, set ASSAY=wgts|tar|pwgs explicitly:
#   ASSAY=wgts sphinx-build source build/
#
# Leaving both unset builds the full main project.
# ---------------------------------------------------------------------------

_ASSAY = os.environ.get('ASSAY', '').lower()
if not _ASSAY:
    _rtd_project = os.environ.get('READTHEDOCS_PROJECT', '').lower()
    for _candidate in ('wgts', 'tar', 'pwgs'):
        if _candidate in _rtd_project:
            _ASSAY = _candidate
            break

_SHARED_RST_PROLOG = """
.. |hg38-version| replace:: hg38-p12
.. |hg38-ref-remote| replace:: `UCSC <https://hgdownload.cse.ucsc.edu/goldenpath/hg38/bigZips/p12/>`__
.. |hg38-ref-local| replace:: `Modulator </.mounts/labs/gsi/modulator/sw/data/hg38-p12/hg38_random.fa>`__
.. |wgs-intervals| replace:: `Interval-files <https://bitbucket.oicr.on.ca/projects/GSI/repos/interval-files/browse/accredited/ALL.AS%2CCH%2CCM%2CNN%2CPG%2CSW%2CWG.hg38.bed>`__
.. |revolve-panel-paper| replace:: `Paper <https://doi.org/10.1158/1078-0432.CCR-23-0797>`__
.. |revolve-panel-local| replace:: `Interval-files <https://bitbucket.oicr.on.ca/projects/GSI/repos/interval-files/browse/accredited/EVOLVE-CHARM.TS.hg38.bed>`__
.. |revolve-panel-remote| replace:: `Excel file <https://pmc.ncbi.nlm.nih.gov/articles/instance/10502468/bin/ccr-23-0797_supplementary_table_s3_suppts3.xlsx>`__
.. |callability-exome-local| replace:: `Interval-files <https://bitbucket.oicr.on.ca/projects/GSI/repos/interval-files/browse/accredited/Agilent_SureSelect_v6.EX.hg38.alias>`__
.. |callability-exome-remote| replace:: `UCSC <https://genome.ucsc.edu/cgi-bin/hgTables?db=hg38&hgta_group=map&hgta_track=exomeProbesets&hgta_table=Agilent_Human_Exon_V6_Regions&hgta_doSchema=describe+table+schema>`__
"""

if _ASSAY == 'wgts':
    project = 'OICR Genomics WGTS Pipeline'
    version = '6.0'
    release = '6.0'
    tags.add('wgts_build')
    # Toctrees inside inactive .. only:: blocks still get parsed by Sphinx;
    # suppress the resulting "reference to excluded document" warnings.
    suppress_warnings = ['toc.excluded']
    exclude_patterns = [
        'informatics-pipelines/assays.rst',
        'informatics-pipelines/tar.rst',
        'informatics-pipelines/pwgs.rst',
        'data-review-reporting/tar-report.rst',
        'data-review-reporting/plasma-report.rst',
        'ruo-pipelines/**',
        '_build/**',
        'venv/**',
    ]
    rst_prolog = _SHARED_RST_PROLOG + """
.. |wgts-version| replace:: 6.0
"""

elif _ASSAY == 'tar':
    project = 'OICR Genomics TAR Pipeline'
    version = '4.0'
    release = '4.0'
    tags.add('tar_build')
    suppress_warnings = ['toc.excluded']
    exclude_patterns = [
        'informatics-pipelines/assays.rst',
        'informatics-pipelines/wgts.rst',
        'informatics-pipelines/pwgs.rst',
        'data-review-reporting/wgts-report.rst',
        'data-review-reporting/plasma-report.rst',
        'ruo-pipelines/**',
        '_build/**',
        'venv/**',
    ]
    rst_prolog = _SHARED_RST_PROLOG + """
.. |tar-version| replace:: 4.0
"""

elif _ASSAY == 'pwgs':
    project = 'OICR Genomics pWGS Pipeline'
    version = '3.0'
    release = '3.0'
    tags.add('pwgs_build')
    suppress_warnings = ['toc.excluded']
    exclude_patterns = [
        'informatics-pipelines/assays.rst',
        'informatics-pipelines/wgts.rst',
        'informatics-pipelines/tar.rst',
        'data-review-reporting/wgts-report.rst',
        'data-review-reporting/tar-report.rst',
        'ruo-pipelines/**',
        '_build/**',
        'venv/**',
    ]
    rst_prolog = _SHARED_RST_PROLOG + """
.. |pwgs-version| replace:: 3.0
"""

else:
    # Main project — builds everything
    project = 'OICR Genome Sequence Informatics'
    version = '1.0'
    release = '1.0'
    exclude_patterns = [
        '_build/**',
        'venv/**',
    ]
    rst_prolog = _SHARED_RST_PROLOG + """
.. |wgts-version| replace:: 6.0
.. |tar-version| replace:: 4.0
.. |pwgs-version| replace:: 3.0
"""

copyright = '2025, Ontario Institute for Cancer Research'
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

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_css_files = ["custom.css"]
numfig = True


if tags.has('update-workflows'):
    try:
        script_to_run = os.path.join(os.path.dirname(__file__), 'update-workflows.py')

        print("Executing external script to fetch workflows...")

        # Use subprocess.run() to execute the script.
        result = subprocess.run(
            [sys.executable, script_to_run],
            capture_output=True,
            text=True,
            check=True
        )

        print("Script output:")
        print(result.stdout)

    except subprocess.CalledProcessError as e:
        print("Error calling script:")
        print(e.stderr)
        sys.exit("Critical script failed. Stopping build.")

    except FileNotFoundError:
        print(f"Error: The script {script_to_run} was not found.")
        sys.exit("Stopping build.")
else:
    print("Skipping data fetching script. To run it, build with the '-t update-workflows' flag.")
