import requests
import pandas as pd

collection = "observations"
base_url = f"https://api.dataplatform.knmi.nl/edr/collections/{collection}"
token = "eyJvcmciOiI1ZTU1NGUxOTI3NGE5NjAwMDEyYTNlYjEiLCJpZCI6IjcxZGFmYmI1NGZkYTQ4NjI5ZGU0Mjk5OTM1ZDlmMzdmIiwiaCI6Im11cm11cjEyOCJ9"
headers = {"Authorization": token}

request = requests.get(url='https://api.dataplatform.knmi.nl/edr/collections/observations', headers=headers)
jsonre = request.json()
df = pd.json_normalize(jsonre)
print(df)


