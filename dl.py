#!/usr/bin/python

import urllib.request
import os

basedir = 'downloads/'

# read each line in file as a url. your fault if url syntax is wrong.
for url in open('urls.txt', 'r'):
    # parse the clip source channel
    channel = url.split('/')[3]

    # use the twitch generated url path as the filename because it's
    # guarenteed to be unique and who wants to do extra work
    filename = url.split('/')[4]

    # tell the user where we're downloading to
    outputpath = (basedir + channel + '/' + filename + '.mp4').replace('\n', '')
    print(outputpath)

    # create downloads dir if it doesn't exist already
    if not os.path.exists(basedir + channel + '/'):
        os.makedirs(basedir + channel + '/')

    # get html content from url
    html = str(urllib.request.urlopen(url).read())

    # extract the mp4 url for source quality
    mp4url = html.split('source\":\"')[1].split('\"}')[0]

    # download file to output path
    urllib.request.urlretrieve(mp4url, outputpath)

input('Finished. Press enter to exit.')
