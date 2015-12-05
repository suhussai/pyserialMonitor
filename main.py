import curses

def displayValues():
    index = 0
    for ID, value in Values_To_Montior.iteritems():
        index += 1
        myscreen.addstr(index, 2, "%s: %d C" % (ID, value))
        
    myscreen.refresh()

# # pyserialMonitor

# # input
#  - String format: ID Value \n
#  - 

# # log
#  - Time, Value1, Value2, ...

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

logFile = "valuesMonitored"
myscreen = curses.initscr()

myscreen.border(0)
displayValues()

myscreen.getch()

Values_To_Montior["FCTEMP1"] = 25
displayValues()




myscreen.getch()
curses.endwin()

 

