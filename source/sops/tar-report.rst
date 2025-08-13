Creating Targeted Sequencing (TAR) Reports
===============================================

a. TAR - Djerba INI configuration file assembly

First, set up the working directory as outlined in the following section: Setting up a Djerba working directory. 

The following information must be populated into the .ini file:

.. list-table:: Fields to fill in a TAR INI file
	:widths: 20 20 20 20 20
	:header-rows: 1

	* 	- Plugin
		- Parameter
		- Source
		- Description
		- Example
	*	- tar_input_params_helper
		- donor
		- Dimsum
		- LIMS ID comprising the study name and patient number
		- REVOLVE_0001
	* 	-
		- project
		- Dimsum
		- Name of the project in provenance
		- REVTAR
	* 	- 
		- study
		- Req system
		- Name of the study (acronym) in requisition system
		- Re-VOLVE
	*	-
		- oncotree_code
		- Req system
		- OncoTree code
		- HGSOC
	*	-
		- cbio_id
		- shesmu
		- (When not known, same as project)
		- REVOLVE
	*	-
		- patient_study_id
		- Req system
		- Patient study ID in requisition system
		- REV-01-001
	*	- 
		- tumour_id
		- Dimsum
		- ID of tumour sample
		- REV-01-001_Pl
	*	- 
		- normal_id
		- Dimsum
		- ID of blood sample
		- REV-01-001_BC
	*	-
		- primary_cancer
		- Req system
		- Name of primary cancer
		- High grade serous ovarian carcinoma
	*	- 
		- site_of_biopsy
		- Req system
		- Site of biopsy/surgery (usually cfDNA)
		- cfDNA
	*	-
		- sample_type
		- Req system
		- Sample type  (usually cfDNA)
		- cfDNA
	*	- 
		- known_variants
		- Req system
		- A known variant from previous genetic testing
		- TP53 p.(D158*)
	*	- 
		- requisition_approved
		- Req system
		- Date of first requisition approval by Tissue Portal staff in yyyy-mm-dd format
		- 2023-10-31
	*	-
		- requisition_id
		- Req system
		- Name of the requisition
		- REVWGTS-P-861
	*	-
		- assay
		- Req system
		- The assay used (targeted sequencing assay, value is “TAR”)
		- TAR
	*	- provenance_helper
		- sample_name_normal
		- Dimsum - Full Depth Sequencings
		- Default value is None
		- REVOLVE_0001_01_LB01-02
	*	- 
		- sample_name_tumour
		- Dimsum - Full Depth Sequencings
		- Default value is None
		- REVOLVE_0001_04_LB01-02
	*	- 
		- sample_name_aux
		- Dimsum - Full Depth Sequencings
		- Default value is None
		- REVOLVE_0001_04_LB01-01
	*	- tar.status
		- copy_number_ctdna_detected
		- Upon review of ichorCNA plot
		- Default value is False
		- False/True
	*	-
		- small_mutation_ctdna_detected
		- Upon review of the reported SNVs
		- Default value is False
		- False/True


a. Parameters from Dimsum
i. Login using your OICR username and LDAP at https://dimsum.gsi.oicr.on.ca/
ii. On the QC dashboard, scroll down to the case of interest, or go to filter -> donor -> type in the donor (ex. REVOLVE_0001).
iii. Click on the case to see case details


iv. Complete the relevant fields in the INI file according to the following table:

INI parameter
Header in Dimsum
donor
Donor, first link (ex. REVOLVE_0001)
project
Project, first link (ex. REVOLVE)
tumour_id
Test, Tumour TS (ex. REV-01-001_Pl)
normal_id
Test, Normal TS (ex. REV-01-001_BC)
sample_name_normal
Ly R under Full Depth Sequencings (ex. REVOLVE_0001_01_LB01-02)
sample_name_tumour
Pl T TS under Full Depth Sequencings (ex. REVOLVE_0001_04_LB01-02)
sample_name_aux
Pl T SW under Full Depth Sequencings (ex. REVOLVE_0001_04_LB01-01)

b. Parameters from the requisition system
i. Login using your OICR username and LDAP at https://requisition.genomics.oicr.on.ca/ 
ii. From the dashboard submissions tab, navigate to the project:


iii. Refer to the “External Names” in MISO to find the “Patient Study ID” within the requisition system, eg. REVOLVE_001 -> REV-TAR-329.
iv. Find the sample in the requisition system, click “View”, and scroll down to view information:


v. Complete the relevant fields in the INI file according to the following table:

