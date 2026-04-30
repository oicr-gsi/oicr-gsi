Targeted Sequencing (TAR) Reports
===============================================

.. _retrieve-pregenerated-djerba-reports:

First, set up the working directory and analysis environment

#. Login and set up the analysis environment on a Univa compute node, as described in step 1.
#. Identify the case you want to review by querying the latest Vidarr report index:

   .. code-block:: bash

      zgrep djerbaReportGenerator /scratch2/groups/gsi/staging/vidarr/vidarr_files_report_latest.tsv.gz \
      | grep CHARM2_caseID \
      | cut -f1,2,47,23,31,14

#. Locate the corresponding ``.gz`` archive for the correct requisition.
#. Copy the correct file into your usual working directory.
#. Extract the archive:

   .. code-block:: bash

      tar -xvzf reqID-v1.tar.gz

#. Navigate into the extracted folder:

   .. code-block:: bash

      cd reqID-v1

   This directory contains all Djerba-generated files required for review and report generation.

#. Proceed to review and interpretation of the interim HTML report.

.. note::

   The ``vidarr-u20-djerbaReportGenerator.shesmu`` olive automatically generates these reports. There is no longer a need to manually create or configure the config.ini from scratch.


--------------------------------------------

.. _retrieve-pregenerated-djerba-reports:

Interim Report Review And Modifications
~~~~~~~~~~~~~~~~~~~~~~~~~~

Until API integration is available to automate this step, these values must be manually updated in the reqID-v1_report.json file.
This information is usually obtained from the Requisition (Req) system.

* :ref:`navigate-reqsys`

.. list-table:: Fields to fill tar_input_params_helper section
   :widths: 20 20 20 20
   :header-rows: 1

   * - Parameter
     - Source
     - Description
     - Example

   * - ``study``
     - Req system, “Name of study (acronym)” under “Submission” tab
     - Requisition system study identifier
     - Re-VOLVE

   * - ``known_variants``
     - Req system
     - Known variant from previous genetic testing
     - TP53 p.(D158*)

   * - ``requisition_approved``
     - Req system, “Submission approved” date under “Case History” tab
     - Date of first requisition approval in yyyy-mm-dd format
     - 2023-10-31

It's also necessary to update the ``Author`` field from **"Analysis Author"** to your name.

.. note::

   Until the olive is updated, the following two fields must be temporarily modified manually:

   * ``site_of_biopsy`` should be set to ``cfDNA`` (not ``N/A``)
   * ``sample_type`` should be set to ``cfDNA`` (not ``N/A``)



Interpreting the TAR Report
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#. Review case information in the “Case Overview” section.

#. Review tumour information in the “Sample Information” section.

#. Review Whizbam links for variants:

   * All variant calls must be inspected to determine whether they are true positives or artefacts.
   * Variants supported by non-variant reads in the normal sample are more likely to be artefacts.
   * Examples: :ref:`tar-whizbam-examples`

#. Examine copy number solution in:

   ``report/$(sample_name_aux)_genomeWide.pdf``

   * If tumour fraction < 10%, confirm plot is centred at 0.
   * If tumour fraction > 10%, assess whether apparent elevation is driven by artefactual chromosomal regions.
   * Common artefact regions: 1p, 10q, 17, 19, 22.

   * Examples: :ref:`tar-ichor-examples`

   * If high purity is driven by artefactual regions, set tumour fraction to <10% and remove copy number variants.

#. After reviewing copy number and small mutations:

   Update the following fields as needed:

   * ``copy_number_ctdna_detected``
   * ``small_mutation_ctdna_detected``
   * ``any_ctdna_detected``

   **Defaults:**
   * False / “ctDNA not detected”
   * “Not Detected”

   **If evidence supports detection:**
   * True / “ctDNA detected”
   * “Detected”

   Example configuration:

   .. code-block:: json

      {
        "plugins": {
          "tar.status": {
            "results": {
              "copy_number_ctdna_detected": "ctDNA detected",
              "small_mutation_ctdna_detected": "ctDNA not detected",
              "any_ctdna_detected": "Detected"
            }
          }
        },
        "config": {
          "tar.status": {
            "copy_number_ctdna_detected": "True",
            "small_mutation_ctdna_detected": "False"
          }
        }
      }

   .. image:: images/tar-status2.png

