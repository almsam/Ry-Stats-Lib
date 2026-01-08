import atexit
import inspect
import importlib.resources
import io
import os
import pathlib
import sys
import typing
from collections.abc import Callable, Hashable, Mapping, Sequence

import pandas as _pd
import numpy as _np

from .utils.typing_helpers import copy_callable_signature

__all__ = (
    "read_csv",
    "read_tsv",
    "read_txt",
    "read_fwf",
    "write_csv",
    "write_txt",
    "save",
    "load",
    "cat",
    "print",
)


################################################
#  Compression Format Detection
################################################

type _SUPPORTED_COMPRESSION_FORMATS = typing.Literal["zstd", "xz", "uncompressed"]
type _SUPPORTED_DTYPES = typing.Literal["pd_series", "pd_dataframe", "np_ndarray"]
SUPPORTED_DTYPES: frozenset[_SUPPORTED_DTYPES] = frozenset({"pd_series", "pd_dataframe", "np_ndarray"})
COMPRESSION_FORMAT: typing.Literal["zstd", "xz"] | None = None
SUPPORTED_COMPRESSION_FORMATS: set[_SUPPORTED_COMPRESSION_FORMATS] = {"uncompressed"}

try:
    from compression import zstd  # pyright: ignore[reportMissingImports]  # Support for zstd compression on 3.14+
    COMPRESSION_FORMAT = "zstd"
    SUPPORTED_COMPRESSION_FORMATS.add("zstd")
except ImportError:
    pass
try:
    from compression import lzma  # pyright: ignore[reportMissingImports]  # Support for xz compression on 3.14+
    if COMPRESSION_FORMAT is None:
        COMPRESSION_FORMAT = "xz"
    SUPPORTED_COMPRESSION_FORMATS.add("xz")
except ImportError:
    try:  # fallback for older Python versions
        import lzma
        if COMPRESSION_FORMAT is None:
            COMPRESSION_FORMAT = "xz"
        SUPPORTED_COMPRESSION_FORMATS.add("xz")
    except ImportError:
        COMPRESSION_FORMAT = None
        
    
################################################
#  Persistent I/O Functions for DataFrames
################################################

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

################################################
#  Custom Save/Load Functions for DataFrames, Series, ndarrays
################################################

def save(obj: _pd.DataFrame | _pd.Series | _np.ndarray, name: str | None = None) -> None:
    """Saves a pandas DataFrame, Series, or numpy ndarray to disk, optionally in a compressed format if available in the stdlib.
    
    Args:
        obj (pd.DataFrame | pd.Series | np.ndarray): The object to save.
        name (str | None): The name to use for the saved file. If None, the variable name will be attempted to inferred.
    Raises:
        TypeError: If obj is not a pandas DataFrame, Series, or numpy ndarray.
        ValueError: If name is None and the variable name cannot be inferred.
    """
    # Infer the variable name if not provided
    if name is None:
        lcl = inspect.stack()[2][0].f_locals
        try:
            name = next((k for k, v in lcl.items() if v is obj))
        except StopIteration:
            raise ValueError("Could not infer variable name; please provide a name argument.") from None
    
    # Create the .RyData directory in the current working directory if it doesn't exist
    cwd = pathlib.Path.cwd()
    ry_data = cwd / ".RyData"
    ry_data.mkdir(exist_ok=True)
    
    # Serialize the object to a BytesIO buffer
    with io.BytesIO() as buf:
        dtype: _SUPPORTED_DTYPES
        # Determine the type of the object and serialize accordingly
        if isinstance(obj, (_pd.Series)):
            obj.to_csv(buf, index=False)
            dtype = "pd_series"
        elif isinstance(obj, (_pd.DataFrame)):
            obj.to_csv(buf, index=False)
            dtype = "pd_dataframe"
        elif isinstance(obj, _np.ndarray):
            # Disallow pickling for security reasons and to ensure compatibility across different numpy or Python versions
            _np.save(buf, obj, allow_pickle=False)
            dtype = "np_ndarray"
        else:
            raise TypeError("obj must be a pandas DataFrame, Series, or numpy ndarray.")
        
        # Write the buffer to disk with the appropriate compression format
        buf.seek(0)
        with open(ry_data.joinpath(f"{name}"), "wb") as output_file:
            output_file.write(dtype.encode("utf-8") + b"\n")
            match COMPRESSION_FORMAT:
                case "zstd":
                    output_file.write(b"zstd\n")
                    with zstd.open(output_file, "wb") as f:
                        f.write(buf.getvalue())
                case "xz":
                    output_file.write(b"xz\n")
                    with lzma.open(output_file, "wb") as f:
                        f.write(buf.getvalue())
                case None:
                    output_file.write(b"uncompressed\n")
                    output_file.write(buf.getvalue())
                case _:
                    typing.assert_never(COMPRESSION_FORMAT)

