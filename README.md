GSI is a team of bioinformaticians, software developers, and clinical genome interpreters
 at [Ontario Institute for Cancer Research](https://oicr.on.ca) 
that develop, maintain, and operate the core 
analysis infrastructure, analyze genomic data produced at the institute, and support
collaborators, researchers, and clinical trials with their bioinformatics analysis.

To support these activities, we have developed a large suite of open-source software
that can be found under our Github organizations: [oicr-gsi](https://github.com/oicr-gsi)
and [miso-lims](https://github.com/miso-lims).

This repository is for some of the public documentation related to our clinical offerings.

# Installing the documentation

These docs are built with Python 3 and Sphinx. It's best to install and run within a python virtual environment.

To install:
```
python3 -m pip install -r requirements.txt
```

To build:
```
make html
```

Open the local copy of the website at `build/html/index.html`


# Updating documentation

Documentation is written in reStructuredText. Here's a [primer](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html).


# Update the workflows for an assay

There's a python script that will automatically update the assay specific `.csv` files in [source/sops/software](source/sops/software) according to the `.txt` files that are in the same directory.

1. Modify the list of workflows for the assay at [source/sops/software](source/sops/software).
2. Run `make update`.
  * This command will download gsi_workflows.json from OICR, which is produced by https://github.com/oicr-gsi/workflowTracker/blob/main/workflow_tracker.py. You need to be on the VPN and have SSH keys set up for this to work.
  * if you have a passphrase on your ssh key, it will ask you for it
  * it will then use the list of workflows for each assay, pull out the appropriate clinical workflow information, and stick it in a csv file in source/sops/software
3. Commit the txt and generated csv files.

You can then use the csv in RST using the `.. csv-table::` command.

# Deploy documentation to ReadTheDocs

Documentation pushed to the `main` branch is automatically built on RtD.

* Project page on RtD : https://app.readthedocs.org/projects/oicr-gsi/
* Latest documentation : https://oicr-gsi.readthedocs.io/en/latest/


# Contact us

Contact us either through the Github issue tracker on any project.



