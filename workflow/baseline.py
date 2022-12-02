from sklearn.metrics import accuracy_score # import library

def baseline(df):
    df['ATMO_baseline'] = df['ATMO'].shift(periods=8,axis=0) #creation of y_pred by shifting target of 7 days
    y_baseline = df['ATMO_baseline'][8:] #take off the 7 first values to drop nan
    y_true = df['ATMO'][8:] #take off the 7 first values to drop nan
    accuracy = accuracy_score(y_true, y_baseline) # use accuracy modul from sklearn
    df = df.drop(columns = ['ATMO_baseline'])

    return df, accuracy
