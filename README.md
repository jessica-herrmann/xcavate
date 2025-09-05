# About

X-CAVATE is an algorithm for converting vascular network geometries into collision-free 3D printer toolhead pathways.

X-CAVATE accepts an input list of coordinates (in cm) specifying the b-splines constituting a vascular network. It reorders the coordinates such that they can be printed, from start to finish, to fabricate the network without collisions between the printhead nozzle and deposited ink.

# Getting Started

## Input Files

### Custom Files

X-CAVATE contains multiple input file types to assist with integration into the user's specific printer hardware and software.

These files are contained within the "inputs/custom" folder, and must be updated with the user's specific code prior to running x-cavate.

| File | Description |
| ----------- | ----------- |
| header_code.txt | Custom g-code for header |
| start_extrusion_code.txt | Custom g-code for starting extrusion (single material) |
| stop_extrusion_code.txt | Custom g-code for stopping extrusion (single material) |
| start_extrusion_printhead1.txt | Custom g-code for starting extrusion of printhead 1 (multimaterial) |
| start_extrusion_axis1.txt | Custom g-code for starting extrusion of axis 1 (multimaterial) |
| stop_extrusion_printhead1.txt | Custom g-code for stopping extrusion of printhead 1 (multimaterial) |
| stop_extrusion_printhead1.txt | Custom g-code for stopping extrusion of printhead 1 (multimaterial) |
| dwell_start.txt | Custom g-code for dwelling at the start of a print pass |
| dwell_end.txt | Custom g-code for dwelling at the end of a print pass |
| active_pressure_printhead1.txt | Custom g-code for setting the pressure for extrusion when printhead 1 is the active nozzle |
| active_pressure_printhead1.txt | Custom g-code for setting the pressure for extrusion when printhead 2 is the active nozzle |
| rest_pressure_printhead1.txt | Custom g-code for setting the resting pressure for extrusion when printhead 1 is the resting nozzle |
| rest_pressure_printhead2.txt | Custom g-code for setting the resting pressure for extrusion when printhead 2 is the resting nozzle |



## Required Format

To print with specified filament radii, add the radius to each coordinate within the fourth column of the VascularNetwork.txt file ONLY (not the inlet/outlet file), as shown below.

To print with two inks ("arterial" and "venous"), specify the ink for each coordinate in the fifth column of the VascularNetwork.txt file ONLY (not the inlet/outlet file).

Use 0 to specify "venous" and use any other number (not 0) to specify "arterial."

## Constraints

The inlet/outlet coordinates MUST:
1. Also appear as coordinates within the vascular network .txt file
2. Exactly match the way they appear (i.e., same number of digits displayed after the decimal place) in the VascularNetwork.txt file

Bifurcation points ("branchpoints") MUST:
1. Exist ON the line from which they branch

To avoid long runtimes, it is highly recommended to limit the number of coordinates per vessel within the input VascularNetwork.txt file to no more than 100 coordinates/vessel.

# Required Parameters

## Nozzle Dimensions

Provide the nozzle outer diameter (mm). X-CAVATE will assume an infinite length for the nozzle, meaning that it will only account for collisions with the nozzle itself, rather than with the printhead holding the syringe.

Nordson provides a list of nozzle dimensions here: https://www.nordson.com/en/products/efd-products/general-purpose-dispense-tips

## Multi-material (Arterial and Venous)

To generate g-code for a network which distinguishes between arterial and venous vessels, turn on the "multimaterial" option by specifying "1" for the --multimaterial option in the command line. To turn off the multimaterial feature, specify "0" in the command line.

## Custom G-code

Users must specify at the command line whether they are including custom g-code for adaptation to their own printer hardware/software.

# Optional Parameters

## Gap Closure

X-CAVATE has two features for optimizing closure of gaps which may emerge at print pass junctions:

**1. Nodal Overlap**
Using the `--numOverlap` feature, users can optionally specify a number of nodes by which to overlap the end of a print pass with the previously-printed pass to which it connects. If there are fewer than the specified number of nodes in the existing pass, x-cavate will retrace the entire existing pass.

