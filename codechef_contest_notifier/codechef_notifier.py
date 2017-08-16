from bs4 import BeautifulSoup

import requests
import fileinput
import textwrap

import time
import notify2


site = "https://www.codechef.com/contests"

page = requests.get(site).text

soup = BeautifulSoup(page,"html5lib")

file = open("parseddata.txt", "wb")

for link in soup.find_all('tbody'):
    file.write(link.text.encode("UTF-8"))

file.close()

for line in fileinput.FileInput("parseddata.txt",inplace=1):
    if line.rstrip():
        print textwrap.dedent(line)

ICON_PATH = "/home/hasan/codechef_contest_notifier/news_icon.png"
notify2.init("Contest Notifier")
# create Notification object
n = notify2.Notification(None, icon = ICON_PATH)
# set urgency level
n.set_urgency(notify2.URGENCY_NORMAL)
# set timeout for a notification
n.set_timeout(10000)

present = 0
future = 0
present_contest=[]
future_contest=[]

Present_Contest = []
Future_Contest = []

with open('parseddata.txt','rw') as file:
    for line in file:
        l = len(line)
        if line=='Past Contests\n':
            present = 0
            future = 0
            break
        elif (line== 'Future Contests\n' or future==1) and line!='\n':
            present=0
            future=1
            future_contest.append(line[:l-1])
        elif (line== 'Present Contests\n' or present==1) and line!='\n':
            present=1
            present_contest.append(line[:l-1])
def call(present_contest):
    len_contest = len(present_contest)
    i = 5
    Present_Contest = []
    while i < len_contest:
        contests = {}
        contests['NAME'] = present_contest[i + 1]
        s1 = "CODE = " + present_contest[i] + '\n'
        s2 = "START = " + present_contest[i + 2] + '\n'
        s3 = "END = " + present_contest[i + 3] + '\n'
        s = s1 + s2 + s3
        contests['Description'] = s
        i = i + 4
        Present_Contest.append(contests)
    return Present_Contest

n.update('Running Contests')
n.show()
time.sleep(5)

Present_Contest=call(present_contest)

for item in range(len(Present_Contest)):
    n.update(Present_Contest[item]['NAME'], Present_Contest[item]['Description'])
    n.show()
    time.sleep(10)
n.update('Upcoming Contests')
n.show()
time.sleep(5)

Future_Contest = call(future_contest)

for item in range(len(Future_Contest)):
    n.update(Future_Contest[item]['NAME'], Future_Contest[item]['Description'])
    n.show()
    time.sleep(10)