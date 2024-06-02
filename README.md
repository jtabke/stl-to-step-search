# stl-to-step-search

stl-to-step-search is a tool for finding a STEP file that matches a given STL. This can be particularly useful when trying to track down the source STEP file from which an STL was generated, especially when file names are not organized in an obvious manner.

## Overview

There are several potential methods to implement this:

- Bounding Box Comparison: Compare the bounding boxes of the STL and STEP files.
- Volume Comparison: Analyze and compare the volumes of the STL and STEP files.
- Point Cloud Comparison: Compare point clouds derived from the STL and STEP files.
- Surface Distance Comparison: Calculate and compare distances between corresponding surfaces of the STL and STEP files.

However, difficulties may arise due to differences in file formats. While the STL file is represented as a tessellation, the STEP file is represented as a boundary representation.

For initial implementation we have chosen to use bounding box and volume comparisons as the primary methods for finding matching STEP files.

## Install

Due to the lack of other libraries that implement ISO10303-21 STEP file support, we will use the slightly heavy handed pythonocc which implements a full mapping of the OpenCascade geometry kernel and many other features.

1. git clone this repo

```sh
git clone https://github.com/jtabke/stl-to-step-search.git
```

2. [Install pythonocc](https://github.com/tpaviot/pythonocc-core)
   ```sh
   conda create --name=pyoccenv python=3.10
   conda activate pyoccenv
   conda install -c conda-forge pythonocc-core=7.8.1
   ```

## Usage

Run the search.py script with the appropriate command-line arguments:

```sh
python search.py --tolerance=0.02 path_to_your_stl_file.stl path_to_your_directory --depth=2
```

- Tolerance (--tolerance): Specify the tolerance percentage for comparison. Default is 0.02.
- STL File Path: Provide the path to your STL file (path_to_your_stl_file.stl).
- Directory Path: Provide the directory path to search in (path_to_your_directory).
- Depth of Traversal (--depth): Specify the depth of directory traversal. Default is 1.
