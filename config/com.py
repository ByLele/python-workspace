import base64
import concurrent.futures
import logging
import os
import re
import time
from dataclasses import dataclass
from functools import wraps
from pathlib import Path
from typing import (
    NamedTuple,
    AnyStr,
    List,
    Literal,
    Generic,
    Union,
    TypeVar,
    Any,
)

import numpy as np
import openpyxl.utils.escape
import pandas as pd
from pandas._typing import DtypeArg
from pandas.core.dtypes.common import is_string_dtype