INI parameter
Header in Req System
study
“Name of study (acronym)” under “Submission” tab
patient_study_id
“Patient study ID” under “Submission” tab
oncotree_code
“OncoTree code” under “Submission” tab
primary_cancer
“Primary cancer diagnosis” under “Submission” tab
requisition_approved
‘Submission approved” date under “Case History” tab
Requisition_id
Top of the requisition after “ID”
c. Example of a completed Djerba INI file

Spaces are acceptable in the parameter value and on either side of the = sign::

	[core]

	[tar_input_params_helper]
	donor=REVOLVE_0001
	project=REVTAR
	study=Re-VOLVE
	oncotree_code=HGSOC
	cbio_id=REVOLVE
	patient_study_id=REV-01-001
	tumour_id=REV-01-001_Pl
	normal_id=REV-01-001_BC
	primary_cancer=High grade serous ovarian carcinoma
	site_of_biopsy=cfDNA
	sample_type = cfDNA
	known_variants=<em>TP53</em> (p.D148*)
	requisition_approved=2023-05-09
	requisition_id = REVWGTS-P-861
	assay=TAR
	[provenance_helper]
	sample_name_normal = REVOLVE_0001_01_LB01-02
	sample_name_tumour = REVOLVE_0001_04_LB01-02
	sample_name_aux = REVOLVE_0001_04_LB01-01
	[report_title]
	[patient_info]
	[case_overview]
	[gene_information_merger]
	[treatment_options_merger]
	[summary]
	[tar.sample]
	[tar.snv_indel]
	[tar.swgs]
	[tar.status]
	copy_number_ctdna_detected = False
	small_mutation_ctdna_detected = False
	[supplement.body]

b. TAR - Report generation

i. Login and setup the analysis environment on a Univa compute node, as described in step 1.
ii. Run djerba.py in report mode to generate an HTML report. (See below for examples.)
iii. Output filename is of the form ${TUMOUR_ID}-v{VERSION_NUMBER}.html in the report directory, where $TUMOUR_ID is the tumour ID from Dimsum.
iv. Run the script using the INI file completed in step 2.2a; the ‘report’ subdirectory created in Step 1 for intermediate output; 
v. Examples:

Example report::
	$ djerba.py report -i config.ini -o report/ 

vi. Proceed to review and interpretation of the interim HTML output.

c. TAR - Interpreting the Interim Report
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This section is to be performed by CGI staff. Most results are reviewed in the interim report. Results reviewed by other means are explicitly mentioned in the text.

i. Review and confirm accuracy of non-PHI fields on interim report relative to current requisition in requisition portal in the case overview section.

ii. Information regarding the tumour will be listed in the “Sample Information” section:
iii. Review whizbam links for variants:

* All variant calls must be viewed to gauge whether they are confident and thus reportable or an artifact and thus must be removed.
* In general, if there are non-variant supporting reads in the normal, the variant is more likely to be an artifact. 

* Examples of variants to keep

Example 1:



According to data_mutations_extended_oncogenic.txt, this is a G -> T nonsense mutation. As this call has many supporting reads in the tumour but not in the normal, it is a confident call and should be kept for reporting.

Example 2:



According to data_mutations_extended_oncogenic.txt, this is a frame-shift insertion. A frame-shift insertion is represented by a short purple line. This insertion can be better seen when scrolling down:



As the frame-shift insertion has no supporting reads in the normal, it is likely a confident call and should be kept for reporting.


* Examples of variants to remove

Example 1:



Upon initial review, this looks like a A -> T SNP call, as this variant does not have supporting reads in the normal. However, according to data_mutations_extended_oncogenic.txt, this call is actually a frame-shift deletion. Indeed, when scrolling down, this frame-shift deletion is visible:



As this frame-shift deletion has supporting reads in the normal, it is likely to be an artifact and must be removed.

Example 2:



According to data_mutations_extended_oncogenic.txt, this call is actually a frame-shift insertion. A frame-shift insertion is represented by a short purple line (such as on the right of the above screenshot). As there are no short purple lines present in the tumour, this variant does not pass QC and must be removed. 


iv. Check provenance for the IchorCNA plots file: $(sample_name_aux)_plots.tar.gz. After extraction, examine the copy number solution in $(sample_name_aux)_genomeWide.pdf. If the tumour fraction is less than 10%, confirm that the plot is centered at 0. If the tumour fraction is greater than 10%, confirm that the plot is centered at 0 and determine if the high tumour fraction is being driven by potentially artifact chromosomal regions. The regions that correspond to recurrent artifacts commonly found in healthy controls (i.e. likely false positives) are: 1p, 10q, 17, 19, and 22.

