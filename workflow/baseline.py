from sklearn.metrics import accuracy_score # import library

def baseline(df):
    df_baseline = df.copy()
    df_baseline['ATMO_baseline'] = df_baseline['ATMO'].shift(periods=8,axis=0) #creation of y_pred by shifting target of 7 days
    y_baseline = df_baseline['ATMO_baseline'][8:] #take off the 7 first values to drop nan
    y_true = df_baseline['ATMO'][8:] #take off the 7 first values to drop nan
    accuracy = accuracy_score(y_true, y_baseline) # use accuracy modul from sklearn
#    df_baseline = df_baseline.drop(columns = ['ATMO_baseline'])

    return accuracy
