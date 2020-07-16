![ExoDATA](/ExoData%20logo.png)

# ExoDATA: Integration of externally computed DATA for visualization on structure and data analysis in a structural context 
### Team: Giulia Babbi, Raul Cachau, Matthew Sinnott, Todd Smith, Francesco Tabaro

# Motivation
In DNA and proteins, residue (and atom) level properties are calculated by numerous programs. From sequence variation to chemical modifications to volumetric data to electon densities to simulation and molecular dynamics calucations, there are many kinds of data that, when visualized in the context of three dimensional (3D) molecular structures, can provide insights to develop new knowlege. Presently, iCn3D displays structures from data in PDB or MMDB files and supports a wide variety of annotation modes. It's accompaning 1D sequence views can display annotations from other databases, but external data cannot be added in a flexible mannor. 

The goal of this project is to develop capabilities in iCn3D that will give individuals the ability to import externally computed residue (and atom) annotations (properties) data from other sources and experiments. Once imported these data can be visualized and shared as structure annotations for additional analyses. In one example an individual should be able to compare, combine and correlate multiple properties computed by multiple programs, to open the door to deep and rich structure-properties analysis at various levels of detail. In other words, for a given structure, can we visualize a state of knowledge in a new conext? 

# Examples - Use Cases
The following examples illustrate some of the data of interest.

## Covalent Labelling Mass Spectrometry (CLMS)
CLMS uses a chemical modification to label residues which are on the protein surface, this information is usefulwhen modelling monomeric structures (Sinnott et al., 2020) as this can inform on which parts of a protein areexposed vs which are buried. It is also useful when looking at complexes especially for trying to define excludedareas which are liely to be interface regions (Schmidt et al., 2017).

### Data Structure
aa1|c1
aa2|c2
aa3|c3

Data are structured as shown above in a text file, where aa indicates the residue id and c indicates the chain id foreach modified residue.

## Hydrogen Deuterium Exchange (HDX)
By measuring the rate of exchange of hydrogen and deuterium (using NMR or Mass Spec) over a protein onecan identify residues which are more protected (i.e. buried) than others. This allows it to inform on residueaccessibility and dynamics (Wales and Engen, 2006). There are two main variants of this experiment: foldingand stability.
* Folding: The protons of the backbone amide of amino acid residues exchange with protons of thesolvent (water) at neutral or acidic pH. If these amide protons are in residues that are part of the foldingnuclei of proteins, they become protected from solvent at a very early stage during the folding processand stop exchanging. These 'protection rates' of amide protons can be detected by a range of methodsthat follow their solvent exchange from the completely unfolded state throughout the entire foldingcourse: for example pulsed labelling, quenched flow and competition-based HDX measurements(coupled with either NMR or MS) as well as oxidative labelling experiments provide invaluableinformation on the folding mechanisms of proteins.
* Stability: On the other hand, the native exchange experiments investigate proteins in their folded orpartially folded states and report on the stability of existing hydrogen bonds to the amide protons basedon their resistance to solvent exchange. By varying the environmental conditions, like pH or denaturantconcentrations, such measurements can also provide quantitative information on the protection levelsof the individual amide protons in function of changes in the conformation of the protein. Comparingthese values can distinguish more stable from less stable regions of the protein fold

### Data Structure
aa1; type1; marker1
aa2; type2; marker2
aa3; type3; marker3

Data are structured as above, aa indicates a residue identifier, type refers to the residue type. The marker is theindication of protection of that residue. For folding experiments this marker will be EARLY, INTERMEDIATEor LATE, for stability experiments this will be STRONG, MEDIUM or WEAK

## Discrete Optimised Protein Energy (DOPE) Score
DOPE, or Discrete Optimized Protein Energy  (Shen and Sali, 2006), is a statistical potential used to assesshomology   models   in   protein   structure   prediction.   DOPE   is   based   on   an   improved   reference   state   thatcorresponds to noninteracting atoms in a homogeneous sphere with the radius dependent on a sample nativestructure; it thus accounts for the finite and spherical shape of the native structures.

### Calculation
DOPE scores are calculated using MODELLER9.24.

