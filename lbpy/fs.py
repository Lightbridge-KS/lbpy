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
