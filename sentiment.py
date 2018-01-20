import requests
import json

def sentimentAnalysis(text):
    link = "https://australiaeast.api.cognitive.microsoft.com/text/analytics/v2.0/sentiment"

    same = "{'documents': [{'language': 'en','id': 'string','text': '" + text + "'}]}"
    headers = {"Content-type": "application/json", "Ocp-Apim-Subscription-Key": "e9042e0307e24217b2f0496efeb8dbaf", 'Accept':'application/json'}
    r = requests.post(link, headers=headers, data=same)

    obj = json.loads(r.text)
    return obj["documents"][0]['score']

def unusualValue(score):
    if(score < 0.05 or score > 0.80):
        return True
    else:
        return False