#. Once the variants to remove have been identified, remove them from ``reqID-v1_report.json``. :ref:`json-tips`

	.. note:: 
			For all follow-up cases, ensure that the status is consistent with the previous submission. If the case is positive; either due to a tumor fraction >10% or the presence of a reported SNV; be sure to double-check the original ichorCNA plot and confirm the variants reported in the initial submission.

			It is not uncommon for the follow-up report to show new variants or higher tumor fraction; this can occur if the original sample was below our limit of detection. In such cases, review the old data in IGV to see if any supporting reads were present, and examine the ichorCNA plot for amplifications that may align with the current findings. 

#. If prior knowledge of previous sequencing results or biomarkers is known, review the relevant sections of the report to confirm and note abnormalities.
	
	* If any discrepancy is noted, the sample should be marked as failed in Dimsum according to the QM-036 Quality Control Approval Procedure SOP and a :ref:`tar-failed-report` should be generated.

	.. list-table:: Possible abnormalities
		:widths: 30 30 40
		:header-rows: 1

		*	- Abnormality
			- Potential Cause
			- Action
		* 	- Lack of expected alteration, or presence of a mutation in a cancer type where the mutation is expected or not expected
			- * Lack of coverage for the expected mutation
			  * Sample swap
			  * Mutation is filtered
			- * Verify coverage for the region by inspecting the bam file in Whizbam
			  * Check for sample swaps
			  * Confirm mutation was not removed by pipeline by reviewing the MuTect2 VCF file
		*	- Prior sequencing results are not confirmed
			- * Low coverage for the expected mutation
			  * Sample swap
			  * Mutation is filtered
			- * Verify coverage for the region by inspecting the bam file in Whizbam
			  * Check for sample swaps
			  * Confirm mutation was not removed by pipeline by reviewing the MuTect2 VCF file


#. Review the Small Mutations (SNVs/INDELs) section of the report. SNVs and INDELs are reported according to the following filtering criteria:

	.. list-table:: SNV/InDels filter criteria
		:widths: 50 50
		:header-rows: 1

		* 	- Filter
			- Threshold
		*	- Variant Allele Frequency (VAF)
		 	- ≥ 1%
		*	- Supporting Alternate Reads
			- ≥ 3 reads
		*	- OncoKB
			- * All level 1-4, R variants which pass the above criteria
			  * All “Oncogenic”, “Likely Oncogenic” and “Predicted Oncogenic” alterations which pass the above criteria

	* Review all actionable and/or oncogenic mutations using Whizbam links for alignment artifacts. Whizbam links can be navigated to by clicking the link in the rightmost column in the ``data_mutations_extended_oncogenic.txt`` file in the patient's ``report`` directory.  Alterations which are deemed artifacts are to be removed from the JSON file and recorded on the relevant JIRA ticket.
	* Dinucleotide substitutions which are represented as two individual mutations are to be merged. Merged variants should be recorded in a new file named ``data_mutations_merged.txt``. Copy both original individual annotations to this file, along with a third record of the final merged variant. To perform this merge, please follow this step-by-step procedure in the `Merging and Annotating Mutations Representing the Same Event🔒`_ document on CGI:How-to wiki page.

.. _Merging and Annotating Mutations Representing the Same Event🔒 : https://wiki.oicr.on.ca/spaces/GSI/pages/293634774/Merging+and+Annotating+Mutations+Representing+the+Same+Event

