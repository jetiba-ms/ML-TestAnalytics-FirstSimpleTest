try:
    from azureml.datacollector import ModelDataCollector
except ImportError:
    print("Data collection is currently only supported in docker mode. May be disabled for local mode.")
    # Mocking out model data collector functionality
    class ModelDataCollector(object):
        def nop(*args, **kw): pass
        def __getattr__(self, _): return self.nop
        def __init__(self, *args, **kw): return None
    pass

import os

def init():
    global inputs_dc, prediction_dc
    # Get the path to the model asset
    # local_path = get_local_path('mymodel.model.link')
    from sklearn.externals import joblib
    
    inputs_dc = ModelDataCollector("model.pkl", identifier="inputs")
    prediction_dc = ModelDataCollector("model.pkl", identifier="prediction")

    # Load model using appropriate library and function
    global model
    # model = model_load_function(local_path)
    model = joblib.load('model.pkl')

def run(input_df):
    import json
    
    #vect!
    pred = model.predict(input_df['Text'])
    prediction_dc.collect(pred)
    return json.dumps(str(pred[0]))
    #(str(pred[0]))

def main():
    from azureml.api.schema.dataTypes import DataTypes
    from azureml.api.schema.sampleDefinition import SampleDefinition
    from azureml.api.realtime.services import generate_schema
    import pandas

    df = pandas.DataFrame(data=["What a waste of time and money! The story was not realistic at all! Actually it was completely far fetched!"], columns=['Text'])

    # Turn on data collection debug mode to view output in stdout
    os.environ["AML_MODEL_DC_DEBUG"] = 'true'

    # Test the output of the functions
    init()
    input1 = pandas.DataFrame(data=["What a waste of time and money! The story was not realistic at all! Actually it was completely far fetched!"], columns=['Text'])
    print("The input {0} created the following output: {1}".format(input1['Text'], run(input1)))

    inputs = {"input_df": SampleDefinition(DataTypes.PANDAS, df)}

    #Genereate the schema
    generate_schema(run_func=run, inputs=inputs, filepath='./outputs/service_schema.json')
    print("Schema generated")


# Implement test code to run in IDE or Azure ML Workbench
if __name__ == '__main__':
    main()