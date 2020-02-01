import requests
import json
import time
import sys
import os
import getpass
import urllib
from threading import Thread


# TODO: Make the client to wait every outputs until the server has responded with a terminate message
#       or take too much time (timeout)
# TODO: Add support to the file sending function of the server
# TODO: Optimize the code

server = "https://joprocorp.glitch.me/"
timeout = 15
timeexpire = timeout*5

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

def send(cmd, session_id):
    if not(check_session(session_id)):
        terminate()
    response = json.loads(download("input?session_id="+session_id+"&input="+cmd.replace('&', ';and;')))
    if(len(response)>0):
        if(response[0] == "ERROR"):
            if(response[2] == "Command registration failed."):
                #print("Trying to send the command again...")
                send(cmd, session_id)
            print("\nAn error occured: "+response[2])
            return
        if(response[0] == "GRANTED"):
            input_id = response[2]
            #doPrint("Command sent to the central server referenced (id:"+input_id+")")
            i = 0
            complete = False
            sent = False
            while(complete == False):
                # Vérifie si la commande est arrivée sur le serveur de destination
                download_response = download("checkinput?session_id="+session_id+"&input_id="+input_id)
                if not(download_response == []):
                    response = json.loads(download_response)
                    if(len(response)>0):
                        if(response[1] == "SENT" and sent == False):
                            #doPrint("Command arrived to destination server with success")
                            sent = True

                download_response = download("getoutput?session_id="+session_id)
                if not(download_response == []):
                    response = json.loads(download_response)
                    if(len(response)>0):
                        complete = True
                        if(response[0]['output'] == ""):
                            print('The server has responded with a null object string text.')
                            print('This means either :\n - An error occured\n - The ouput can\'t or failed to be sent\n - There is no output to be displayed.')
                        else:
                            response_output = response[0]['output']
                            print(urllib.parse.unquote(response_output).replace(';quote;', '"').replace(';and;', '&'))
                i = i+1

                if(i == 5):
                    if (sent):
                        print('The command reached the server but the server seems')
                        print('to take a lot of time to respond. This may be caused by :')
                        print(' - Execution issue')
                        print(' - Connection problem')
                        print(' - Server issues')
                    else:
                        print('WARN: The command seems to have trouble reaching the destination server.')
                    print('\n')

                if(i > timeout):
                    print('The command didn\'t received any output from the server in the timeout set.')
                    print('Either this is a server error or a connection error.')
                    if not(sent):
                        print('WARN: The command did not reached the destination server.')
                        print('      Check your connection to the server or try to login again.')
                        print('      Maybe the server crashed. Contact the system admin for more details.')
                    print('\n')

                    sent_status = "Unknown"
                    if(sent):
                        sent_status = "Received"
                    else:
                        sent_status = "Not received"
                    print("We will investigate this failure as soon as possible")
                    print('=================== FAIL REPORT ====================')
                    print(' SESSION STATUS           : '+check_session_reason(session_id))
                    print(' REQUEST STATUS (central) : Sent')
                    print(' REQUEST STATUS (dest)    : '+sent_status)
                    print('====================================================')
                    print(" SESSION ID : "+session_id)
                    print(" INPUT ID   : "+input_id)
                    print('====================================================')

                    complete = True
                if not(check_session(session_id)):
                    doPrint('Your session ID is no longer valid.')
                    doPrint('Reason: ' + check_session_reason(session_id))
                    terminate()
                #if(complete == False):
                #    time.sleep(1)
        else:
            doPrint('The command has been denied.')
            doPrint('Reason: ' + response[1])
            return
    else:
        doPrint('Something went wrong.')
        terminate()

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

def logout(session_id):
    download("logout?session_id="+session_id)

def login():
    user = doInput('Username:')
    pwd = doPass('Password:')
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
            doPrint("Access "+response[0]+" for this reason: " + response[1])
            terminate()
    else:
        doPrint("Something went wrong.")
        terminate()

def doPass(toPrint):
    type = "INFO"
    print("["+type+"]["+time.strftime("%H:%M:%S", time.localtime())+"] "+toPrint+" >> ")
    return getpass.getpass("")

def doPrint(toprint):
    type = "INFO"
    print("["+type+"]["+time.strftime("%H:%M:%S", time.localtime())+"] "+toprint)

def doInput(toPrint):
    type = "INFO"
    print("["+type+"]["+time.strftime("%H:%M:%S", time.localtime())+"] "+toPrint+" >> ", end = '')
    return input()

class check_session_while_waiting(Thread):

    """Thread chargé simplement d'afficher une lettre dans la console."""

    def __init__(self, session_id):
        Thread.__init__(self)
        self.session_id = session_id

    def run(self):
        """Code à exécuter pendant l'exécution du thread."""
        running=True
        while (running):
            time.sleep(3)
            response = json.loads(download("check_session?session_id="+session_id))
            if(len(response)>0):
                if(response[0] != "GRANTED"):
                    print("\nAccess terminated: "+response[1])
                    print("Press ENTER to terminate the remote console if it is not terminated.")
                    running = False




# Main section
doPrint(" ____     ___  ___ ___   ___   ______    ___ ")
doPrint("|    \   /  _]|   |   | /   \ |      |  /  _]")
doPrint("|  D  ) /  [_ | _   _ ||     ||      | /  [_ ")
doPrint("|    / |    _]|  \_/  ||  O  ||_|  |_||    _]")
doPrint("|    \ |   [_ |   |   ||     |  |  |  |   [_ ")
doPrint("|  .  \|     ||   |   ||     |  |  |  |     |")
doPrint("|__|\_||_____||___|___| \___/   |__|  |_____|")
doPrint("=============================================")
session_id = "null"
if(os.path.exists('session_id.log')):
    file = open('session_id.log', 'r').read()
    if(file != ""):
        doPrint('Trying previous session ID : "'+file+'"')
        if(check_session(file)):
            session_id = file
        else:
            doPrint('Please login with your credentials:')

if(session_id == "null"):
    session_id = login()
    if(os.path.exists('session_id.log')):
        os.remove('session_id.log')
    file = open('session_id.log', 'a')
    file.write(session_id)
    file.close()

doPrint('Actual session id : "'+session_id+'" saved')
doPrint('To leave the remote console, type "quit remote".\n')
doPrint('NOTE: Sessions inactive for 5 minutes will be considered expired.')
doPrint('They will be removed and their access will be terminated.\n')

# Création des threads
thread_1 = check_session_while_waiting(session_id)

# Lancement des threads
thread_1.start()

command = doInput("Cmd:")
while(command != "quit remote"):
    send(command, session_id)
    print("")
    command = doInput("Cmd:")
logout(session_id)

# Attend que les threads se terminent
thread_1.join()

terminate()