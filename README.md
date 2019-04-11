# Genome Sequence Informatics

The GSI team at [Ontario Institute for Cancer Research](https://oicr.on.ca) is a team of
bioinformaticians and software developers that develop, maintain, and operate the core 
analysis infrastructure, analyze genomic data produced at the institute, and support
collaborators and researchers with their bioinformatics analysis.

To support these activities, we have developed a large suite of open-source software
that can be found under our Github organizations: [oicr-gsi](https://github.com/oicr-gsi)
and [miso-lims](https://github.com/miso-lims).

## Laboratory tracking

To support our wetlab colleagues, we develop a variety of apps for laboratory tracking
that also play nicely with downstream computational tools.

* [MISO LIMS](https://github.com/miso-lims/miso-lims) : laboratory information management 
  system specifically for sequencing facilities.
* [RAMEN](https://github.com/miso-lims/ramen) : minimalist inventory control system for 
  sequencing facilities
* [Run Scanner](https://github.com/miso-lims/runscanner) : web server that monitors output 
  from sequencing instruments (Illumina, PacBio and Oxford Nanopore) and reports their 
  status and metrics
  
For more of our lab tracking software, visit the [miso-lims](https://github.com/miso-lims)
Github organisation.

## Pipeline

One of our main goals is to automate as much analysis, validation, and reporting as possible
and we've built a suite of APIs and software to help.

### General Purpose

* [server-utils](https://github.com/oicr-gsi/server-utils) : Java library for creating standard status pages for web servers without real UIs
* [drmaaws](https://github.com/oicr-gsi/drmaaws) : A webservice for interacting with DRMAA-based clusters
* [node-starter-kit](https://github.com/oicr-gsi/node-starter-kit) : Basic setup for a new Node project
* [queue_use](https://github.com/oicr-gsi/queue_use) : Calculate the usage and other stats for an SGE queue

### Analysis Infrastructure

* [Nabu](https://github.com/oicr-gsi/nabu): QC tracking for files via a web service
* [Shesmu](https://github.com/oicr-gsi/shesmu) : Decision-driven action launching system
* [Niassa](https://github.com/oicr-gsi/niassa) : Bioinformatics workflow engine and analysis provenance system
* [Guanyin](https://github.com/oicr-gsi/guanyin) : Reporting repository and report record keeping
* [Pinery](https://github.com/oicr-gsi/pinery) : A LIMS abstraction layer to provide generalized LIMS access via a web service.
* [Cerberus](https://github.com/oicr-gsi/cerberus) : Provenance API web service
* [Provenance](https://github.com/oicr-gsi/provenance) : A Java API for LIMS and analysis metadata
* [acquacotta-shiny-run-report](https://github.com/oicr-gsi/acquacotta-shiny-run-report) : Interactive and dynamic representation of SeqWare Run Reports

### Analysis Tools

* [Debarcer](https://github.com/oicr-gsi/debarcer) : Debarcer: A package for De-Barcoding and Error Correction of sequencing data containing molecular barcodes
* [bamqc](https://github.com/oicr-gsi/bamqc) : Perl scripts for generating quality control stats from BAM files
* [xenoclassify](https://github.com/oicr-gsi/xenoclassify) : Classifying short-read sequencing data from xenograft samples

# Contact us

Contact us either through the Github issue tracker on any project or in our [Gitter room](https://gitter.im/oicr-gsi/general).
