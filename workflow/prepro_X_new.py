from workflow.preprocessing import preprocess
import pd
from workflow.params import LOCAL_DATA_PATH_2
def get_X_new():
    raw_df = pd.read_csv(f"{LOCAL_DATA_PATH_2}.csv").copy()
    df = preprocess(raw_df)
    X_new = df[len(df-7)]
    return X_new
