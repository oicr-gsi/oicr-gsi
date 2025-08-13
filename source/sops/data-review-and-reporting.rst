Overview of Clinical Report Generation Procedure
#################################################

The report generation procedure involves trained CGI staff carrying out specific additional analysis and interpretation of variant calls and quality metrics output by the standardized bioinformatics pipelines. Either the CGI manager or an assigned member of CGI acts as a clinical reporting lead. Details on this role are outlined on the `wiki page`_. They are responsible for checking the status clinical reports on Dimsum_ and delegating. Interim clinical reports are generated using Djerba. CGI then generates a draft report by interpreting and editing the interim report for subsequent review and sign-out by a geneticist.

.. _wiki page: https://wiki.oicr.on.ca/display/GSI/Be+Clinical+Reporting+Lead
.. _Dimsum: https://dimsum.oicr.on.ca/?PIPELINE=Accredited+with+Clinical+Report&PENDING=Analysis+Review+-+Clinical+Report

In brief, the procedure follows these steps:

1. Set up a working directory to contain intermediate files
2. Create the report - these steps are Assay Specific

    a. Complete configure file with parameters specific to the assay. Non-PHI patient data (sample type, cancer type, anatomical location) from the requisition system is entered in the Djerba config file, and appears in the interim report.
    b. Generate an interim report. Using Djerba, convert the config file to html report
    c. Interpret interim report. 

        i. Review each section of the report to familiarize yourself with actionable and oncogenic variants
        ii. Write a `clinical interpretation statement`_ and insert into interim report

    d. Finalize draft report. Convert the html to the draft pdf
    e. Considerations for Failed reports are given at the end of each assay’s section

3. Review Draft Report meets ISO requirements
4. Download the quality control (QC) report using the case report button in the Dimsum system.
5. Upload the draft report and QC report to the Requisition System for review and sign-out by a Geneticist (see `Requisition and Reporting System Manual`_).
6. If a report is rejected by the Geneticist, it must be reviewed and resubmitted.

.. _clinical interpretation statement: https://wiki.oicr.on.ca/display/GSI/Write+a+Genome+Interpretive+Statement
.. _Requisition and Reporting System Manual: https://oicr-gsi.readthedocs.io/projects/requisition-system/stable

The steps in section 2 outline the procedure for each of the three assays supported by Djerba. There are individual sections for assay specific configuration and interpretation. Further, the step at which QC is evaluated and recorded in MISO changes among assays, as outlined in each respective procedure. 

    1. Whole Genome and Transcriptome Sequencing (WGTS)
    2. Targeted sequencing (TAR)
    3. plasma Whole Genome Sequencing (pWGS)

For considerations of variant classification, incidental findings and analytical methodology changes, see Additional Considerations at the end of this document.

**Example Terminology:**

1. Donor: refers to the MISO-generated patient identifier (eg. OCT_010118)
2. Requisition: a unique ID used to track the assay request for service. The requisition ID is the organizing unit of a case. It is identified through the requisition-system and each requisition will lead to one report. There may be multiple requisitions for one donor therefore we focus specifically on requisitions as the functional unit.
3. Project: refers to the project name as entered in the LIMS (eg. OCTCAP)
4. groupID: a unifying identifier for a group of libraries (or just one library) that will be analyzed as a unit. For example, top-ups will be grouped under one group-id. Similarly, several extractions from one tumour sample can be analyzed together under one group-id. Libraries with the same group-id are merged in the pipeline. DNA and RNA libraries use the same groupID (e.g. OCT-01-0118-TS) to define an analysis to be completed together. The groupID is an identifier used in MISO which indicates libraries that are to be processed together, thus resulting in a call-ready bam file. In other words, two samples derived from the same tissue with the same groupID will be merged into a single bam file. Often, the groupID is equivalent to the “Sample Study ID” from the sample requisition system as described in the TM. Sample Accessioning Procedure SOP.

In this SOP, the donor alias OCT_010118 or ${DONOR} will be used as an example to generate a WGTS, a TAR, and a pWGS report.  The example commands and filesystem paths will generalize to other samples and projects.

