import datadotworld as dw

api_client = dw.api_client()

api_client.download_dataset('patrickzhang/asdqq')

api_client.download_file('patrickzhang/asd', 'asdf.csv')