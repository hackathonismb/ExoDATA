![ExoDATA](/ExoData%20logo.png)

# ExoDATA: Integration of externally computed DATA for visualization on structure and data analysis in a structural context 
### Team: Giulia Babbi, Raul Cachau, Matthew Sinnott, Todd Smith, Francesco Tabaro

# Motivation
In DNA and proteins, residue (and atom) level properties are calculated by numerous programs. From chemical modifications to simulation and molecural dynamics calucations thier are many kinds of data, that when visualized in the context of three dimensional (3D) molecular structures can provide insights to develop new knowlege. Presently, iCn3D displays structures from data in PDB or MMDB files. It's accompaning 1D sequence views can display annotations from other databases, but external data cannot be added in a flexible mannor. 

The goal of this project is to develop capabilities in iCn3D to be able to import externally computed residue (and atom) annotation (properties) from other sources and experiments and visualize and share those annotations with structures and for additional analysis. In one example an individual should be able to compare, combine and correlate multiple properties computed by multiple programs, to open the door to deep and rich structure-properties analysis at various levels of detail.

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

# Discrete Optimised Protein Energy (DOPE) Score
DOPE, or Discrete Optimized Protein Energy  (Shen and Sali, 2006), is a statistical potential used to assesshomology   models   in   protein   structure   prediction.   DOPE   is   based   on   an   improved   reference   state   thatcorresponds to noninteracting atoms in a homogeneous sphere with the radius dependent on a sample nativestructure; it thus accounts for the finite and spherical shape of the native structures.

## Calculation
DOPE scores are calculated using MODELLER9.24.


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

## Questions
What are the easy wins? 
iCn3D has many capabilities for displaying data, what can we use now? That is have menu items call existing display types
Area concepts: Surface displays, wire frames, water
Chemical concepts: Display, colors ...

## Example data types
Motion ranges and envelops from molecular simulations / molecular dynamics
Annotations from chemical modification of exposed surfaces
Volumetric data
Elecron density data
DSN6 files

## ISMB Survey
Goal: To learn what attendees would like to see, in terms, of visualizing data in the context of 3D structures. 
Preamble: ISMB attendees we ned your help. We are participating in hackathon to improve iCn3D. One of the poject is to [view external data](https://github.com/hackathonismb/Integration-of-externally-computed-DATA-for-visualization-and-analysis-on-structure) such as chemical modifications, molecualr dynamics information, and quality information as annotations on 3D molecular structures. To help up we have a very short survey we'd like you to take a less than one minute survey. 

### Questions: 
* What data would you like to see layered on a 3D structural model?
* Where do you get that data? Source type (files, program output, databases, servers), name?

# References
Schmidt, C., Macpherson, J.A., Lau, A.M., Tan, K.W., Fraternali, F., and Politis, A. (2017). Surface Accessibility and Dynamics of Macromolecular Assemblies Probed by Covalent Labeling Mass Spectrometry and Integrative Modeling. Anal. Chem. 89, 1459–1468.
Shen, M., and Sali, A. (2006). Statistical potential for assessment and prediction of protein structures. Protein Sci. 15, 2507–2524.
Sinnott, M., Malhotra, S., Madhusudhan, M.S., Thalassinos, K., and Topf, M. (2020). Combining Information from Crosslinks and Monolinks in the Modeling of Protein Str

