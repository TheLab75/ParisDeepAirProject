import glob
import os
import time
import pickle
from tensorflow.keras import models

cluster_list=['Paris_est','Paris_south','Paris_north','Paris_west','Paris_center']

def save_model(model=None):
    """
    persist trained model, params and metrics
    """

    timestamp = time.strftime("%Y%m%d-%H%M%S")

    print( "\nSave model to local disk..." )
    for cluster in cluster_list:
    # save model
        if model is not None:
            model_path = os.path.join('model_save','models',cluster)
            print(f"- model path: {model_path}")
            model.save(model_path)

    print("\n✅ data saved locally")

    return None

def load_model(save_copy_locally=False):
    """
    load the latest saved model, return None if no model found
    """
    print("\nLoad model from local disk...")
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    for cluster in cluster_list:
        # get latest model version
        model_directory = os.path.join('model_save','models',cluster)
        print(model_directory)
        results = glob.glob(f"{model_directory}/*")
        if not results:
            return None

        #model_path = sorted(results)[-1]
        #print(f"- path: {model_path}")

        model = models.load_model(model_directory)
        print("\n✅ model loaded from disk")

    #return model_Paris_est, model_Paris_south, model_Paris_north, model_Paris_west, model_Paris_center
    return model

if __name__ == '__main__':
    print(type(load_model()))
