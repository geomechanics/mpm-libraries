// INPUTS
lc = 1.0; //characteristic length
Xmin = 0;
Xmax = 20;
Ymin = -5;
Ymax = 5;
Zmin = -10;
Zmax = 10;

// 8 corner points of a cube
Point(1) = {Xmin, Ymin, Zmin, lc};
Point(2) = {Xmax, Ymin, Zmin, lc};
Point(3) = {Xmax, Ymax, Zmin, lc};
Point(4) = {Xmin, Ymax, Zmin, lc};
Point(5) = {Xmin, Ymin, Zmax, lc};
Point(6) = {Xmax, Ymin, Zmax, lc};
Point(7) = {Xmax, Ymax, Zmax, lc};
Point(8) = {Xmin, Ymax, Zmax, lc};

Line(1) = {1,2} ;
Line(2) = {2,3} ;
Line(3) = {3,4} ;
Line(4) = {4,1} ;
Line(5) = {1,5} ;
Line(6) = {2,6} ;
Line(7) = {3,7} ;
Line(8) = {4,8} ;
Line(9) = {5,6} ;
Line(10) = {6,7} ;
Line(11) = {7,8} ;
Line(12) = {8,5} ;

Line Loop(1) = {1,2,3,4};
Line Loop(2) = {1,6,-9,-5};
Line Loop(3) = {2,7,-10,-6};
Line Loop(4) = {3,8,-11,-7};
Line Loop(5) = {-4,8,12,-5};
Line Loop(6) = {9,10,11,12};

Plane Surface(1) = {1};
Plane Surface(2) = {2};
Plane Surface(3) = {3};
Plane Surface(4) = {4};
Plane Surface(5) = {5};
Plane Surface(6) = {6};

Surface Loop(1) = {1,2,3,4,5,6};
Volume(1) = {1};

// Line elements (1D) tagged 1-12
Line_YminZmin = 101;
Physical Line("Line_YminZmin") = 1; //1
Line_XmaxZmin = 102;
Physical Line("Line_XmaxZmin") = 2; //2
Line_YmaxZmin = 103;
Physical Line("Line_YmaxZmin") = 3; //3
Line_XminZmin = 104;
Physical Line("Line_XminZmin") = 4; //4
Line_XminYmin = 105;
Physical Line("Line_XminYmin") = 5; //5
Line_XmaxYmin = 106;
Physical Line("Line_XmaxYmin") = 6; //6
Line_XmaxYmax = 107;
Physical Line("Line_XmaxYmax") = 7; //7
Line_XminYmax = 108;
Physical Line("Line_XminYmax") = 8; //8
Line_YminZmax = 109;
Physical Line("Line_YminZmax") = 9; //9
Line_XmaxZmax = 110;
Physical Line("Line_XmaxZmax") = 10; //10
Line_YmaxZmax = 111;
Physical Line("Line_YmaxZmax") = 11; //11
Line_XminZmax = 112;
Physical Line("Line_XminZmax") = 12; //12

// Surface elements (2D) tagged 13-18
Surface_Zmin = 1001;
Physical Surface("Surface_Zmin") = {1} ; //13
Surface_Ymin = 1002;
Physical Surface("Surface_Ymin") = {2} ; //14
Surface_Xmax = 1003;
Physical Surface("Surface_Xmax") = {3} ; //15
Surface_Ymax = 1004;
Physical Surface("Surface_Ymax") = {4} ; //16
Surface_Xmin = 1005;
Physical Surface("Surface_Xmin") = {5} ; //17
Surface_Zmax = 1006;
Physical Surface("Surface_Zmax") = {6} ; //18

// Volume elements (3D) tagged 19
Volume_XYZ = 10001;
Physical Volume("Volume_XYZ") = {1} ; //19

// 2D mesh algorithm (1=MeshAdapt, 2=Automatic, 5=Delaunay, 6=Frontal,
// 7=bamg, 8=delquad)
Mesh.Algorithm = 5; //5 for unstructured tetrahedrons

// Apply recombination algorithm to all surfaces, ignoring per-surface
// spec Default value: '0'
Mesh.RecombineAll = 0;

// Mesh recombination algorithm (0=standard, 1=blossom)
Mesh.RecombinationAlgorithm = 0;

// Remeshing algorithm (0=no split, 1=automatic, 2=automatic)
// Mesh.RemeshAlgorithm = 1;

// Version
Mesh.MshFileVersion = 2.2; //2.2 for output format close to CB-Geo input files

// Remeshing using discrete parametrization (0=harmonic_circle,
// 1=conformal_spectral, 2=rbf, 3=harmonic_plane, 4=convex_circle,
// 5=convex_plane, 6=harmonic square, 7=conformal_fe
// Mesh.RemeshParametrization = 1;

// Number of smoothing steps applied to the final mesh
Mesh.Smoothing = 25;

// Don't extend the elements sizes from the boundary inside the domain (0)
// Mesh.CharacteristicLengthExtendFromBoundary = 0;

// NOTES
// The simplest construction in Gmsh's scripting language is the 'affectation', lc.
// This variable can then be used in the definition of Gmsh's simplest
// `elementary entity', a `Point'. A Point is defined by a list of
// four numbers: three coordinates (X, Y and Z), and a characteristic
// length (lc) that sets the target element size at the point.

// Source: Zhenxiang Su
