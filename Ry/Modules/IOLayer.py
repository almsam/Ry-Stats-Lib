import os as _os
import pandas as _pd

from .utils.typing_helpers import copy_callable_signature

@copy_callable_signature(_pd.read_csv)
def read_csv(filepath_or_buffer, /, **kwargs) -> _pd.DataFrame:
    """Reads a CSV file and returns a pandas DataFrame.

    Args:
        filepath_or_buffer (os.PathLike): The path to the CSV file.
        **kwargs: Additional keyword arguments to pass to pandas read_csv.
    Returns:
        pd.DataFrame: The DataFrame containing the CSV data.
    """
    kwargs.pop("filepath_or_buffer", None) # Remove if present to avoid conflicts
    return _pd.read_csv(filepath_or_buffer, **kwargs)


@copy_callable_signature(_pd.read_csv)
def read_tsv(filepath_or_buffer, /, **kwargs) -> _pd.DataFrame:
    """Reads a TSV file and returns a pandas DataFrame.

    Args:
        filepath_or_buffer (os.PathLike): The path to the TSV file.
        **kwargs: Additional keyword arguments to pass to pandas read_csv.
    Returns:
        pd.DataFrame: The DataFrame containing the TSV data.
    """
    kwargs.pop("filepath_or_buffer", None) # Remove if present to avoid conflicts
    kwargs["sep"] = "\t"  # Set separator to tab for TSV files
    return _pd.read_csv(filepath_or_buffer, **kwargs)