**2. Segment Extension**
Using the `pass_to_extend` .txt file, users can specify which print passes to extend. Using the `deltas_to_extend` .txt file, users can specify the distance, in mm, by which to extend the _x_-, _y_-, and _z_-coordinates. The `_SM` extension is the file for extending single material passes, and the `_MM` extension is for multimaterial.

<img width="555" height="77" alt="image" src="https://github.com/user-attachments/assets/00b3502b-892d-4684-8624-e76d3d15a8b2" />


## Tolerancing

Branchpoints represent sites in the vascular network which are particularly prone to nozzle collisions with already-printed ink. This is because the branchpoints tend to contain many coordinates which are spaced closely together. In X-CAVATE, it is possible to "override" points of detected collision by introducing a "tolerance" value. The tolerance value replaces the nozzle outer diameter as the dimension used to detect potential collisions such that any neighboring coordinate A within the "tolerance" for printed coordinate B will be printed within the same print pass as coordinate B, even if the printing of coordinate A introduces a collision with coordinate B.

If no tolerance value is specified by the user, X-CAVATE will default to generating paths without any tolerance (0).

## Padding

If the user does not specify padding, X-CAVATE will default to generating paths without any padding (0).

## Volumetric Flow Rate

This parameter is the volumetric flow rate, Q, of the ink through the printhead nozzle. Q varies with the ink, syringe, and nozzle, and can be experimentally determined using the "calibration.py" script (see readme_calibration.md for instructions).

This value is necessary when printing vessels of varying radii.

If the user does not specify the flow rate, X-CAVATE will default to a value of 0.127 mm^3/s.

###

# Summary of Parameters and Default Values

### Required Parameters:

| Parameter | Description | Value |
| ----------- | ----------- | ----------- |
| network_file | Path to .txt file containing network coordinates | |
| inletoutlet_file | Path to .txt file containing inlet and outlet coordinates | |
| multimaterial | Two inks (arterial, venous) | 1=Yes, 0=No | 
| tolerance_flag | Include tolerance? | 1=Yes, 0=No |
| nozzleOD | Nozzle outer diameter (mm) |  |
| numDecimalsOutput | Number of decimals places for rounding output values | |
| speed_calc | Compute print speeds for changing radii? | 1=Yes, 0=No |
| plots | Generate plots of network print paths? | 1=Yes, 0=No |
| downsample | Downsample interpolated network? | 1=Yes, 0=No | 
| customG | Including custom g-code? | 1=Yes, 0=No |


<br>

### Optional Parameters and Default Values:
| Parameter | Description | Default Value |
| ----------- | ----------- | ----------- |
| tolerance   | Amount of tolerance (mm) | 0 | 
| container_x | Dimensions of print container in x (mm) | 50 |
| container_y | Dimensions of print container in y (mm) | 50 |
| container_z | Dimensions of print container in z (mm) | 50 |
| scaleFactor | Multiple by which to scale the size of the input network | 1 (matches input, i.e. not scaled) |
| downsample_factor | By what factor should xcavate downsample the interpolated network? | 1 (no downsampling) |
| flow | Volumetric flow rate of the ink through the syringe (mm^3/s) | 0.127 |
| topPadding | Amount of padding (mm) to add above maximum z-coordinate in network | 0 |
| dwellStart | Duration of time (s) to dwell at start of print segment | 0.08 |
| dwellEnd | Duration of time (s) to dwell at end of print segment | 0.08|

# Local Code Setup

The input network coordinates should be listed in terms of centimeters. X-CAVATE will internally convert the centimeters to millimeters.

Before running the code, create two new folders within the same folder containing xcavate.py: one folder labeled "input," which should contain the two network .txt files, and an empty folder labled "output."

Ensure Python 3 is installed locally before running xcavate.py.

# Running from the Command Line

The following is an example prompt to run at the command line, with sample parameter values specified:

`python xcavate.py --network_file inputs/VesselNetwork.txt --inletoutlet_file inputs/InletsOutlets.txt --multimaterial 1 --tolerance 0 --nozzleOD 0.65 --numDecimalsOutput 5 --container_height 50 --tolerance_flag 0 --speed_calc 1 --plots 1 --downsample 0 --flow 0.127 --customG 1`