def load(name: str) -> _pd.DataFrame | _pd.Series | _np.ndarray:
    """Loads a pandas DataFrame, Series, or numpy ndarray from disk, optionally in a compressed format if available in the stdlib.
    
    Args:
        name (str): The name of the file to load (without extension).
    Returns:
        pd.DataFrame | pd.Series | np.ndarray: The loaded object.
    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file is not a supported data type or compression format.
    """
    # Try to load the file from the .RyData directory in the current working directory
    cwd = pathlib.Path.cwd()
    ry_data = cwd / ".RyData"
    if not ry_data.exists():
        raise FileNotFoundError(f"No data has been saved in the current working directory: {cwd!r}.")
    file = ry_data / name
    if not file.exists():
        raise FileNotFoundError(f"No saved data found with the name: {name!r}.")
    with open(file, "rb") as f:
        # The first line is the data type (see SUPPORTED_DTYPES for currently supported types)
        dtype = f.readline().strip().decode("utf-8")
        if dtype not in SUPPORTED_DTYPES:
            raise ValueError(f"Unsupported data type found in file: {dtype!r}.")
        # The second line is the compression format (see SUPPORTED_COMPRESSION_FORMATS for currently supported formats)
        compression = f.readline().strip().decode("utf-8")
        if compression not in SUPPORTED_COMPRESSION_FORMATS:
            raise ValueError(f"Unsupported compression format found in file: {compression!r}.")
        # Read the rest of the file based on the compression format into a buffer (BytesIO)
        match compression:
            case "zstd":
                with zstd.open(f, "rb") as comp_f:
                    data = io.BytesIO(comp_f.read())
            case "xz":
                with lzma.open(f, "rb") as comp_f:
                    data = io.BytesIO(comp_f.read())
            case "uncompressed":
                data = io.BytesIO(f.read())
            case _:
                typing.assert_never(compression)
    
    # Finally, unserialize the data based on the data type
    data.seek(0)
    match dtype:
        case "pd_series":
            # Read as 1-column DataFrame and convert to Series
            return _pd.read_csv(data, index_col=0).squeeze("columns")  # pyright: ignore[reportReturnType]
        case "pd_dataframe":
            # Read as DataFrame
            return _pd.read_csv(data)
        case "np_ndarray":
            # Read as ndarray
            return _np.load(data)
        case _:
            typing.assert_never(dtype)

#################################################
# Console and Stream I/O Functions
#################################################

def cat(obj: typing.Any) -> None:
    """Prints the string representation of an object to the console without any additional formatting.

    Args:
        obj: The object to print.
    """
    if isinstance(obj, bytes):
        print(obj.decode("utf-8"))
    elif isinstance(obj, str):
        print(obj)
    # Pandas DataFrames and Series have their own pretty-printing methods
    elif isinstance(obj, (_pd.DataFrame, _pd.Series)):
        _pd.set_option("display.max_columns", None)
        _pd.set_option("display.max_rows", None)
        print(obj.to_string())
    # Numpy ndarrays also have their own pretty-printing methods
    elif isinstance(obj, _np.ndarray):
        _np.set_printoptions(threshold=None)
        print(obj)
    else:
        # use the default string representation for other types
        print(repr(obj))


def print(obj: typing.Any) -> None:
    """Prints the string representation of an object to the console with default formatting.

    Args:
        obj: The object to print.
    """
    # Pandas DataFrames and Series have their own pretty-printing methods
    if isinstance(obj, (_pd.DataFrame, _pd.Series)):
        _pd.set_option("display.max_columns", 20)
        _pd.set_option("display.max_rows", 60)
        print(obj.to_string())
    # Numpy ndarrays also have their own pretty-printing methods
    elif isinstance(obj, _np.ndarray):
        _np.set_printoptions(threshold=1000)
        print(obj)
    else:
        # use pprint for other types
        import pprint
        pprint.pprint(obj)


def sink(file: os.PathLike[str] | io.TextIOWrapper | None = None) -> None:
    """Redirects the standard output to a file or back to the console.

    Args:
        file (os.PathLike[str] | None): The path to the output file, or None (default) to redirect back to the console.
    """
    if file is None:
        # Restore standard output to console
        sys.stdout = sys.__stdout__
    elif isinstance(file, io.TextIOWrapper):
        # Redirect standard output to the provided file-like object
        sys.stdout = file
    else:
        f = open(file, "w")
        sys.stdout = f
        # Try to close the file on program exit
        def close_file(): 
            try:
                f.close()
            except Exception:
                pass
        atexit.register(close_file)

#################################################
# Load Builtin Datasets
##################################################

def data(name: str) -> _pd.DataFrame | _np.ndarray:
    """Loads a builtin dataset by name.

    Args:
        name (str): The name of the dataset to load.
    Returns:
        pd.DataFrame | np.ndarray: The loaded dataset.
    Raises:
        FileNotFoundError: If the dataset does not exist.
    """
    try:
        with importlib.resources.open_binary("Ry.Data", name) as f:
            if name.endswith(".csv"):
                return _pd.read_csv(f)
            elif name.endswith(".npy"):
                return _np.load(f)
            else:
                raise FileNotFoundError(f"Unknown dataset: {name!r}.")
    except FileNotFoundError:
        raise FileNotFoundError(f"Unknown dataset: {name!r}.") from None
