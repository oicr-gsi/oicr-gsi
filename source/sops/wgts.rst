#############################################################
Whole Genome and Transcriptome (WGTS) version |wgts-version|
#############################################################

Whole Genome
-------------
.. _wgs-pipeline:

.. figure:: images/wgs-pipeline.png
	
	**Whole Genome Sequencing Analysis Pipeline.**

1.	The whole genome pipeline commences once the bcl2fastq workflow is completed and FASTQ files are available (not shown). 
2.	FASTQ files are quality controlled using FastQC. FastQC produces quality control metrics related to reads (e.g. total numbers of reads).
3.	FASTQ files are aligned with BwaMem to generate an unprocessed lane-level BAM file. 
4.	Cases are quality controlled with the - bamQCworkflow generating a JSON file of lane-level alignment QC metrics for review. The quality control metrics include the insert size distribution, amount of duplication, mapping percentage, and other WG ‘Single Lane’ metrics described in QM. Quality Control and Calibration Procedures.  Genomic fingerprints are generated from lane-level alignments and made available to sample authentication procedures.
5.	Cases are quality controlled again with bamQC running on the merged set of all lane-level alignments generating a JSON file of call-ready alignment QC metrics for review. In addition to the lane-level QC metrics this includes an assessment of the per-sample depth of coverage (QM. Quality Control and Calibration Procedures).
6.	All lane-level BAM files are collected and processed via BamMergePreProcessing, which merges and sorts lane-level BAMs, as well as performing  duplicate marking, and base quality score recalibration to generate a call-ready sample-level BAM..
7.	These normal and tumour BAM files are used as input for the variant calling workflows.

	a.	MuTect2 generates SNV and INDEL mutation calls in vcf format, which are annotated by VariantEffectPredictor, generating a MAF file of annotated calls.
	b.	GRIDSS and Delly generate somatic structural alterations in VCF format. The Delly vcf is post-processed by MAVIS to generate calls in TSV format, in addition to graphical representations of the structural event in SVG format. 
	c.	The GRIDSS vcf is post-processed by Purple and used for evidence to support copy number calls, loss of heterozygosity status, and estimate tumour purity.
	d.	msisensor calls the proportion of microsatellite sites with evidence of variants between T-N to produce a microsatellite score recorded in a .TXT file.
	e.	HRDetect calls the homologous recombination deficiency (HRD) status using the Mutect2 vcf file, and the GRIDSS vcf file as input. The output file is a json file containing the HRD results.
	f.	T1K reports germline HLA typing alleles by estimating allele abundances from input read alignments. The output is a TSV file that includes the identified HLA alleles, their abundance, quality, and any secondary alleles.

8.	All alteration files are provided to Djerba to generate a provisional clinical report for review by genome interpreters.


WGS Workflows and Software
^^^^^^^^^^^^^^^^^^^^^^^^^^

More information about the analysis pipelines is available in the ‘Procedure’ section below. Workflow parameterization is automated through the linked Shesmu configuration. This repository is restricted to authorized individuals.

* Human Genome Reference: |hg38-version|
	* Source: |hg38-ref-remote|
	* Local fasta: |hg38-ref-local|



.. csv-table:: Whole Genome Sequencing Software
   :file: software/wgs.csv
   :widths: 30, 30, 30, 30, 30
   :header-rows: 1


Whole Transcriptome
--------------------

.. _wts-pipeline:

.. figure:: images/wts-pipeline.png

	**Whole Transcriptome Sequencing Analysis Pipeline.**


1.	As with the WGS informatics pipeline, the whole transcriptome pipeline commences once FASTQ files are generated from bcl2fastq. 
2.	FASTQ files are aligned with the STAR workflow, generating genome-aligned and transcriptome-aligned BAM files. STAR also outputs a TSV file of chimeric junctions which is used as input for the STAR-Fusion workflow. 
3.	The FASTQ files are also provided to RNASeqQc which generates a JSON file of QC metrics for plotting via Dashi. The quality control metrics include the WT ‘Single Lane’ metrics described in QM. Quality Control and Calibration Procedures. Genomic fingerprints are generated from lane-level alignments and made available to sample authentication procedures.
4.	The transcriptome-aligned BAM file is provided as input to RSEM, generating FPKM values and normalized expression counts in tabular format. 
5.	RNA fusion calls are generated from STAR-Fusion and Aribba.  Both are used as input to to MAVIS for validation and annotation.
6.	All alteration files are provided to Djerba to generate a provisional clinical report for review by genome interpreters.


TS Workflows and Software
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

More information about the analysis pipelines is available in the ‘Procedure’ section below.  Workflow parameterization is automated through the linked Shesmu configuration. This repository is restricted to authorized individuals.

.. csv-table:: Whole Transcriptome Sequencing Software
   :file: software/wts.csv
   :widths: 30, 30, 30, 30, 30
   :header-rows: 1

