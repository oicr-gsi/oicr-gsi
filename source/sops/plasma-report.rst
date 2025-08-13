2.3. Creating plasma Whole Genome Sequencing (pWGS) Reports
==============================================================

a. PWGS - INI assembly
------------------------

To create a pWGS report, we run Djerba with two pWGS plugins enabled: 
pwgs.sample performs sample identification and QC checks, 
pwgs.analysis performs analysis of mrdetect workflow outputs 

The pwgs plugins require the following information to be populated into the .ini file:

Plugin
Parameter
Source
Description
Example
Core
author
bambooHR
Your name
Rosalind Franklin

pwgs_cardea_helper
requisition_id
Dimsum
The id of the requisition
PWGVAL_011418_Ct
pwgs.
case_overview
primary_cancer
requisition
system
Primary cancer as specified in the requisition system
Pancreatic Adenocarcinoma

wgs_report_id
requisition
system
The ID of the associated WG(T)S report
OCT-01-1328_Ut_P-v2

requisition approved
requisition
system
date of approval for the requisition
2023/10/10
pwgs_provenance_helper
No input parameters required
pwgs.sample
No input parameters required
pwgs.summary
No input parameters required
pwgs.analysis
No input parameters required
supplement.header

supplement.body
assay
Dimsum
assay short name
PWGS

b. PWGS - Interim Report

The Djerba report html can be created with the command:

$ djerba.py report --ini config.ini --out-dir report 

The report html will be of the name ${group_id)_report.clinical.html

c. PWGS - Interpretation

The sample QC section has three metrics to be reviewed by CGI staff: median insert size, mean genome-wide coverage and primary SNVs, as shown in screenshot below:



Coverage
Mean deduplicate coverage should be ≥30X (40X target). Mean deduplicated coverage is automatically pulled into Djerba from QC-ETL. Samples under 30X deduplicated should be topped up by TGL. 

Primary SNVs
The plasma whole genome sequencing assay assumes the WGS or WGTS (40X or 80X) assay has been completed (hereafter, this family of assays are referred to collectively as ‘WGS’). The WGS report must be completed and the Djerba working directory be accessible on the cluster. Assay calibration showed a minimum requirement of 4,000 candidate SNVs in WGS report for reliable and replicable results; the pWGS assay should not be run when the primary tumour has less than 4,000 SNVs as per the current validation report. Assay requisitioners have been informed of this requirement and that number is included in WGS reports; cases where the 4,000 SNV threshold is not met will be failed (see 2.3e). Additionally, cases will also be failed if tumor purity is below the 30% threshold, even if the SNV count exceeds 4,000.

Median Insert Size
We set an upper limit to the median insert size (see QM-24: Quality Control and Calibration for cutoff value). cfDNA samples have a distinct insert size distribution that can be used to distinguish them from either normal (buffy coat) or primary tumour tissue samples with DNA fragmented by sonication. Median insert size can therefore be used to detect a swap between (for example) cfDNA and buffy coat. Libraries where the median insert size is higher than the threshold should most commonly be failed, however, if the median insert size value for a case is just slightly above the threshold, the insert size distribution can be visualized to confirm how much higher the median is than 167 bp and the sample rescued manually. Insert size distribution can be found in insert_size_distribution.svg and the figure below is to be used to guide decisions:

PASS
FAIL


The distribution is very narrow and centered at 167 bp with a second very low peak at 334 (167 x 2).
The distribution is wide, centered near 250 bp and has some fragments larger than 500 bp.


d. PWGS - Draft Report

If the report passes all QC metrics and all information is present, the report is converted from html to pdf, either using manually or using Djerba:

$ djerba.py render --json report/${group_id)report.json --out-dir report --pdf

e. PWGS - Failed Report
A failed report may be generated for this assay if:
1. The distribution of insert sizes does not follow those outlined in section c., and/or
2. The number of candidate SNVs is below 4000
3. The WGTS report failed 
The failed report is generated according to the same procedure as a TAR failed report (see 2.2e).

remove [pwgs.analysis]
add [failed_report]
primary_cancer = Undetermined
assay = PWGS
study=PWGVAL

[report_title]
failed=True

3. Reviewing the Draft Report

Review and confirm accuracy of non-PHI fields on draft report relative to current requisition in the Requisition System. Updates to a requisition may occur at any time prior to case sign out. 

As listed in ISO 15189 (sections 7.4.1.6 and 7.4.1.7), clinical reports contain the following information:

ISO Requirement
Report Location
Unique patient identification
Footer, on each page of the report
The date of the issue of the report

Unique identification that all its components are recognized as a portion of a complete report and a clear identification of the end (e.g. page number to total number of pages).

Identification of the laboratory issuing the report
Header
Name or other unique identifier of the user [i.e. requisitioner]
Case Overview
Any specific information necessary to describe the sample (e.g. source, site of specimen, macroscopic description)

