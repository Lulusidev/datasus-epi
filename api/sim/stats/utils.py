from dataclasses import dataclass
from typing import Any, Dict, Optional, List, Union
import pandas as pd
import numpy as np

@dataclass
class TestResult:
    """Standard container for statistical test results."""
    test_name: str
    statistic: float
    p_value: float
    degrees_of_freedom: Optional[int] = None
    effect_size: Optional[float] = None
    effect_size_name: Optional[str] = None
    confidence_interval: Optional[tuple[float, float]] = None
    additional_metrics: Optional[Dict[str, Any]] = None
    interpretation: Optional[str] = None

def detect_variable_type(series: pd.Series) -> str:
    """
    Detects if a variable is categorical or numeric.
    
    Args:
        series: The pandas Series to check.
        
    Returns:
        'numeric' or 'categorical'.
    """
    if pd.api.types.is_numeric_dtype(series):
        # Check for low cardinality numeric which might be categorical codes
        if series.nunique() < 10 and not pd.api.types.is_float_dtype(series):
            return 'categorical'
        return 'numeric'
    
    return 'categorical'

def decode_age_sim(age_code: Union[str, int]) -> Optional[float]:
    """
    Decodes the SIM 'IDADE' field into years (float).
    
    Format: XYY
    X = Unit (0=min, 1=hour, 2=day, 3=month, 4=year, 5=>100y)
    YY = Value
    
    Returns:
        Age in years.
    """
    if pd.isna(age_code):
        return None
        
    s_code = str(age_code).zfill(3)
    if len(s_code) > 3: 
        # Handle cases where it might be 4 digits (some old formats or errors)
        # Assuming standard 3 digit format for most recent data based on dictionary
        # Dictionary says: "composto de dois subcampos... O primeiro, de 1 dígito... O segundo, de dois dígitos" -> Total 3 digits typically.
        # But sometimes DBF/Parquet stores as larger int.
        s_code = s_code.zfill(3) 

    try:
        unit = int(s_code[0])
        value = int(s_code[1:])
    except ValueError:
        return None

    if unit == 0: # Minutes
        return value / (60 * 24 * 365.25)
    elif unit == 1: # Hours
        return value / (24 * 365.25)
    elif unit == 2: # Days
        return value / 365.25
    elif unit == 3: # Months
        return value / 12.0
    elif unit == 4: # Years
        return float(value)
    elif unit == 5: # Years > 100
        return float(value + 100)
    else:
        return None

def clean_sim_data(df: pd.DataFrame, columns: List[str], ignore_values: List[Any] = [9, '9', ' ', '']) -> pd.DataFrame:
    """
    Cleans specified columns by replacing ignore values with NaN.
    """
    df_clean = df.copy()
    for col in columns:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].replace(ignore_values, np.nan)
    return df_clean

def prepare_binary_variable(series: pd.Series, positive_value: Any) -> pd.Series:
    """
    Converts a categorical variable into binary (0/1) based on a positive value.
    """
    return (series == positive_value).astype(int)
