"""
Compare two directories or files.

This function takes two paths as command line arguments and compares them.
If both paths are files, it compares the files and prints the result.
If both paths are directories, it compares the directories and prints the result for each file.
If the paths are not of the same type (one is a file and the other is a directory), 
it prints an error message.

Usage: python pyhashdiff.py <path1> <path2>
"""

import os
import hashlib
import argparse
from pathlib import Path


def md5_hash(file_path):
    """
    Calculate the MD5 hash of a file.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The MD5 hash of the file, or None if an exception occurs.

    """
    try:
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except (IOError, FileNotFoundError) as e:
        print(f"Error reading file {file_path}: {e}")
        return None


def compare_files(file1, file2):
    """
    Compare two files.

    This function takes two file paths as input and compares the contents of the files.
    It returns a tuple (same, message), where same is a boolean indicating whether the files
    are the same and message is a string describing the result of the comparison.

    Args:
        file1 (str): Path to the first file.
        file2 (str): Path to the second file.

    Returns:
        tuple: A tuple (same, message) where same is a boolean indicating whether the files are
        the same and message is a string describing the result of the comparison.
    """
    size1 = os.path.getsize(file1)
    size2 = os.path.getsize(file2)
    if size1 != size2:
        return (False, f"Sizes differ: {size1} != {size2}")
    md5_1 = md5_hash(file1)
    md5_2 = md5_hash(file2)

    if md5_1 is None or md5_2 is None:
        return (False, "Error calculating MD5 hash.")

    if md5_1 != md5_2:
        return (False, f"MD5 hashes differ: {md5_1} != {md5_2}")

    return (True, "Files are the same.")


def compare_directories(dir1, dir2):
    """
    Compare two directories.

    This function takes two directory paths as input and compares the contents of the directories.
    It returns a dictionary where the keys are file paths relative to the directories,
    and the values are strings describing the result of the comparison.

    Args:
        dir1 (str): Path to the first directory.
        dir2 (str): Path to the second directory.

    Returns:
        dict: A dictionary where the keys are file paths relative to the directories,
        and the values are strings describing the result of the comparison.
    """
    files1 = {f.relative_to(dir1) for f in Path(dir1).rglob("*") if f.is_file()}
    files2 = {f.relative_to(dir2) for f in Path(dir2).rglob("*") if f.is_file()}
    unique_files = files1.symmetric_difference(files2)
    results = {}
    for file in unique_files:
        if file in files1:
            results[str(file)] = "UNIQ: Only in " + str(dir1)
        else:
            results[str(file)] = "UNIQ: Only in " + str(dir2)
    common_files = files1.intersection(files2)
    for file in common_files:
        counterpart = Path(dir2) / file
        same, message = compare_files(str(Path(dir1) / file), str(counterpart))
        if not same:
            results[str(file)] = message
    return results


def main():
    """
    main(): Parse command line arguments and compare the paths.
    """
    parser = argparse.ArgumentParser(description="Compare two directories or files.")
    parser.add_argument("path1", type=str, help="First file/dir path")
    parser.add_argument("path2", type=str, help="Second file/dir path")
    args = parser.parse_args()

    path1 = Path(args.path1)
    path2 = Path(args.path2)

    if path1.is_file() and path2.is_file():
        same, message = compare_files(path1, path2)
        if same:
            print(f"DIFF: {message}")
        else:
            print(f"SAME: {message}")

    elif path1.is_dir() and path2.is_dir():
        results = compare_directories(path1, path2)
        for file, result in results.items():
            print(f"{file}: {result}")
    else:
        print("Both paths must be either files or directories.")


if __name__ == "__main__":
    main()
