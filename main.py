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
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains


@route('/')
def send_static2():
    # return ("?")
    return static_file("main.html", root='web/')

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

def getVideo(video_link, name):
    # soup = BeautifulSoup(html_doc, 'html.parser')
    # video_link = soup.video['src'][:-4]
    test=urllib.request.FancyURLopener()
    test.retrieve(video_link,name+".mp4")


def login(driver, username, password):
    driver.get("http://www.twitch.tv/user/login")
    elem_user = driver.find_element_by_id("username")
    elem_passwd = driver.find_element_by_name("password")
    elem_user.send_keys(username)
    elem_passwd.send_keys(password + Keys.RETURN)
    time.sleep(5)

def getClip(driver, channel_name,theiters):
    link = "twitch.tv/" + channel_name

    driver.get(link)

    mature_menu = driver.find_element_by_css_selector(".pl-mature-overlay")
    mature_accept = driver.find_element_by_css_selector(".player-content-button")
    ActionChains(driver).move_to_element(mature_menu).click(mature_accept).perform()

    menu = driver.find_element_by_css_selector(".player-menu")
    hidden_submenu = driver.find_element_by_css_selector(".pl-clips-button")
    ActionChains(driver).move_to_element(menu).click(hidden_submenu).perform()

    html = driver.page_source
    soup = BeautifulSoup(html, "html5lib")
    form = soup.find("form", {"class" : "js-create-clip-form"})
    broadcast_ID = soup.find("input", {"class" : "js-create-clip-broadcast_id"})['value']
    offset_time = soup.find("input", {"class" : "js-create-clip-offset"})['value']

    clip_url = "https://clips-media-assets.twitch.tv/raw_media/" + broadcast_ID + "-offset-" + offset_time + ".mp4"
    return clip_url


def clip(streamerid):
    global chats
    print("clipping")

    theiters = iters

    with open('%s%d.txt' % (streamers[streamerid], theiters), 'w') as outfile:
        json.dump(chats, outfile)

    username = "bungusbot2"
    password = "monkabot"
    channel_name = streamers[streamerid]

    driver = webdriver.Chrome()
    login(driver, username, password)
    clip_url = getClip(driver, channel_name,theiters)

    post = "js-create-clip-form"
    button_class = "pl-clips-button"

    # f=codecs.open(mov_path, 'r')
    # text = f.read()
    getVideo(clip_url, "%s%d" % (streamers[streamerid], theiters))

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
