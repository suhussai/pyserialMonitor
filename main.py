import curses
import time
import serial
import signal
import sys

#http://stackoverflow.com/questions/1112343/how-do-i-capture-sigint-in-python?lq=1
def signal_handler(signal, frame):            
    teardownCurses(curses)
    teardownSerial(ser)
    teardownFileHandler(fileHandler)
    sys.exit(0)

def setupSerial(portName, baudrate):
    # https://pyserial.readthedocs.org/en/latest/shortintro.html
    ser = serial.Serial()
    ser.baudrate = baudrate
    ser.port = portName
    #ser.timeout = 1
    ser.open()
    return ser

def displayValues(myscreen):
    # http://www.tuxradar.com/content/code-project-build-ncurses-ui-python#null
    myscreen.addstr(1, 2, "Values Monitored")
    index = 2
    for ID, value in Values_To_Montior.iteritems():
        index += 1
        myscreen.addstr(index, 4, "%s: %d" % (ID, int(value)))            
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
    if len(line) > 0:
        (ID, value) = line.split() # get id and value
        # http://www.tutorialspoint.com/python/python_dictionary.htm
        # http://stackoverflow.com/questions/3294889/iterating-over-dictionaries-using-for-loops-in-python
        if (Values_To_Montior.get(ID, None) is not None): 
            Values_To_Montior[ID] = value # update dict if necessary
            
    return Values_To_Montior

    

def setupFileHandler(fileName):
    #http://www.tutorialspoint.com/python/python_files_io.htm
    fileHandler = open(fileName, "w+")
    # FCTEMP2:-1, TANKPRES:-1, FCTEMP1:-1, AMTEMP2:-1, AMTEMP1:-1, ERROR:-1, FCPRES:-1, FCVOLT:-1, FCCURR:-1, CAPCURR:-1
    fileHandler.write("Time, FCTEMP2, TANKPRES, FCTEMP1, AMTEMP2, AMTEMP1, ERROR, FCPRES, FCVOLT, FCCURR, CAPCURR\n")
    return fileHandler
def teardownFileHandler(fileHandler):
    fileHandler.close()

def writeToLog(fileHandler, Values_To_Montior):
    #http://www.tutorialspoint.com/python/python_date_time.htm
    message = str(time.asctime(time.localtime(time.time()))) + " "
    for ID, value in Values_To_Montior.iteritems():
        message +=  "%d, " % (int(value))

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


#http://stackoverflow.com/questions/1112343/how-do-i-capture-sigint-in-python?lq=1
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGHUP, signal_handler)


refresh_rate = 3 # number of seconds to sleep before updating
logFile = "valuesMonitored"
ser = setupSerial("/dev/ttyACM0", 9600)
myscreen = setupCurses()
fileHandler = setupFileHandler(logFile)

while True:
    try: # https://docs.python.org/2/tutorial/errors.html
        Values_To_Montior = updateValues(ser, Values_To_Montior)
        displayValues(myscreen)
        writeToLog(fileHandler, Values_To_Montior)
        # http://www.tutorialspoint.com/python/time_sleep.htm
        time.sleep(refresh_rate) 
        # press Ctrl-C to get out of loop, 
        #SIGINT handler implemented
    except:
        teardownCurses(curses)
        teardownSerial(ser)
        teardownFileHandler(fileHandler)
        sys.exit(0)

#### Arduino Code
#### http://electronics.stackexchange.com/questions/87868/data-lost-writing-on-arduino-serial-port-overflow
# void setup(){
#   Serial.begin(9600);
# }

# void loop(){
#   Serial.println("FCTEMP2 20");   
#   Serial.flush();
#   delay(1000);
# }