## Epitope from the Immune Epitope Database (IEDB)
From http://www.iedb.org "The Immune Epitope Database (IEDB) is a freely available resource funded by NIAID. It catalogs experimental data on antibody and T cell epitopes studied in humans, non-human primates, and other animal species in the context of infectious disease, allergy, autoimmunity and transplantation. The IEDB also hosts tools to assist in the prediction and analysis of epitopes." As of July 5, 2020 the database holds information on 738,235 peptidic, 2,980 non-peptidic epitopes, over a million T Cell, B Cell and MHC ligand assays, 3,939 source organisms, and 829 restricting MHC Alleles from 21,290 references. In this rich resource, epitopes from proteins with known structures (~4500) are linked to the relevant PDB files and can be displayed in 2D "response frequency" maps. 

In addition to the database of curated information, IEDB provides several epitope prediction tools for both T cell receptors and B cell receptors. In most cases data (epitopes) returned by theses tools are displayed in tables and 2D represtentations. For predictions with known structures, IEDB does provide a 3D viewing capability with jmol. 

### Data Structure
Varied due the program used. All produce information of an aa range and sequence and distinguish linear from discontinuous epitopes.

## Other Examples
DSN6 files

# Requiements
* Import and view external annoation data in iCn3D
* View data as a track in the primary (1D) structure 
* View the data on a 3D structure
* The data should be flexible with respect to data source and complexity

* Basic Annotation
   * Amino acid residue number
   * Data value 
   * Description
* Data Value
   * Vectors, arrays, hashes (key, value)
   * Example: radii, gradients

# Approach
Define a file format (perhaps JSON) and iCn3D parser to interconvert external data to iCn3D data
Later publish an API for database and other kinds of integration such as Jupyter notebooks
Survey ISMB attendees for more examples 

## Questions
What are the easy wins? 
iCn3D has many capabilities for displaying data, what can we use now? That is have menu items call existing display types
Area concepts: Surface displays, wire frames, water
Chemical concepts: Display, colors ...

## ISMB Survey
To better understand the kinds of data that individuals might want to see in the context of a 3D structure, we conducted a survey at the 2020 annual international conference on Intelligent Systems for Molecular Biology (ISMB). Three questions were asked:
1. What kind data would you like to see on a 3D structure?
1. How do you work with the data in question one? (file, program output, database, website (server))
1. What is the name of the program or resource in question 2?

As of July 16, 2020 ten responses were received. The responses fell into two general categories: Genomics data integration and structure modeling. Genomics intergation focused on the ablity to see DNA and protrein (translated) sequence variation overlayed directly, or be visible through "hovering," on structures. One individual sugested that it would be interesting to see coloring codes for the numbers of mutations at a site (hot spots) or the kinds of mutation (severity: benign, uncertain, pathogenic). Other kinds of genomic integration included the ability to visualize structures and their data in the context of reference genomes and (or) codons. 

Structure modeling interests included the ability to see chemical and other properties for atoms and residues. These could be chemical modification, changes to pH, and other properties. Modeling visulaization included ways to understand model certaintity (uncertainty and data quality), volumetric data (hydradation, electron density), and "motions." Domain and side chain flexiblity and vibration modes are examples of modeling motion properties. Source of motion data indclude NMR (nuclear magnetic resonance), molecular dynamics, and simulations. 

The second survey question asked for data source and provided four options: file, program output, dataabase, or website (server). The most common data source was a flat file. Files can get generated from programs or databases (> 50%). Other datasources were indicated as well and supporting these with an API (application programming interface) allows for direct integration with iCn3D. For example, because iCn3D can be implemented as a widget in a web page it is possibile for a genomic or structure database web site to directly integrate and visualize data on a structure within that site. 

![Survey files](/survey.jpg)

A large number of programs and specific resources were indicated. Genomics integration included GATK, VCF files, and dbSNP. Modeling programs included GROMACS, visual molecular dynamics (VMD), propka, and cpptraj.

# References
1. Schmidt, C., Macpherson, J.A., Lau, A.M., Tan, K.W., Fraternali, F., and Politis, A. (2017). Surface Accessibility and Dynamics of Macromolecular Assemblies Probed by Covalent Labeling Mass Spectrometry and Integrative Modeling. Anal. Chem. 89, 1459–1468.
1. Shen, M., and Sali, A. (2006). Statistical potential for assessment and prediction of protein structures. Protein Sci. 15, 2507–2524.
1. Sinnott, M., Malhotra, S., Madhusudhan, M.S., Thalassinos, K., and Topf, M. (2020). Combining Information from Crosslinks and Monolinks in the Modeling of Protein Structure ()
1. Wales, T.E., and Engen, J.R. (2006). Hydrogen exchange mass spectrometry for the analysis of protein dynamics. Mass Spectrom. Rev. 25, 158–170.

