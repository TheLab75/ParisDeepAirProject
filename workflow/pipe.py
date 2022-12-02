#Fichier pour stocker le pipeline qui sera call dans le fichier de preprocessing

from sklearn.pipeline import make_pipeline
from sklearn.compose import make_column_transformer
from sklearn.impute import SimpleImputer

num_features_normal = ['NO2']
num_features_skewed = ['PM25','PM10']

num_imputer_normal = make_pipeline(
    SimpleImputer(strategy='median'))

num_imputer_skewed = make_pipeline(
    SimpleImputer(strategy='median'))

preprocessor_imputer = make_column_transformer(
    (num_imputer_normal, num_features_normal),
    (num_imputer_skewed, num_features_skewed))

#Robust Scaler pour les polluants
from sklearn.preprocessing import RobustScaler

preprocessor_scaler = make_pipeline(
    RobustScaler())
