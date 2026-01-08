import os
import typing
from collections.abc import Callable, Hashable, Mapping, Sequence

import pandas as _pd

from .utils.typing_helpers import copy_callable_signature

__all__ = (
    "read_csv",
    "read_tsv",
    "read_txt",
    "read_fwf",
    "write_csv",
    "write_txt",
)

@copy_callable_signature(_pd.read_csv)
def read_csv(fp, /, **kwargs) -> _pd.DataFrame:
    """Reads a CSV file and returns a pandas DataFrame.

    Args:
        fp (os.PathLike): The path to the CSV file.
        **kwargs: Additional keyword arguments to pass to pandas read_csv.
    Returns:
        pd.DataFrame: The DataFrame containing the CSV data.
    """
    kwargs.pop("filepath_or_buffer", None) # Remove if present to avoid conflicts
    kwargs.pop("delimiter", None)  # Remove delimiter if present to avoid conflicts
    kwargs["sep"] = ","  # Set separator to comma for CSV files
    return _pd.read_csv(fp, **kwargs)


@copy_callable_signature(_pd.read_csv)
def read_tsv(fp, /, **kwargs) -> _pd.DataFrame:
    """Reads a TSV file and returns a pandas DataFrame.

    Args:
        fp (os.PathLike): The path to the TSV file.
        **kwargs: Additional keyword arguments to pass to pandas read_csv.
    Returns:
        pd.DataFrame: The DataFrame containing the TSV data.
    """
    kwargs.pop("filepath_or_buffer", None) # Remove if present to avoid conflicts
    kwargs.pop("delimiter", None)  # Remove delimiter if present to avoid conflicts
    kwargs["sep"] = "\t"  # Set separator to tab for TSV files
    return _pd.read_csv(fp, **kwargs)


@copy_callable_signature(_pd.read_csv)
def read_txt(fp, /, **kwargs) -> _pd.DataFrame:
    """Reads a TXT file and returns a pandas DataFrame.

    Args:
        fp (os.PathLike): The path to the TXT file.
        **kwargs: Additional keyword arguments to pass to pandas read_csv.
    Returns:
        pd.DataFrame: The DataFrame containing the TXT data.
    """
    kwargs.pop("filepath_or_buffer", None) # Remove if present to avoid conflicts
    return _pd.read_csv(fp, **kwargs)


@copy_callable_signature(_pd.read_fwf)
def read_fwf(fp, /, **kwargs) -> _pd.DataFrame:
    """Reads a fixed-width formatted file and returns a pandas DataFrame.

    Args:
        fp (os.PathLike): The path to the fixed-width formatted file.
        **kwargs: Additional keyword arguments to pass to pandas read_fwf.
    Returns:
        pd.DataFrame: The DataFrame containing the fixed-width formatted data.
    """
    kwargs.pop("filepath_or_buffer", None) # Remove if present to avoid conflicts
    return _pd.read_fwf(fp, **kwargs)

type CompressionOptions = typing.Literal["infer", "gzip", "bz2", "zip", "xz", "zstd", "tar"] | dict[str, typing.Any]
type OpenFileErrors = typing.Literal[
    "strict",
    "ignore",
    "replace",
    "surrogateescape",
    "xmlcharrefreplace",
    "backslashreplace",
    "namereplace",
]

class WriteCSVKwargs(typing.TypedDict, total=False):
    sep: str
    na_rep: str
    float_format: str | Callable | None
    columns: Sequence[Hashable] | None
    header: bool | list[str]
    index: bool
    index_label: Hashable | Sequence[Hashable] | None
    encoding: str | None
    compression: CompressionOptions
    quoting: typing.Literal[0, 1, 2, 3, 4, 5]
    quotechar: str
    lineterminator: str | None
    chunksize: int | None
    date_format: str | None
    doublequote: bool
    escapechar: str | None
    decimal: str
    errors: OpenFileErrors
    storage_options: dict[str, typing.Any] | None


def write_csv(df: _pd.DataFrame, fp: os.PathLike, /, **kwargs: typing.Unpack[WriteCSVKwargs]) -> None:
    """Writes a pandas DataFrame to a CSV file.

    Args:
        df (pd.DataFrame): The DataFrame to write.
        fp (os.PathLike): The path to the output CSV file.
        **kwargs: Additional keyword arguments to pass to pandas to_csv.
    """
    if not isinstance(df, _pd.DataFrame):
        raise TypeError(f"df must be of type {_pd.DataFrame.__name__!r}, not {type(df).__name__!r}.")
    kwargs.pop("path_or_buf", None)  # Remove if present to avoid conflicts
    kwargs["mode"] = "w"  # pyright: ignore[reportGeneralTypeIssues]  # force truncate-write mode
    df.to_csv(fp, **kwargs)  # pyright: ignore[reportArgumentType, reportCallIssue]

type FormattersType = list[Callable] | tuple[Callable, ...] | Mapping[str | int, Callable]

class WriteTXTKwargs(typing.TypedDict, total=False):
    columns: list[str] | tuple[str, ...] | None
    col_space: int | list[int] | dict[Hashable, int] | None
    header: bool | list[str] | tuple[str, ...]
    index: bool
    na_rep: str
    formatters: FormattersType | None
    float_format: str | Callable | None
    sparsify: bool | None
    index_names: bool
    justify: str | None
    max_rows: int | None
    max_cols: int | None
    show_dimensions: bool
    decimal: str
    line_width: int | None
    min_rows: int | None
    max_colwidth: int | None
    encoding: str | None
    

@typing.overload
def write_txt(df: _pd.DataFrame, fp: os.PathLike[str], /, **kwargs: typing.Unpack[WriteTXTKwargs]) -> None:
    ...


@typing.overload
def write_txt(df: _pd.DataFrame, fp: None = None, /, **kwargs: typing.Unpack[WriteTXTKwargs]) -> str:
    ...

def write_txt(df: _pd.DataFrame, fp: os.PathLike[str] | None = None, /, **kwargs: typing.Unpack[WriteTXTKwargs]) -> str | None:
    """Writes a pandas DataFrame to a TXT file.

    Args:
        df (pd.DataFrame): The DataFrame to write.
        fp (os.PathLike[str] | None): The path to the output TXT file, or None (default) to return the output as a string.
        **kwargs: Additional keyword arguments to pass to pandas to_csv.
    """
    if not isinstance(df, _pd.DataFrame):
        raise TypeError(f"df must be of type {_pd.DataFrame.__name__!r}, not {type(df).__name__!r}.")
    kwargs.pop("path_or_buf", None)  # Remove if present to avoid conflicts
    return df.to_string(fp, **kwargs) 
    
    