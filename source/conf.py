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
.. |hg38-ref-remote| replace:: `UCSC <https://hgdownload.cse.ucsc.edu/goldenpath/hg38/bigZips/p12/>`__
.. |hg38-ref-local| replace:: `Modulator </.mounts/labs/gsi/modulator/sw/data/hg38-p12/hg38_random.fa>`__
.. |revolve-panel-paper| replace:: `Paper <https://doi.org/10.1158/1078-0432.CCR-23-0797>`__
.. |revolve-panel-local| replace:: `Interval-files <https://bitbucket.oicr.on.ca/projects/GSI/repos/interval-files/browse/accredited/EVOLVE-CHARM.TS.hg38.bed>`__
.. |revolve-panel-remote| replace:: `Excel file <https://pmc.ncbi.nlm.nih.gov/articles/instance/10502468/bin/ccr-23-0797_supplementary_table_s3_suppts3.xlsx>`__
.. |callability-exome-local| replace:: `Interval-files <https://bitbucket.oicr.on.ca/projects/GSI/repos/interval-files/browse/accredited/Agilent_SureSelect_v6.EX.hg38.alias>`__
.. |callability-exome-remote| replace:: `UCSC <https://genome.ucsc.edu/cgi-bin/hgTables?db=hg38&hgta_group=map&hgta_track=exomeProbesets&hgta_table=Agilent_Human_Exon_V6_Regions&hgta_doSchema=describe+table+schema>`__
.. |wgs-intervals| replace:: `Interval-files <https://bitbucket.oicr.on.ca/projects/GSI/repos/interval-files/browse/accredited/ALL.AS%2CCH%2CCM%2CNN%2CPG%2CSW%2CWG.hg38.bed>`__
"""


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
        # It's a good practice to stop the build if a critical script fails.
        sys.exit("Critical script failed. Stopping build.")

    except FileNotFoundError:
        print(f"Error: The script {script_to_run} was not found.")
        sys.exit("Stopping build.")
else:
    print("Skipping data fetching script. To run it, build with the '-t update-workflows' flag.")

