from datetime import datetime
import os

def test():
    print("Tools work! Hey!")

def notes(name_of_note : str, writing=False, content=""):
    pass

def getTime():
    now = datetime.now()
    
    current_time = now.strftime("%H:%M")

    return current_time

def getDate():
    now = datetime.now()
    
    current_date = now.strftime("%D")

    return current_date

def end_talk():
    global conversation_going
    conversation_going = False
