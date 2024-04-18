# File and Directory Comparer

This Python script allows users to compare two files or two directories. When comparing files, it checks if they differ by size or MD5 hash. For directories, it recursively examines each directory and reports differences between files by existence, size, or MD5 hash.

## Requirements

- Python 3.x

## Installation

No installation is needed. Just ensure you have Python 3.x installed on your system. You can download Python from [python.org](https://www.python.org/downloads/).

## Usage

To use the script, you need to pass two pathnames as command-line arguments. Here's how to run the script:

```bash
python compare.py <path1> <path2>
```

Where:
- `<path1>`: First file or directory to compare.
- `<path2>`: Second file or directory to compare.

### Examples

1. **Comparing Two Files**:

```bash
python pyhashdiff.py file1.txt file2.txt
```

2. **Comparing two directories**

```
bash
python pyhashdiff.py dir1/ dir2/
```

This will recursively compare the directories and list differences in file existence, size, or MD5 hash.

## Functionality

- **File Comparison**: Compares two files to determine if there are any differences in size or MD5 hash.
- **Directory Comparison**: Recursively compares files within two directories. Reports files that are unique to each directory and compares common files for differences in size or MD5 hash.

## License

This project is licensed under the GNU GPL v3 License - see the [LICENSE](LICENSE.md) file for details.
