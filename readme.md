# ML Model to Detect Sentiment of Product Reviews online

### 1-Data preprocessing
In order to prepare the data for the analysis, it is possible to use the data preparation tools that ML Workbench provides.

Data are available to dowload on Kaggle: [Amazon Reviews](https://www.kaggle.com/bittlingmayer/amazonreviews)

More information on how to [prepare the data in ML Workbench](https://docs.microsoft.com/en-us/azure/machine-learning/preview/tutorial-classifying-iris-part-1)

### 2-Build model
The file *train.py* contains the Python code to apply the machine learning algorithm to the data.

The file *score.py* contains the Python code to test the model created in the previous file on the test dataset.

On the [docs](https://docs.microsoft.com/en-us/azure/machine-learning/preview/tutorial-classifying-iris-part-2) it is possible to understand better how to execute the code.

### 3-Deploy model
` az ml env setup -n <new deployment environment name> --location <e.g. eastus2> `

Add `-c` or `--cluster` switch in the following command to set up an environment in cluster mode later.

` az ml account modelmanagement set -n <youracctname> -g <yourresourcegroupname> `

` az ml env set -n <deployment environment name> -g <existing resource group name> `

` az ml service create realtime -f score_iris.py --model-file model.pkl -s service_schema.json -n irisapp -r python --collect-model-data true -c aml_config\conda_dependencies.yml `

parameters are:
- -f: The scoring script file name.

- --model-file: The model file. In this case, it's the pickled model.pkl file.

- -s: The service schema. This was generated in a previous step by running the score_iris.py script locally.

- -n: The app name, which must be all lowercase.

- -r: The runtime of the model. In this case, it's a Python model. Valid runtimes are python and spark-py.

- --collect-model-data true: This switch enables data collection.

- -c: Path to the conda dependencies file where additional packages are specified.

Command to gain more info about the model deployed:
` az ml model show -m a76c078203d9426b8647bba2a1854944 `

` az ml manifest show -i 256f60c7-e085-4ad8-9802-3ccacbe261e7 `

When it finishes:
` docker ps ` to see the container running locally on Docker

Output from the Command Prompt:

 model.pkl
Successfully registered model
Id: dc48590341a74de8811e48922076abc3
More information: 'az ml model show -m dc48590341a74de8811e48922076abc3'
Creating new driver at C:\Users\jetiba\AppData\Local\Temp\tmpzkdxth20.py
 score.py
 service_schema.json
Successfully created manifest
Id: e541e271-5885-40d9-9842-e4d2fcc867f6
More information: 'az ml manifest show -i e541e271-5885-40d9-9842-e4d2fcc867f6'
Creating image................................................................Done.
Image ID: eb03653e-3f6c-4f70-8e28-af8322a6565e
More details: 'az ml image show -i eb03653e-3f6c-4f70-8e28-af8322a6565e'
Usage information: 'az ml image usage -i eb03653e-3f6c-4f70-8e28-af8322a6565e'
[Local mode] Running docker container.
[Local mode] Pulling the image from mlcrpacr14c72735e14d.azurecr.io/textsentapp:4. This may take a few minutes, depending on your connection speed...
[Local mode] Pulling..............................................
[Local mode] Waiting for container to initialize
[Local mode] Done
[Local mode] Service ID: textsentapp
[Local mode] Usage for cmd: az ml service run realtime -i textsentapp -d "{\"input_df\": [{\"Text\": \"This is a great 1st drone and I was amazed by it. I got it for my son and he loves it.\"}]}"
[Local mode] Usage for powershell: az ml service run realtime -i textsentapp --% -d "{\"input_df\": [{\"Text\": \"This is a great 1st drone and I was amazed by it. I got it for my son and he loves it.\"}]}"
[Local mode] Additional usage information: 'az ml service usage realtime -i textsentapp'

To test the model you can try this:
az ml service run realtime -i textsentapp -d "{\"input_df\": [{\"Text\": \"some new feedback to test if it works!!\"}]}"