Creating Reports
##################

Before Starting
==================

Informatics pipelines must have completed as described in the :doc:`informatics-pipelines` SOP.

When informatics pipelines have completed, a Jira ticket will be created in the CGI Jira queue and assigned to a CGI staff member by the clinical reporting lead. This ticket is specific for CGI staff and indicates when all workflows for a requisition have completed. The ticket is meant to be a trigger for CGI staff to begin with this SOP, and contains the information needed to proceed with the procedure. If the clinical reporting lead is unavailable, delegation responsibility falls to the CGI Manager, then the Director, GSI. This begins the Data Review and Reporting Procedure.

.. _djerba-working-dir:

Setting up a Djerba working directory
========================================

Analysis is carried out on the Univa cluster as the svc.cgiprod user and all work is to be completed under the /.mounts/labs/CGI/cap-djerba/ base directory. Set up the analysis environment as follows:

# Log into a Univa cluster head node, with the CGI staff’s username. For more information on logging into the OICR vist OICR’s `HPC school`_ 
b. Switch to the svc.cgiprod user account using the sudo command: ``sudo -u svc.cgiprod -i`` followed by ``qrsh``, with appropriate options, to open a session on a compute node.
# Load Djerba_ and its prerequisites: ``module load djerba``. It is normal to see a few warning messages on module load. If in doubt as to whether it has run successfully, run ``echo $?`` immediately afterwards to check the return code, which should be 0 (zero).
# create a working directory in CGI space to contain intermediate files. The working directory will be contained within a base directory specific to the project, donor, and requisition.
# djerba.py requires a report directory. It may also have a separate scratch directory; otherwise, ancillary files will be written to the report directory. Make a directory called “report” inside the working directory.
# To generate an INI config file, use the ‘setup’ mode of djerba.py with the name of the appropriate assay (one of WGTS, WGS, TAR or PWGS). This will create a config file called ‘config.ini’. 


.. _HPC school: https://www.google.com/url?q=https://gitlab.oicr.on.ca/ResearchIT/hpc-school/-/blob/master/hpc-intro.md%23logging-onto-a-head-node&sa=D&source=docs&ust=1699549033261016&usg=AOvVaw0HETLo4tBLeyEO1HJ2hIHE
.. _Djerba: https://github.com/oicr-gsi/djerba

Use the ``--compact`` flag to generate an INI file with only the minimum required parameters. Other parameters may need to be modified, for example if report_version in the [core] section requires a value other than 1; in this case, the ``--compact`` flag may be omitted.

Use ``--pre-populate`` flag (or ``-p PATH``) to specify the path to an existing INI file specific to the project. Its key/value pairs will be merged into the newly generated config.ini, automatically filling in those parameters so you don’t have to enter them manually. If there’s no project INI file yet, just omit this flag.
Detailed information on completing the config file is found in the dedicated assay sections below::

	$ WORK_DIR=$BASE_DIR/$PROJECT/$DONOR/$REQUISITION
	$ mkdir ${WORK_DIR}/report
	$  djerba.py setup --assay $ASSAY --ini ${WORK_DIR}/config.ini --compact --pre-populate $BASE_DIR/$PROJECT/${project_name}-config.ini

	#example
	$WORK_DIR=/.mounts/labs/CGI/cap-djerba/PASS01/PANX_1234/PASS01UHN-000
	$PROJECT_DIR=/.mounts/labs/CGI/cap-djerba/PASS01
	$ mkdir ${WORK_DIR}/report
	$ djerba.py setup --assay $WGTS --ini ${WORK_DIR}/config.ini --compact --pre-populate ${PROJECT_DIR}/PASS01-config.ini

Once a working directory has been set up, a report must be generated according to the assay listed in the requisition. Currently, Djerba supports the generation of clinical reports for the following assays: WGTS, TAR, and PWGS.

The instructions for generating reports for each assay are documented below. An example command line session is included at the end of each section. 










.. toctree::
   :maxdepth: 2
