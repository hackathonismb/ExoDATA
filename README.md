# Integration of externally computed DATA for visualization on structure and data analysis in a structural context 
Residue (and atom) level properties are calculated by numerous programs.  The goal is to be able to load in externally computed properties, but also experimental properties for visualization on structure, presentation and sharing, and for analysis, i.e. to compare, combine and correlate multiple properties computed by multiple programs, and open the door to deep and rich structure-properties analysis at various levels of detail.

# Requiements
* Import and view external annoation data in iCn3D
* View data as a track in the primary structure 
* View the data on 3D structures
* Data should be flexible with respect to data source
* Annotations need to be defined interms of structure

* Basic Annotation
** Amino acid residue number
** Data value 
** Description
* Data Value
** Vectors, arrays, hashes (key, value)
** Example: radii, gradients

# Simple model
Define a file format (perhaps JSON) and iCn3D parser to interconvert external data to iCn3D data
Later publish an API for database and other kinds of integration

## Questions
What are the easy wins? 
iCn3D has many capabilities for displaying data, what can we use now? That is have menu items call existing display types
Area concepts: Surface displays, wire frames, water
Chemical concepts: Display, colors ...

## Example data types
Motion ranges and envelops from molecular simulations / molecular dynamics
Annotations from chemical modification of exposed surfaces