▪ Example of a plot centered at 0 (it will appear blue):

▪ Example of a plot not centered at 0 (it will appear brown):

▪ Example of a high purity solution likely driven by potentially artifact chromosomal regions (ex. 1p, 17, 22):


▪ Example of a high purity solution which is likely correct:


▪ If it is determined that the high purity is likely driven by potentially artifact chromosomal regions, change the estimated tumour fraction to <10%. Copy number variants must be removed.

v. After reviewing both the copy number variants and the small mutations, the parameters in [tar.status] in the config.ini may need to be adjusted.
▪ [tar.status]

copy_number_ctdna_detected = False
small_mutation_ctdna_detected = False
Both parameters automatically default to False.


After reviewing the SNVs and purity/CNVs, adjust the parameters as follows:

* copy_number_ctdna_detected = True if the purity is ≥ 10%
* small_mutation_ctdna_detected = True if there are high confidence SNVs present 

Once done, re-generate the report to ensure changes to [tar.status] are rendered correctly::
	$ djerba.py report -i config.ini -o report/

For example, for a report with copy_number_ctdna_detected = True and 	 small_mutation_ctdna_detected = False, the output will be:



vi. Once the variants to remove have been identified, remove them from djerba_report.json. It is helpful to use json tool to make editing the json easier::

	$ cat djerba_report.json | python3 -m json.tool > report/djerba_report_machine.pretty.json
	$ vim report/djerba_report_machine.pretty.json
	$ djerba.py render -j report/djerba_report_machine.pretty.json -o report -p  

Note: For all follow-up cases, ensure that the status is consistent with the previous submission. If the case is positive—either due to a tumor fraction >10% or the presence of a reported SNV—be sure to double-check the original ichorCNA plot and confirm the variants reported in the initial submission.

It’s not uncommon for the follow-up report to show new variants or higher tumor fraction; this can occur if the original sample was below our limit of detection. In such cases, review the old data in IGV to see if any supporting reads were present, and examine the ichorCNA plot for amplifications that may align with the current findings. 

vii. If prior knowledge of previous sequencing results or biomarkers is known, review the relevant sections of the report to confirm and note abnormalities:

Abnormality
Potential Cause
Action
Lack of expected alteration, or presence of a mutation in a cancer type where the mutation is expected or not expected
* Lack of coverage for the expected mutation
* Sample swap
* Mutation is filtered
* Verify coverage for the region by inspecting the bam file in Whizbam
* Check for sample swaps
* Confirm mutation was not removed by pipeline by reviewing the MuTect2 VCF file
Prior sequencing results are not confirmed
* Low coverage for the expected mutation
* Sample swap
* Mutation is filtered
* Verify coverage for the region by inspecting the bam file in Whizbam
* Check for sample swaps
* Confirm mutation was not removed by pipeline by reviewing the MuTect2 VCF file

NOTE: If any discrepancy is noted, the sample should be marked as failed in Dimsum according to the QM-036 Quality Control Approval Procedure SOP. The report is to be regenerated with the FAIL flag as in section 2.2e.

viii. Review the Small Mutations (SNVs/INDELs) section of the report

▪ SNVs and INDELs are reported according to the following filtering criteria:

Filter
Threshold
Variant Allele Frequency (VAF)

* ≥ 1%

Supporting Alternate Reads

* ≥ 3 reads

OncoKB

* All level 1-4, R variants which pass the above criteria
* All “Oncogenic”, “Likely Oncogenic” and “Predicted Oncogenic” alterations which pass the above criteria

▪ Review all actionable and/or oncogenic mutations using Whizbam links for alignment artifacts. Whizbam links can be navigated to by clicking the link in the rightmost column in the data_mutations_extended_oncogenic.txt file in the patients report directory.  Alterations which are deemed artifacts are to be removed from the JSON file and recorded on the relevant JIRA ticket.

▪ Dinucleotide substitutions which are represented as two individual mutations are to be merged. Merged variants should be recorded in a new file named data_mutations_merged.txt. Copy both original individual annotations to this file, along with a third record of the final merged variant. To perform this merge, please follow this step-by-step procedure in the “Merging and Annotating Mutations Representing the Same Event” document on CGI:How-to wiki page.

ix. Generate an interpretation statement based on the findings from above. For samples flagged as follow-up, an additional statement is included to comment on the shared and/or exclusive variants relative to prior sequencing results. 

▪ Final statement is recorded in a TXT file named results_summary.txt
▪ Use the following template as an example:

