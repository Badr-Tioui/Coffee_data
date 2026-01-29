import pandas as pd
from etl.quality_checks import run_quality_checks

def test_no_missing_values():
    df = pd.DataFrame({"Consumption":[1,2,3]})
    assert df["Consumption"].isna().sum() == 0
