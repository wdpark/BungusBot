import requests
import json
import urllib

client_id = "24ppj2dxzhfju7rivs0qusm0yvjjr3"
link = 'https://api.twitch.tv/kraken/streams/?game='
headers = {'Accept': 'application/vnd.twitchtv.v5+json', 'Client-ID': client_id}

def getTopStreamers(game):
    game = urllib.parse.quote(game)
    # print (link+game)
    r = requests.get(link + game, headers=headers)
    obj = json.loads(r.text)
    streamList = obj["streams"]

    channelNames = []
    for x in range(0,9):
        streamer = streamList[x]
        displayName = streamer["channel"]["display_name"]
        channelNames.append(displayName)
    print (channelNames)


getTopStreamers("league of legends")
