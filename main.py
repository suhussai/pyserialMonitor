import curses
import time
import serial

def setupSerial(portName, baudrate):
    ser = serial.Serial()
    ser.baudrate = baudrate
    ser.port = portName
    ser.timeout = 1
    ser.open()
    if ser.is_open():
        print("NOT exiting!")
        return ser
    else:
        print("exiting!")
        exit(0)

def displayValues(myscreen):
    myscreen.addstr(1, 2, "Values Monitored")
    index = 2
    for ID, value in Values_To_Montior.iteritems():
        index += 1
        myscreen.addstr(index, 4, "%s: %d" % (ID, value))
        
    myscreen.refresh()

def setupCurses():
    myscreen = curses.initscr()

    myscreen.border(0)
    return myscreen

def teardownCurses(curses):
    curses.endwin()


def teardownSerial(ser):
    ser.close()


def updateValues(ser, Values_To_Montior):
    line = ser.readline() # read line    
    ID, value = line.split() # get id and value
    
    if (Values_To_Montior.get(ID, default = None) is not None): 
        Values_To_Montior[ID] = value # update dict if necessary
    else:
        return

def setupFileHandler(fileName):
    return open(fileName, "r+")

def teardownFileHandler(fileHandler):
    fileHandler.close()

def writeToLog(fileHandler):
    message = round(time.time()) + " "
    for ID, value in Values_To_Montior.iteritems():
        message +=  "%s: %d" % (ID, value)

    message += "\n"
    fileHandler.write(message)

Values_To_Montior = {
    "FCTEMP1" : -1,
    "FCTEMP2" : -1,
    "AMTEMP1" : -1,
    "AMTEMP2" : -1,
    "ERROR" : -1,
    "FCVOLT" : -1,
    "FCCURR" : -1,
    "CAPCURR" : -1,
    "TANKPRES" : -1,
    "FCPRES" : -1
}

refresh_rate = 10 # number of seconds to sleep before updating

# # log
#  - Time, Value1, Value2, ...

logFile = "valuesMonitored"
ser = setupSerial("/dev/ttyS29", 9600)
myscreen = setupCurses()
fileHandler = setupFileHandler(logFile)

while 1:
    updateValues(ser, Values_To_Montior)
    displayValues(myscreen)
    writeToLog(fileHandler)
    time.sleep(refresh_rate)

teardownCurses(curses)
teardownSerial(ser)
teardownFileHandler(fileHandler)