Clear, unambiguous identification of the examinations performed

Type of primary sample
Sample Information
Sample quality and suitability that can compromise the clinical value of examination results

Indications of any critical results
Treatment Options
Identification of the examination method used
Supplementary
Identification of the CGI Staff reviewing the results and authorizing the release of the report
Report Sign-offs
The draft clinical genomic report is then uploaded to the Requisition System as defined in the QM. Requisition and Reporting System Manual - Uploading a Draft Clinical Report (Laboratory). CGI Staff will mark the draft report as ‘Pass’ or ‘Fail’ in MISO according to the QM. Quality Control and Calibration Procedures SOP.

4. QC Report Generation

The draft clinical report is accompanied by a QC report, which documents the QC audit trail for the sample in question. The report must be generated after MISO has been updated with informatics QC results.

The QC report may be generated using the “case report” button in Dimsum. Under “Assay”, click on the assay (eg. WGTS - 80XT/30XN). Then, at the top right of the page, click on the green “QC Report'' button. On the new page, in the top right, click on the green “Print” button to save to pdf for uploading to the requisition system. Investigate any warnings or errors in the QC report.

5. Uploading to the Requisition System

This section is to be performed by CGI Staff. The final step is to download the completed PDF report to a local machine, and then upload to the requisition system.
1. Upload the Djerba report document and the QC report document from Dimsum to the requisition system, as described in the QM. Requisition and Reporting System Manual - Uploading a Draft Clinical Report (Laboratory).
a. If needed, the Djerba PDF can be copied from the cluster to a directory on the CGI staff’s local machine. For example:
scp user@chickenwire.oicr.on.ca:/path/to/clinical_report.pdf 
If files are downloaded, immediately delete the copies of clinical and QC reports on the CGI staff’s local machine. This improves the security of the reporting process. In particular, it is intended to prevent a CGI staff from uploading a report for the wrong sample to the requisition system.
2. After all files are uploaded to the requisition system, CGI Staff will mark the Draft Report as ‘pass’ or ‘fail’ in Dimsum, according to the QM-036 Quality Control Approval Procedure SOP. This will signal to the Medical Director that the Report is ready for their review.

6. Revising a Draft Report (Rejection by Geneticist) 

In the event that an uploaded report is rejected by the geneticist, CGI staff will receive an e-mail notification from the requisition system indicating that the report has been rejected, with general comments for the reason for rejection.

CGI staff will review the comments and, if necessary, repeat the above procedure to produce a new report with an incremented version (using the version parameter in the [core] section of the INI).

7. Issuing an Amended Report 

A report that has been signed-out but that requires revision of metrics, interpretation, patient information, or other content edits must go through a re-accessioning process before it can be amended and reported. When amendments are necessary, the following steps must be followed, led by the CGI manager:

1. Contact the requisitioner 
a. The requisitioner’s email can be found at the top of the requisition.
b. Briefly describe the reason for amendment (ex. callability change, purity change, addition or removal of variant, PHI change, etc.)
c. Request that the requisitioner rescind the requisition 
d. Example email: 
Hi,
I’m [NAME], a member of the Clinical Genome Interpretation (CGI) team in OICR Genomics. Earlier, you submitted the following tumour sample requisition for the [PROJECT] project: [REQUISITION_ID], [DATE OF SUBMISSION]. After some discussion, we discovered [REASON FOR AMENDMENT]. 
We request that you re-open the submission so we can issue an amended report for this sample.
Thanks,
[NAME]
2. Once you receive confirmation that the requistioner has rescinded the requisition, contact a Tissue Portal (TP) member by Slack or email to re-approve the requisition.
a. When the requisition is rescinded by the requisitioner, the CGI team will no longer be able to view it in the requisition system until it can be approved by TP. 
b. Contact the TP member via Slack or email with the requisition number for them to re-approve and provide the reason for amendment.
c. When the requisition is approved, it will again become visible to the CGI team on the requisition system as “Submission Approved” 
3. Generate an amended report
a. Amended reports have:
i. A table at the top detailing the revisions. Example:

ii. Red “R#” markers to indicate where in the report the revisions occurred. Example:

iii.  A record of all the sign outs for each amendment. Example:

iv. An incremented version number (original report is ${Requisition_ID}-v1, first amended report is ${Requisition_ID}-v2, second amended report is ${Requisition_ID}-v3, etc). Example:

b. Generate the new report using Djerba, being sure to specify the report ID with the incremented version number in the [core] section of the config.ini file:
[core]
report_id = ${Requisition_ID}-v2

