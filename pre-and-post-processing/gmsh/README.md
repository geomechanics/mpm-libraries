# Gmsh
## Pre-Processing For 3D Tetrahedral Mesh
This folder contains sample gmsh input and conversion files, useful for
mpm pre-processing with tetrahedral elements, as described in the [MPM wiki](https://github.com/geomechanics/mpm/wiki/Gmsh).
Additional example files are provided for reference: to check that the process
can be correctly replicated.

**Steps:**
* Import the gmsh input file (herein [sample_gmsh_input_tetrahedron.geo](https://github.com/geomechanics/mpm-libraries/blob/main/pre-and-post-processing/gmsh/sample_gmsh_input_tetrahedron.geo)) to gmsh.
* Generate mesh and save as a .msh file. If using the gmsh GUI:
    * 'File' --> 'Open...' --> select the gmsh .geo input file
    * 'Modules' --> 'Mesh' --> '3D'
    * 'File' --> 'Save Mesh'
    * Note: an example file, [example_gmsh_output_tetrahedron.msh](https://github.com/geomechanics/mpm-libraries/blob/main/pre-and-post-processing/gmsh/example-files/example_gmsh_output_tetrahedron.msh), is provided for reference.
* Convert the .msh to a .csv file (all delimiters should be ',' for the .csv)
    * Note: an example file, [to_convert.csv](https://github.com/geomechanics/mpm-libraries/blob/main/pre-and-post-processing/gmsh/example-files/to_convert.csv), is provided for reference.
* Modify the inputs to the conversion program, [preproc_gmsh_converter.py](https://github.com/geomechanics/mpm-libraries/blob/main/pre-and-post-processing/gmsh/preproc_gmsh_converter.py), as needed:
    * The main user inputs are entered near the top of the file.
    * A section of additional user inputs (customizations) are available further
    down in the file, for additional flexibility.
    * Please see the file itself for descriptions and details on the inputs.
* Run the conversion program (uses Python).
* The following outputs may be generated:
    * MPM mesh input file: [mesh.txt](https://github.com/geomechanics/mpm-libraries/blob/main/pre-and-post-processing/gmsh/example-files/mesh.txt).
    * MPM velocity constraints input file: [velocity_constraints.txt](https://github.com/geomechanics/mpm-libraries/blob/main/pre-and-post-processing/gmsh/example-files/velocity_constraints.txt).
    * MPM entity sets input file: [entity_sets.json](https://github.com/geomechanics/mpm-libraries/blob/main/pre-and-post-processing/gmsh/example-files/entity_sets.json).
    * A folder with additional informational files (may be useful for additional
    pre-processing needs), specifically:
        * A .csv file with information on all elements (one per row), including
        surface (2D) and edge (1D) elements, with columns (in order):
            * Overall element ID (for 1D, 2D, and 3D elements)
            * Element type (1: 1D line, 2: 2D surface, 3: 3D volume)
            * Edge, surface, or volume tag, corresponding to those tags in the
            gmsh input file (note: surface tags are also defined in the
            conversion program)
            * Local location number (with respect to element type, corresponding
            to those in the gmsh input file)
            * Nodal IDs fir the element
        * A .csv file with information on all nodes, one per row (columns are
        node IDs followed by nodal coordinates).

**Notes on the sample files:**
* The files are set up to create tetrahedral mesh within a hexahedral
bounding box.
* The files are set up to create boundary conditions (BCs) for the surfaces of
the mesh bounding box only.