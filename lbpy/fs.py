import os
from pathlib import Path


def read_text(path, encoding="utf-8"):
    """Read a text file and return its content as a string.

    Parameters
    ----------
    path : str or Path
        The path to the text file to be read.
    encoding : str, default="utf-8"
        The character encoding to use when reading the file.

    Returns
    -------
    str
        The content of the text file as a string if successful.
    None
        If the file is not found.

    Raises
    ------
    FileNotFoundError
        If the specified file path does not exist.
    Exception
        For other possible errors during file reading operations.

    Examples
    --------
    ```python
    content = read_text("example.txt")
    content = read_text("/path/to/file.txt", encoding="latin-1")
    ```
    """
    path = Path(path)
    try:
        # Open the text file in read mode
        with open(path, "r", encoding=encoding) as file:
            # Read the entire file content into a string
            text_content = file.read()
            return text_content
    except FileNotFoundError:
        print(f"File was not found: `{path}`")
    except Exception:
        raise


def read_text_dir(
    path,
    recurse: bool = True,
    pattern: str = "*",
    case_sensitive: bool | None = None,
    encoding: str = "utf-8",
):
    """Read all text files in a directory and return their contents in a dictionary.

    Parameters
    ----------
    path : str or Path
        The directory path to read text files from.
    recurse : bool, default=True
        If True, recursively search subdirectories for matching files.
    pattern : str, default="*"
        The glob pattern to match filenames against.
    case_sensitive : bool or None, default=None
        Whether the pattern matching should be case-sensitive.
        If None, follows the system default behavior.
    encoding : str, default="utf-8"
        The character encoding to use when reading files.

    Returns
    -------
    dict
        A dictionary with filenames as keys and file contents as values.
        The dictionary is sorted alphabetically by filename.

    Raises
    ------
    FileNotFoundError
        If the specified directory path does not exist.
    NotADirectoryError
        If the specified path is not a directory.

    Examples
    --------
    ```python
    # Read all text files in a directory
    files_content = read_text_dir("/path/to/directory")

    # Read only .txt files in the current directory, not recursively
    txt_files = read_text_dir(".", recurse=False, pattern="*.txt")
    ```
    """
    path = Path(path)
    # Validate that the path exists and is a directory
    if not path.exists():
        raise FileNotFoundError(f"The path does not exist: '{path}'")
    if not path.is_dir():
        raise NotADirectoryError(f"The path is not a directory: '{path}'")

    # Get mapping of pattern
    if recurse:
        path_map = path.rglob(pattern, case_sensitive=case_sensitive)
    else:
        path_map = path.glob(pattern, case_sensitive=case_sensitive)

    # Get the list of path that is files and not dotfile
    path_list = [f for f in path_map if f.is_file() and not f.name.startswith(".")]
    path_name_list = [f.name for f in path_list]

    # Read files in to dictionary where keys are filenames
    content_dict = {}

    for path_name, path in zip(path_name_list, path_list):
        try:
            content_dict[path_name] = read_text(path, encoding=encoding)
        except Exception as e:
            print(f"Error reading file: '{path_name}'\n {e}")
            continue
    # Sort by filename
    content_dict_sorted = dict(sorted(content_dict.items()))

    return content_dict_sorted


def write_text(text, path, encoding="utf-8", recurse=False, append=False):
    """Write a text string to a text file.

    Parameters
    ----------
    text : str
        The text content to write to the file.
    path : str or Path
        The path to the text file to be written.
    encoding : str, default="utf-8"
        The character encoding to use when writing the file.
    recurse : bool, default=False
        If True, create parent directories if they don't exist.
    append : bool, default=False
        If True, append to the file instead of overwriting.

    Raises
    ------
    PermissionError
        If the process lacks permission to write to the file.
    IsADirectoryError
        If the specified path is a directory, not a file.
    Exception
        For other possible errors during file writing operations.
    """
    path = Path(path)
    try:
        # Create intermediate directories if they don't exist
        if recurse and not path.parent.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            print(f"Created intermediate dir: {path.parent}")

        # Open the text file to write or append content
        with open(path, "a" if append else "w", encoding=encoding) as file:
            file.write(text)
            if append:
                print(f"Text successfully append to {path}")
            else:
                print(f"Text successfully written to {path}")

    except (PermissionError, IsADirectoryError):
        print(f"Cannot write to file: `{path}`")
    except Exception:
        raise