Analysis Subsection
Example statement
Comparison to prior sequencing results (for follow-up samples only)
Comment on the number of shared and exclusive mutations relative to prior sequencing results. When newly reported variants are discovered, include OncoKB recommendations for any new indications:
“Relative to prior sequencing of [current sample X], [prior sample Y] shares 3 common variants and one variant is exclusive to, and has 1 additional oncogenic variant in gene A
SNV/Indel 
“Mutations analysis uncovered loss of function mutations in xxx genes that suggest xxx.”
Copy Number
“Copy Number analysis uncovered an amplification in xxx genes that suggest xxx.”
OncoKB treatment recommendations
Statements are taken from oncoKB:
“Alteration xxx is a Level 1 mutation which the following treatment recommendations according to oncoKB”

▪  For an example summary, please refer to our wiki page on writing a genome interpretive statement.

d. TAR - Draft Report
~~~~~~~~~~~~~~~~~~~~~~~~

This section is to be performed by CGI staff.
Regenerate the PDF report with the interpretation changes and summary text:

Edit results_summary.txt and then update the genomic summary text in the report JSON document as follows (note that input and output for the update_summary.py script may be the same file)::

	$ djerba.py update -s report/results_summary.txt -j report/report.json -o report/ -p

TAR - Updating QCs
The draft clinical report is accompanied by a QC report, which documents the QC audit trail for the sample in question. The report must be generated after MISO has been updated with informatics QC results. The sample QC section has one metric to be reviewed by CGI staff: the ichorCNA plot. Review the ichorCNA plot as detailed in the section “TAR - Interpreting the Interim Report” above.

1. If the sample passes QCs as detailed in the QM. Quality Control and Calibration Procedures, then under “QCs” for the case in MISO, enter PASS under the types “Informatics Review” and “Draft Clinical Report”

Once updated in Dimsum, the QC report may be generated using the “case report” button in Dimsum. Under “Assay”, click on the assay (ex. REVOLVE - cfDNA+BC). Then, at the top right of the page, click on the green “QC Report'' button. On the new page, in the top right, click on the green “Print” button to save to pdf for uploading to the requisition system. Investigate any warnings or errors in the QC report.

TAR - Example Djerba TAR session

The following is an example sequence of commands used to generate a clinical report with Djerba. It is intended as a guide to CGI staff for report generation. The commands are for illustration only, not a fixed script to be followed. The start of each command is prefixed with $, and comments are prefixed with #::

	$ ssh ugehn.hpc
	$ sudo -u svc.cgiprod -i
	$ qrsh -P gsi -l h_vmem=16G
	$ module load djerba
	$ cd WORK_DIR
	# make a folder with the donor name, ex. REVOLVE_0001
	$ mkdir REVOLVE_0001
	$ cd REVOLVE_0001
	# make a folder with the report directory, i.e. report/
	$ mkdir report
	# create a config.ini file
	$ djerba.py setup --assay ASSAY --ini {WORK_DIR}/config.ini --compact –p ../../../CHARM2PLAS_project.ini
	$ vim  {WORK_DIR}/config.ini
	# run djerba.py to generate a report
	$ djerba.py report -i config.ini -o report/
	# review the HTML
	# review whizbam links in data_mutations_extended_oncogenic.txt 
	# remove any false calls in djerba_report.json (use json.tool to make it easier)
	$ cat djerba_report.json | python3 -m json.tool > report/djerba_report_machine.pretty.json
	$ vim djerba_report_machine.pretty.json
	# edit results_summary.txt to write the genomic summary 
	$ vim report/results_summary.txt
	# update the ctDNA plugin status from "Not Detected” to “Detected” if needed
	# update the genomic summary
	$ djerba.py update -s report/results_summary.txt -j report/report.json -o report/ -p

e. TAR - Failed Report
~~~~~~~~~~~~~~~~~~~~~~

If the report fails any QC metrics or fails for another reason, a failed report must be submitted to the requisition system.

To generate a failed report for TAR, fill out the following ini (see section 2.2.a for ini parameters)::

	[core]

	[tar_input_params_helper]
	donor=
	project=
	study=
	cbio_id=
	oncotree_code=
	patient_study_id=
	tumour_id=
	normal_id=
	primary_cancer=
	site_of_biopsy=
	known_variants=
	requisition_id=
	requisition_approved=
	assay=

	[provenance_helper]
	sample_name_normal = None
	sample_name_tumour = None
	sample_name_aux = None

	[report_title]
	failed = True
	[patient_info]
	[case_overview]
	[summary]
	failed = True 
	summary_file = results_summary.txt
	[tar.sample]
	[supplement.header]
	[supplement.body]
	failed = True

Ensure that the reason for failure is clearly identified in the report summary.