# -*- coding: utf-8 -*-
"""
Completed 2/2/15

@author: Timothy Plummer
"""

from Tkinter import *
import os
import win32api
import datetime
import shutil

"""
A GUI that will allow the user to set up and stop a daysimeter with little hassle
"""
class Application(Frame):

    def __init__(self, master):
        """
        Initialize the Framework for the GUI
        Is run automatical when Application is called
        Creates the window, and calles create_interface to populate the text and buttons
        CALLED FROM : Application(automatic)
        CALLES: Applicaton.create_interface()
        """
        Frame.__init__(self, master)         #function to set up window
        self.grid()                          #function that fills the window, currently empty
        self.create_interface()              #call to create_interface on line 35


    def create_interface(self):
        """
        Populates the window created in Application.__init__ with information as needed
        will ask for the user to plug in their Daysimeter,and to click the "Search" button.
        the surch button will then call the function find.
        CALLED FROM : Application.__init__
        CALLES: find()
        """
        self.instructions = Label(self, anchor = "center", justify= "center") #text formatting
        self.instructions["text"] = "Welcome, please plug in your Daysimeter. \n\
When ready please click the search button.\n\
If there is an error please restart the program." #text for the user instructions printed in window
        self.instructions.grid()            #prints instructions on the window
        self.button = Button(self, text= "Search", command = self.find) #creates a button to call find find on line 54
        self.button.grid()                  #prints the button on the window

    def find(self):
        """
        When called this function will find the strings of all the drives that are active on the
        computer, except the C:\ drive because it is a reserved drive letter,and will look at each
        one for two files, "log_info.txt" and "data_log.txt". If these two are found there will
        be a check to see if the "log_info.txt" is less then or equal 1050 bytes (in case the
        file is 1024 or higher due to an error). if it is found it will copy the files to C:\\Daysimeter Files
        then ir will call edit, with the path  to "log_info.txt", if not it the search button
        remains and will allow the user to search again.
        CALLED FROM :Application.create_interface
        CALLES: Application.edit() with path to "log_info.txt"
        """
        now = datetime.datetime.now()        #gathers the current date and time
        year =str(now.year)                  #converts the year to a string
        yy= year[2:4]                        #takes the last two digits of year and uts them in yy
        if now.month <10:
            month= "0" +str(now.month)
        else:
            month = str(now.month)
        if now.day<10:
            day="0"+str(now.day)
        else:
            day= str(now.day)
        if now.hour<10:                      #if statement to correct for single digit hours
            if now.minute<10:                #if statement to correct for single digit minuets
                date=month+"-"+day+"-"+yy+" "+"0"+str(now.hour)+"0"+str(now.minute) #stores the date in the proper format
            else:
                date= month+"-"+day+"-"+yy+" "+"0"+str(now.hour)+str(now.minute)#stores the date in the proper format
        else:
            if now.minute<10:
                date= month+"-"+day+"-"+yy+" "+str(now.hour)+"0"+str(now.minute)#stores the date in the proper format
            else:
                date= month+"-"+day+"-"+yy+" "+str(now.hour)+str(now.minute)#stores the date in the proper format
        drives = win32api.GetLogicalDriveStrings()  #gets the strings for the active drives
        drives = drives.split('\000')[:-1]          #splits the strings out so they are usable
        self.instructions["text"] = "Searching"     #gives the user feedback so they know it is doing something
        for rootname in drives:                     #creates a loop to cycle through each drive one at a time
            if (rootname != "C:\\"):                #so that the program will not check the C:\ drive
                path1= rootname + "log_info.txt"    #creates a string with the possible path to the first test file
                path2= rootname + "data_log.txt"    #creates a string to the 2nd possible test file
                if (os.path.isfile(path1) & os.path.isfile(path2)): #tests to see if the files exists
                    storage = "C:\\Daysimeter Files"
                    if not os.path.isdir(storage):
                        os.makedirs(storage)
                    shutil.copy2(path1,storage+"\\"+date+" log_info.txt")
                    shutil.copy2(path2,storage+"\\"+date+" data_log.txt")
                    if (os.path.getsize(path1)<= 1050): #if they do check to see if "log_info.txt" is of the right size
                        self.instructions["text"]="Found, what would you like to do."   #if it up date the text to to tell the user
                        self.edit(path1)            #call to edit on line 80
            else:                                   #the Daysimeter does not exist if this line gets called
                self.instructions["text"]="Could not find the Daysimeter.\n\
   Make sure it is connected."                      #updates users instructions

    def edit(self, path):
        """
        This function will gather the information from the Daysimeter "log_info.txt" file and will read
        the first 7 lines of the file. then it will split based on the first line of the file. if it is a
        2 or 4 it will ask the user if they want to continue collecting data, or if they want to put the
        Daysimeter in to stand by mode. if the first line is a 0 it will ask the user if they want to
        start collecting data or keep the Daysimeter in stand by mode.
        CALLED FROM: Application.find with a path to the Daysimeter "log_info.txt" file
        CALLES:      Application.cont no inputs
                     Application.stop with the path to the log_info.txt and the input text
                     Application.start wiht the path to the log_info.txt and the input text
                     Application.noth no inputs
        """
        f = open(path, 'r')      #open the file for reading only
        fileText=f.readlines()   #reads all lines of the file and saves them as a list
        if (fileText[0] == "4\n" or fileText[0]=="2\n"):   #checks to see if the first line is a 2 or a 4
            self.button["text"]="Continue"       #updates the button text for user input
            self.button["command"]= self.cont    #changes the command of the button to call Application.cont on line 115
            self.button2 = Button(self, text = "Stop", command=lambda: self.stop(path, fileText))
                                                 #for line 97 creates a new button to call Application.Stop on line 128
            self.button2.grid(row= 2, column =1) #sets the location of button2 and prints it in the window
            self.button.grid(row=2, column = 0)  #sets the location of button and prints it in the window
        elif (fileText[0]=="0\n"):                    #first if failed, checks to see if the first line is a 0
            self.instructions["text"]="What would you like to do?"   #user instructions
            self.button["text"]="Start"          #updates the buttons text for user input
            self.button["command"]=lambda: self.start(path, fileText)    #updates button's command to call Application.start on line 147
            self.button2 = Button(self, text = "StandBy", command=self.noth) #updates button's command to call Application.noth on line
            self.button2.grid(row= 2, column =1) #reprints the new button2 updates
            self.button.grid(row=2, column = 0)  #reprints the new button updae

    def cont(self):
        """
        This function is called if the user's Daysimeter is about to start, or currently is collecting data
        it will not change anything in the "log_info.txt" file, and which allows the Daysimeter to
        go through its boot sequence if this is a start of a new data collection.
        CALLED FROM: Application.edit no inputs
        CALLES:      NONE
        Possible END OF PROGRAM
        """
        self.instructions["text"]="Complete, data collection will continue.\nPlease shut down this program." #user instructions
        self.button.grid_forget()    #removes button from the window
        self.button2.grid_forget()   #removes button2 from the window
        return                       #Possible END OF PROGRAM

    def stop(self, path, text):
        """
        This function will change "log_info.txt" first line from either a 2 or 4 to 0, and then save the
        changes.
        CALLED FROM: Applications.edit with a path to "log_info.txt" and a list of the text read from the file
        CALLES:      NONE
        Possible END OF PROGRAM
        """
        text[0]="0\n"            #changes the necessary values
        f=open(path,"w")         #opens the file "log_ingo.txt" for writing
        for i, line in enumerate(text):#a loop that allows us to look at all values of the list text
            f.write(line)           #writes text to "log_info.txt" one line at a time
        f.close()                #closes "log_info.txt"
        self.instructions["text"]="Complete, data collection stopped. \n Please shut down this program." #new users instructions 172
        self.button.grid_forget()#removes button
        self.button2.grid_forget()#removes button2
        return                   #Possible END OF PROGRAM.

    def start(self, path, text):
        """
        this function will create a warning to let the user know that if they start a new log then they
        will erase any data that may have been on the Daysimeter. it is up to the user to know if the
        data has been downloaded.
        CALLED FROM: Applications.edit with the path to "log_info.txt" and the text to be written to it
        CALLES:      Applications.noth no inputs
                 Applications.start_new with the path to "log_info.txt" and the text to be written to it
        """
        self.instructions["text"]="WARNING:\n Once started previous data will be removed."   #user instructions
        self.button["text"]="I understand"   #updates button text
        self.button2["text"]="Never mind"     #updates button2 text
        self.button2["command"]= self.noth   #allows button2 to call application.noth on line 172
        self.button["command"]=lambda: self.start_new(path, text)#allows button to call start_new with two inputs path and text
        self.button2.grid(row= 3, column =0) #prints button2 in the window
        self.button.grid(row=2, column = 0)  #prints button in the window
        return                               #Possible END OF PROGRAM

    def start_new(self, path, text):
        """
        This functions will set up the text so that when written to "log_info.txt" it will cause the Daysimeter
        to start collecting data in a new log.
        CALLED FROM: Application.start with the path to "log_info.txt" and the text to be written to it
        CALLES:      Application.timerSet with the path to "log_info.txt" and the text to be written to it
        """
        text[0]="2\n"                #replaces the data necessary
        self.timerSet(text, path)    #calls the function timerSet on line 183
        self.button.grid_forget()    #removes button

    def noth(self):
        """
        This function will not change any part of the file "log_info.txt"
        CALLED FROM: Applications.edit no inputs
        CALLES:      NONE
        Possible END OF PROGRAM
        """
        self.instructions["text"]="Data collection remained on StandBy.\n Please shut down this program."   #user instructions
        self.button.grid_forget()    #removes button
        self.button2.grid_forget()   #removes button2
        return                       #Possible END OF PROGRAM

    def timerSet(self,text,path):
        """
        this function will allow the user to set the Daysimeter "timer" by telling it how often to collect data.
        the user has a choice of one of :30, 60, 90, 120, 150, and 180 seconds.
        CALLED FROM: Applications.start_new with the path to "log_info.txt" and the text to be written to it
        CALLES:      Applications.update_file with the path to "log_info.txt" and the text to be written to it
        """
        self.instructions["text"]= "What interval should it gather data"  #user instructions
        self.getInterval = StringVar()   #a variable that stores the user input when the "submit" button is clicked
        self.thirty=Radiobutton(self, text="30 sec for 5.5 days", value="030\n", variable=self.getInterval)   #radio button for 30 sec
        self.thirty.grid(row=1,column=0)                                                         #prints radio button for 30 sec
        self.sixety=Radiobutton(self, text="60 sec for 11 days", value="060\n", variable=self.getInterval)   #radio button for 60 sec
        self.sixety.grid(row=2,column=0)                                                         #prints radio button for 60 sec
        self.ninety=Radiobutton(self, text="90 sec for 16.5 days", value="090\n", variable=self.getInterval)   #radio button for 90 sec
        self.ninety.grid(row=3,column=0)                                                         #prints radio button for 90 sec
        self.one_twenty=Radiobutton(self, text="120 sec for 22 days", value="120\n", variable=self.getInterval)#radio button for 120 sec
        self.one_twenty.grid(row=4,column=0)                                                     #prints radio button for 120 sec
        self.one_fifety=Radiobutton(self, text="150 sec for 27.5 days", value="150\n", variable=self.getInterval)#radio button for 150 sec
        self.one_fifety.grid(row=5,column=0)                                                     #prints radio button for 150 sec
        self.one_eighty=Radiobutton(self, text="180 sec for 33 days", value="180\n", variable=self.getInterval)#radio button for 180 sec
        self.one_eighty.grid(row=6,column=0)                                                     #prints radio button for 180 sec
        self.thirty.select()             #set up so only one value is active at one time
        self.button2["text"]="Submit"    #updates button2 text
        self.button2.grid(column = 1)    #prints button2
        self.button2["command"]=lambda: self.update_file(text,path)#allows button2 to call update_file with text and path

    def update_file(self, text, path):
        """
        this function will gather all of the data needed to start a Daysimeter, with the time that the
        computer is at when the user clicks submit from function Application.timerSet it will then print
        this information to the file and give the user some instructions.
        CALLED FROM: Application.timerSet with the path to "log_info.txt" and the text to be written to it
        CALLES:      NONE
        Possible END OF PROGRAM
        """
        text[3] = self.getInterval.get()     #sets the interval selected by the user from timerSet
        now = datetime.datetime.now()        #gathers the current date and time
        year =str(now.year)                  #converts the year to a string
        yy= year[2:4]                        #takes the last two digits of year and uts them in yy
        if now.month <10:
            month= "0" +str(now.month)
        else:
            month = str(now.month)
        if now.day<10:
            day="0"+str(now.day)
        else:
            day= str(now.day)
        if now.hour<10:                      #if statement to correct for single digit hours
            if now.minute<10:                #if statement to correct for single digit minuets
                date=month+"-"+day+"-"+yy+" "+"0"+str(now.hour)+":"+"0"+str(now.minute)+"\n" #stores the date in the proper format
            else:
                date= month+"-"+day+"-"+yy+" "+"0"+str(now.hour)+":"+str(now.minute)+"\n"#stores the date in the proper format
        else:
            if now.minute<10:
                date= month+"-"+day+"-"+yy+" "+str(now.hour)+":"+"0"+str(now.minute)+"\n"#stores the date in the proper format
            else:
                date= month+"-"+day+"-"+yy+" "+str(now.hour)+":"+str(now.minute)+"\n"#stores the date in the proper format
        text[2]=date                         #sets the date to be written to the file
        f=open(path,"w")                     #opens the file for writing
        for i, line in enumerate(text):         #a loop that allows us to look at all values of the list text
            f.write(line)                       #writes text to "log_info.txt" one line at a time
        f.close()                            #closes the file "log_info.txt"
        self.instructions["text"]="Data collection started.\n Please remove the Daysimeter \n\
        and close the program."              #users instructions
        self.button.grid_forget()            #removes button from window
        self.button2.grid_forget()           #removes button2 from window
        self.thirty.grid_remove()            #removes radio button from window
        self.sixety.grid_remove()            #removes radio button from window
        self.ninety.grid_remove()            #removes radio button from window
        self.one_twenty.grid_remove()        #removes radio button from window
        self.one_fifety.grid_remove()        #removes radio button from window
        self.one_eighty.grid_remove()        #removes radio button from window
        return                               #Possible END OF PRORGRAM
"""
Below are the commands that are run when the program is started. this creates an application object,
that allows the user to fill in the necessary information for the Daysimeter to start or stop as needed.
CALLES: Application with the root which creates the window.

"""
root = Tk()                 #function used by Tkinter to create the Window
root.title("Daysimeter Start-Stop")#Titles the Window
root.geometry("250x200")    #defines the size of the window (is set by how large the radio buttons list in timerSet gets)
app = Application(root)     #calls the Application class to create and fill the window
root.mainloop()             #Necessary function, allows the window to be displayed on the screen
""" ****END OF FILE **** NOTHING BELOW THIS LINE**** """