c. To add features 3a i-iii, the clinical report HTML (${Requisition_ID}-v2_report.clinical.html) will have to be manually edited. Use the following HTML code to make a table (greyed out code will help guide the placement of the table in the HTML)::

	<h1>Clinical Research Report</h1>
	<span DJERBA_COMPONENT_END='report_title' />

	<table width=100% style="text-align:left; margin-left: auto; margin-right: auto;">
	<thead><tr>
	<th width="12%">Revision Date</th>
	<th width="13%" >Revision Marker</th>
	<th width="75%">Revision Comments</th>
	</tr></thead>
	<tbody>
	<tr style="background-color: #f2f2f2;"">
	<td >2024-10-17</td>
	<td ><strong style="color:red;">R1</strong></td>
	<td >Correction to Estimated Cancer Cell Content in Sample Information</em></td>
	</tr>
	<tr style="background-color: #f2f2f2;"">
	<td >2024-10-17</td>
	<td ><strong style="color:red;">R2</strong></td>
	<td >Removal of MN1 from Shallow Whole Genome Sequencing</em></td>
	</tr>
	</table>

	<span DJERBA_COMPONENT_START='patient_info' />

d. Add the revision markers next to the relevant sections.
i. <sup><strong style="color:red;">R1</strong></sup></a>
ii. Example::

	<tr>
	<td>Sample Type:</td>
	<td>cfDNA</td>
	<td>Estimated Cancer Cell Content (%):</td>
	<td>&lt;10.0%<sup><strong style="color:red;">R1</strong></sup></a></td>
	</tr>

iii. Change the revision marker (R1, R2, R3, etc.) as needed.
e. Add the amended sign offs.
i. Example::

	<tr>
	<td width="33%">Report drafted by CGI Member  on 2024-09-26</td>
	</tr>
	<tr>
	<td width="33%">Report electronically signed out by PLACEHOLDER (ABMS #XXXXXXX) on yyyy-mm-dd</td>
	</tr>
	<tr>
	<td width="33%">Amended report drafted by CGI Member on 2024-10-17</td>
	</tr>
	<tr>
	<td width="33%">Amended report electronically signed out by PLACEHOLDER (ABMS #XXXXXXX) on yyyy-mm-dd</td>
	</tr>
	<tr>

4. The normal Djerba rendering method will not function. Instead use a standalone PDF converter, such as the script html_to_pdf.py from the djerba_prototypes repository. The PDF produced must have the standard Djerba page footer, including the report ID and the current date.
5. To upload the amended report, go to the requisition, click edit, and upload the newly generated amended report. Make sure the version number is incremented. 
6.  Inform the geneticist through Slack or email that the report has been submitted. They will not receive automatic notification. 

Additional Considerations
Variant Classification
1. Human sequence variants are reported using HGVS nomenclature and include the HUGO Gene Nomenclature Committee (HGNC) gene name, and a standard versioned reference identifier to a corresponding transcript and protein. The variant chromosomal position is also reported.
2. OICR Genomics’ reports cover all cancer genes as defined by OncoKB (https://www.oncokb.org/cancerGenes). The OncoKB cancer gene list is a collation of cancer associated genes according to multiple sources including: MSK-IMPACT trial, Foundation One CDx panel, Vogelstien et al., 2013, and the Tier 1 Cancer Gene Census gene list. Variant classification follows OncoKB AMP/ASCO/CAP Consensus Recommendation.
3. OICR also annotates the report using NCCN. The NCCN Compendium is a manually compiled list of somatic alterations for reporting in specific cancers. For Plasma Cell Myeloma (PCM) cases, we report t(4;14), t(14;16), t(11;14), and t(14;20). For ovarian cancer (OVARY), we report Homologous Recombination Deficiency (HRD).
4. Variant interpretation inputs to CGI reporting will be updated to keep pace with major releases. When variants have been reclassified, our interpretation and report will be based upon the latest version. New reports will contain the most current variant classification available at the time of drafting the report. We will not issue updates to previously signed-out reports.
5. The lab maintains a record of identified variants and associated interpretations for each patient in a structured file system. In addition to the maintenance of patient reports, all data used in the generation and interpretation of each report is retained. This includes all annotated variants which have been reviewed by genome CGI staff. 

Incidental Findings
As only OncoKB level 1-4, Oncogenic and Likely Oncogenic variants, R (resistance), and NCCN-prognostic variants are reviewed, and the results of this review are presented in the clinical genomic report, incidental findings are not examined or reported.

Analytical Methodology Changes
1. Analytical methodology changes will follow the processes laid out in QM. Continuous Improvement Plan and QM. Computer System Maintenance.
2. Unless a new requisition is submitted, OICR Genomics will not issue new updates to previously signed-out clinical genomic reports. 
3. If OICR Genomics changes its analytical methodology to correct major errors or oversights that significantly impact the final genomic report, that information will be communicated to both previous and current clients. Affected clients will be emailed to inform them of the change and any effect this may have on their existing or future genomic reports.