#. Generate an interpretation statement based on the findings from above and record it in a TXT file named ``results_summary.txt``

	* For samples flagged as follow-up, include an additional statement to comment on the shared and/or exclusive variants relative to prior sequencing results. 
	* For an example summary, please refer to our wiki page on writing a `genome interpretive statement🔒`_.
	* Use the following template as an example:

	.. list-table:: Writing a TAR interpretation statement
		:widths: 50 50
		:header-rows: 1

		*	- Analysis Subsection
			- Example statement
		*	- Comparison to prior sequencing results (for follow-up samples only)
			- Comment on the number of shared and exclusive mutations relative to prior sequencing results. When newly reported variants are discovered, include OncoKB recommendations for any new indications:
			  “Relative to prior sequencing of [current sample X], [prior sample Y] shares 3 common variants and one variant is exclusive to, and has 1 additional oncogenic variant in gene A
		* 	- SNV/Indel 
			- “Mutations analysis uncovered loss of function mutations in xxx genes that suggest xxx.”
		*	- Copy Number
			- “Copy Number analysis uncovered an amplification in xxx genes that suggest xxx.”
		*	- OncoKB treatment recommendations
			- Statements are taken from oncoKB:
			  “Alteration xxx is a Level 1 mutation which the following treatment recommendations according to oncoKB”

.. _genome interpretive statement🔒 : https://wiki.oicr.on.ca/display/GSI/Write+a+Genome+Interpretive+Statement

Updating QCs
~~~~~~~~~~~~~~~~~~~

The only QC for CGI to complete is to `review the ichorCNA plot`_, which was done above.

Sign off on the "Informatics Review" in Dimsum according to the QM-036. Quality Control Approval Procedure.


Draft Report
~~~~~~~~~~~~~~~~~~~~~~~~

Regenerate the PDF report with the interpretation changes and summary text:

* Update the genomic summary text in the report JSON document as follows (note that input and output for the ``update_summary.py`` script may be the same file)::

      $ djerba.py update -s report/results_summary.txt -j report/reqID-v1_report.json -o report/ -p


* Alternatively, all changes made to ``reqID-v1_report.json`` can be made to ``reqID-v1_report.updated.json``, including updates to ``results_summary.txt``, by inserting the desired text under the following JSON field:

::

    "results": {
        "summary_text": ""
    }

Then run:

::

    $ djerba.py render -j report/reqID-v1_report.updated.json -o report/ -p
Continue to :ref:`Review the Draft Report` ➡️
**********************************************



Example Djerba TAR session
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following is an example sequence of commands used to generate a clinical report with Djerba. It is intended as a guide to CGI staff for report generation. The commands are for illustration only, not a fixed script to be followed. The start of each command is prefixed with $, and comments are prefixed with #::

	$ ssh ugehn.hpc
	$ sudo -u svc.cgiprod -i
	$ qrsh -P gsi -l h_vmem=16G
	$ module load djerba
	$ cd WORK_DIR

	# make a folder structure with the donor name/requisition ID/report
	$ mkdir -p REVOLVE_0001/REV-01/report
	$ cd REVOLVE_0001/REV-01

	# Fetch the pre-genrated Djerba report
	$ zgrep djerbaReportGenerator /scratch2/groups/gsi/staging/vidarr/vidarr_files_report_latest.tsv.gz | grep REVOLVE_0001

	# Copy the correct .tar.gz into working directory and extract
	$ tar -xvzf REV-01.tar.gz

	# review the HTML

	# Pretty-print JSON for review (choose one command or use your IDE to make it easier)
	$ cat REV-01-v1_report.json | python3 -m json.tool > report/REV-01-v1_report.pretty.json
	$ jq . REV-01-v1_report.json > REV-01-v1_report.pretty.json

	# Edit JSON ("study", "requisition_approved", "known_variants", "author" etc.)
	$ vim REV-01-v1_report.pretty.json

	# Review whizbam links in data_mutations_extended_oncogenic.txt
	# Remove any false calls in REV-01-v1_report.pretty.json

	# Edit results_summary.txt to write the genomic summary
	$ vim report/results_summary.txt

	# Update the ctDNA plugin status from "Not Detected” to “Detected” if needed

	# Update the genomic summary
	$ djerba.py update -s report/results_summary.txt -j report/REV-01-v1_report.pretty.json -o report/ -p


+----------------+----------------------+
| **Change Log** | `Github commit log`_ |
+----------------+----------------------+

.. _Github commit log : https://github.com/oicr-gsi/oicr-gsi/commits/main/source/data-review-reporting/tar-report.rst

