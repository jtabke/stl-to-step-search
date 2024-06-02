import os
import argparse
from OCC.Extend.DataExchange import read_stl_file, read_step_file
from OCC.Extend.ShapeFactory import measure_shape_volume, get_boundingbox
from OCC.Extend.TopologyUtils import TopologyExplorer


def analyze_stl(stl_file):
    shape = read_stl_file(stl_file)
    shape_volume = measure_shape_volume(shape)
    shape_bounding_box = get_boundingbox(shape)
    xmin, ymin, zmin, xmax, ymax, zmax = shape_bounding_box
    size_x = xmax - xmin
    size_y = ymax - ymin
    size_z = zmax - zmin

    num_faces = TopologyExplorer(shape).number_of_faces()
    num_shells = TopologyExplorer(shape).number_of_shells()

    return {
        "volume": shape_volume,
        "bounding_box": (xmin, ymin, zmin, xmax, ymax, zmax),
        "size": (size_x, size_y, size_z),
        "num_faces": num_faces,
        "num_shells": num_shells,
    }


def analyze_step(step_file):
    shape = read_step_file(step_file, verbosity=False)
    shape_volume = measure_shape_volume(shape)
    shape_bounding_box = get_boundingbox(shape)
    xmin, ymin, zmin, xmax, ymax, zmax = shape_bounding_box
    size_x = xmax - xmin
    size_y = ymax - ymin
    size_z = zmax - zmin

    num_faces = TopologyExplorer(shape).number_of_faces()
    num_shells = TopologyExplorer(shape).number_of_shells()

    return {
        "volume": shape_volume,
        "bounding_box": (xmin, ymin, zmin, xmax, ymax, zmax),
        "size": (size_x, size_y, size_z),
        "num_faces": num_faces,
        "num_shells": num_shells,
    }


def compare_files(stl_analysis, step_analysis, tolerance_percentage):
    volume_diff_percentage = (
        abs(stl_analysis["volume"] - step_analysis["volume"]) / stl_analysis["volume"]
    )
    size_diff_x_percentage = (
        abs(stl_analysis["size"][0] - step_analysis["size"][0])
        / stl_analysis["size"][0]
    )
    size_diff_y_percentage = (
        abs(stl_analysis["size"][1] - step_analysis["size"][1])
        / stl_analysis["size"][1]
    )
    size_diff_z_percentage = (
        abs(stl_analysis["size"][2] - step_analysis["size"][2])
        / stl_analysis["size"][2]
    )

    if (
        volume_diff_percentage <= tolerance_percentage
        and size_diff_x_percentage <= tolerance_percentage
        and size_diff_y_percentage <= tolerance_percentage
        and size_diff_z_percentage <= tolerance_percentage
    ):
        return True
    return False


def search_directory(stl_file, directory, depth, tolerance_percentage):
    stl_analysis = analyze_stl(stl_file)
    matching_files = []

    for root, dirs, files in os.walk(directory):
        current_depth = root.count(os.sep) - directory.count(os.sep)
        if current_depth >= depth:
            del dirs[:]
            continue

        for file in files:
            if file.lower().endswith(".step"):
                step_file = os.path.join(root, file)
                step_analysis = analyze_step(step_file)

                if compare_files(stl_analysis, step_analysis, tolerance_percentage):
                    matching_files.append(step_file)

    return matching_files


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Search for matching STEP files in a directory."
    )
    parser.add_argument(
        "--tolerance",
        type=float,
        default=0.02,
        help="Tolerance percentage for comparison.",
    )
    parser.add_argument("stl_file", type=str, help="Path to the STL file.")
    parser.add_argument("directory", type=str, help="Directory to search in.")
    parser.add_argument(
        "--depth", type=int, default=1, help="Depth of directory traversal."
    )

    args = parser.parse_args()

    matching_files = search_directory(
        args.stl_file, args.directory, args.depth, args.tolerance
    )
    if matching_files:
        print("Matching STEP files found:")
        for file in matching_files:
            print(file)
    else:
        print("No matching STEP files found.")
