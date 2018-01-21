import socket, string
import time
import keyboard
from bs4 import BeautifulSoup
import urllib.request
import codecs
import json
import sys
from bottle import route, run, template, static_file, get, post, request, BaseRequest, Bottle, abort
from threading import Thread
from time import sleep

@route('/')
def send_static2():
    # return ("?")
    return static_file("main2.html", root='web/')

@route('/<filename:path>')
def send_static(filename):
    return static_file(filename, root='web/')

@route('/clip1', method='POST')
def do_uploadc():
    print("make the clip u booster")
    clip(0)
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

streamers = ["a_seagull", "nl_kripp", "riotgames", "tsm_theoddone"]
# streamers = ["riotgames"]

sockets = []
counts = []
avgss = []
chats = []

test = 0

app = Bottle()

@app.route('/websocket')
def handle_websocket():
    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        abort(400, 'Expected WebSocket request.')

    while True:
        time.sleep(0.5)
        wsock.send(json.dumps(avgss))
        # try:
        #     message = wsock.receive()
        #     wsock.send("Your message was: %r" % message)
        # except WebSocketError:
        #     break


from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler

def threadfunc2():
    server = WSGIServer(("0.0.0.0", 8080), app,
                        handler_class=WebSocketHandler)
    server.serve_forever()

thread = Thread(target = threadfunc2)
thread.daemon = True
thread.start()
print("threading worked")




for i in range(len(streamers)):
    # Connecting to Twitch IRC by passing credentials and joining a certain channel
    s = socket.socket()
    s.connect((HOST, PORT))
    s.send(("PASS " + PASS + "\r\n").encode())
    s.send(("NICK " + NICK + "\r\n").encode())
    s.send(("JOIN #%s \r\n" % streamers[i]).encode())
    sockets.append(s);
    counts.append(0);
    avgss.append([]);
    avgss[i].append(1);
    readbuffers.append("");

iters = 0

if sys.argv[1] == "load":
    avgss = json.load(open('data.txt'))
    iters = 100

start = time.time()
skip = 0

def getVideo(html_doc, name):
    soup = BeautifulSoup(html_doc, 'html.parser')
    video_link = soup.video['src'][:-4]
    test=urllib.request.FancyURLopener()
    test.retrieve(video_link,name+".mp4")


def clip(streamerid):
    global chats
    print("clipping")

    theiters = iters

    with open('%s%d.txt' % (streamers[streamerid], theiters), 'w') as outfile:
        json.dump(chats, outfile)
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
    time.sleep(5)

    keyboard.press(58) #alt
    keyboard.press(7) #X
    keyboard.release(58)
    keyboard.release(7)
    time.sleep(15) #there may be some lag in internet speed

    #Save
    keyboard.press(55) #command
    keyboard.press(1) #S
    keyboard.release(55)
    keyboard.release(1)
    time.sleep(0.5)

    #Write title for clip in finder
    keyboard.write("%s%d" % (streamers[streamerid], theiters))
    keyboard.send(36) #enter
    time.sleep(2)

    #Close 2 tabs
    keyboard.press(55) #command
    keyboard.press(13) #W
    keyboard.release(55) #command
    keyboard.release(13) #W

    time.sleep(1)

    keyboard.press(55) #command
    keyboard.press(13) #W
    keyboard.release(55) #command
    keyboard.release(13) #W

    f=codecs.open("/Users/kevin/Downloads/%s%d.html" % (streamers[streamerid], theiters), 'r')
    text = f.read()
    getVideo(text, "%s%d" % (streamers[streamerid], theiters))
    print("download a clip!!!!!!")
    skip = 2
    pass

while True:
    test += 1
    for i in range(len(streamers)):
        readbuffers[i] = readbuffers[i] + sockets[i].recv(1024).decode('utf-8')
        temp = str.split(readbuffers[i], "\n")
        readbuffers[i] = temp.pop()

        for line in temp:
            if (line[0] == "PING"):
                sockets[i].send("PONG %s\r\n" % line[1])
            else:
                parts = str.split(line, ":")
                if "QUIT" not in parts[1] and "JOIN" not in parts[1] and "PART" not in parts[1]:
                    try:
                        message = parts[2][:len(parts[2]) - 1]
                    except:
                        message = ""
                    usernamesplit = str.split(parts[1], "!")
                    username = usernamesplit[0]
                    if MODT:
                        # print(username + ": " + message)
                        chats.append(username + ": " + message)
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

            if iters > 10 and counts[i] > avg*1.5 and skip <= 0:
                clip(i)
                avgss[i].append(counts[i]);
                skip = 4

            if skip < 2:
                avgss[i].append(counts[i]);
                chats = []
                if(len(avgss[i]) > 10):
                    avgss[i].pop()
            else:
                print("(skipperino)")
                skip -= 1;

            counts[i] = 0;
