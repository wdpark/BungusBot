import socket, string
import time
import keyboard
from bs4 import BeautifulSoup
import urllib
import codecs
import json
import sys
from bottle import route, run, template, static_file, get, post, request, BaseRequest
from threading import Thread
from time import sleep

@route('/')
def send_static():
    # return ("?")
    return static_file("main.html", root='web/')

@route('/clip1', method='POST')
def do_uploadc():
    print("make the clip u booster")
    clip(1)
    return "hehexd"

def threadfunc():
    run(host="0.0.0.0", port=8000)

thread = Thread(target = threadfunc)
thread.daemon = True
thread.start()
print("threading worked")

# Set all the variables necessary to connect to Twitch IRC
HOST = "irc.twitch.tv"
NICK = "BungusBot"
PORT = 6667
PASS = "oauth:yoq3z1p3t3kt4pz1cl4n5nil3zq72a"
readbuffers = []
MODT = False

# streamers = ["riotgames", "imaqtpie", "moonmoon_ow"]
streamers = ["riotgames"]

sockets = []
counts = []
avgss = []
for i in range(len(streamers)):
    # Connecting to Twitch IRC by passing credentials and joining a certain channel
    s = socket.socket()
    s.connect((HOST, PORT))
    s.send("PASS " + PASS + "\r\n")
    s.send("NICK " + NICK + "\r\n")
    s.send("JOIN #%s \r\n" % streamers[i])
    sockets.append(s);
    counts.append(0);
    avgss.append([]);
    avgss[i].append(1);
    readbuffers.append("");

iters = 0

if sys.argv[1] == "load":
    avgss = json.load(open('data.txt'))
    iters = 50

start = time.time()
skip = 0

def getVideo(html_doc, name):
    soup = BeautifulSoup(html_doc, 'html.parser')
    video_link = soup.video['src'][:-4]
    test=urllib.FancyURLopener()
    test.retrieve(video_link,name+".mp4")



def clip(streamerid):
    print("clipping")
    #Switch screens from terminal to chrome
    time.sleep(1)
    keyboard.press(59) #ctrl
    keyboard.press(19) #2
    keyboard.release(59)
    keyboard.release(19)

    time.sleep(2)

    #Open new chrome tab
    keyboard.press(55) #command
    keyboard.press(45) #N
    keyboard.release(55) #command
    keyboard.release(45) #N

    time.sleep(2)

    #Type streamer URL into chrome search bar
    keyboard.write('twitch.tv/riotgames')
    time.sleep(0.5)
    keyboard.send(36)

    #Get Clip
    time.sleep(7)
    keyboard.press(58) #alt
    keyboard.press(7) #X
    keyboard.release(58)
    keyboard.release(7)
    time.sleep(12) #there may be some lag in internet speed

    #Write a title for clip
    keyboard.write("%s%d" % (streamers[streamerid], iters))
    keyboard.send(36) #enter

    time.sleep(10)

    #Save
    keyboard.press(55) #command
    keyboard.press(1) #S
    keyboard.release(55)
    keyboard.release(1)
    keyboard.send(36)

    time.sleep(5)

    f=codecs.open("/Users/kevin/Downloads/%s%d.html" % (streamers[streamerid], iters), 'r')
    text = f.read()
    getVideo(text, "%s%d" % (streamers[streamerid], iters))
    print("download a clip!!!!!!")
    skip = 2
    pass

while True:
    for i in range(len(streamers)):
        readbuffers[i] = readbuffers[i] + sockets[i].recv(1024)
        temp = string.split(readbuffers[i], "\n")
        readbuffers[i] = temp.pop()

        for line in temp:
            if (line[0] == "PING"):
                sockets[i].send("PONG %s\r\n" % line[1])
            else:
                parts = string.split(line, ":")
                if "QUIT" not in parts[1] and "JOIN" not in parts[1] and "PART" not in parts[1]:
                    try:
                        message = parts[2][:len(parts[2]) - 1]
                    except:
                        message = ""
                    usernamesplit = string.split(parts[1], "!")
                    username = usernamesplit[0]
                    if MODT:
                        # print(username + ": " + message)
                        counts[i] += 1;
                    for l in parts:
                        if "End of /NAMES list" in l:
                            MODT = True

    if time.time() > start + 10:
        iters += 1
        start = time.time()

        with open('data.txt', 'w') as outfile:
            json.dump(avgss, outfile)

        for i in range(len(streamers)):
            avg = sum(avgss[i]) / float(len(avgss[i]))
            print("streamer %s count: %d, avg: %d" % (streamers[i], counts[i], avg))

            if iters > 10 and counts[i] > avg*1.5 and skip == 0:
                clip(i)
                skip = 4

            if skip == 0:
                avgss[i].append(counts[i]);
                if(len(avgss[i]) > 10):
                    avgss[i].pop()
            else:
                print("(skipperino)")
                skip -= 1;

            counts[i] = 0;
