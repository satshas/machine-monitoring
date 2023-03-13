#
# (c) Marcello Tania 13/03/23
#
# This work may be reproduced, modified, distributed,
# performed, and displayed for any purpose. Copyright is
# retained and must be preserved. The work is provided
# as is; no warranty is provided, and users accept all 
# liability.
#

import paho.mqtt.client as mqtt
from datetime import datetime
from tkinter import *
from  tkinter import ttk
import tkinter.font as tkFont
import csv
import re

global count_laser,count_cnc,count_printer
count_laser = 0
count_cnc = 0

# field names 
fields_state = ['Time', 'State'] 
fields_job = ['ID', 'Path', 'StartTime', 'EndTime'] 

with open('state_laserCutter.csv', 'w', newline='') as file: 
    writer = csv.DictWriter(file, fieldnames = fields_state)
    writer.writeheader() 

with open('state_cnc.csv', 'w', newline='') as file: 
    writer = csv.DictWriter(file, fieldnames = fields_state)
    writer.writeheader() 

with open('state_3dprinter.csv', 'w', newline='') as file: 
    writer = csv.DictWriter(file, fieldnames = fields_state)
    writer.writeheader() 

with open('job_laserCutter.csv', 'w', newline='') as file: 
    writer = csv.DictWriter(file, fieldnames = fields_job)
    writer.writeheader() 

with open('job_cncCutter.csv', 'w', newline='') as file: 
    writer = csv.DictWriter(file, fieldnames = fields_job)
    writer.writeheader() 

with open('job_3dprinter.csv', 'w', newline='') as file: 
    writer = csv.DictWriter(file, fieldnames = fields_job)
    writer.writeheader() 

def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)

    # Laser Cutter

    #If the received message is light on then set the image the the ‘light on’ image
    if message.topic == "inmachines/lasercutter/state":
        state = str(message.payload.decode("utf-8"))
        statusUpdateLaserLabel.configure(text=state)
        statusUpdateLaserLabel.update()

        # datetime object containing current date and time
        now = datetime.now()

        # data rows as dictionary objects 
        mydict =[{'Time': now, 'State': state}]

        with open('state_laserCutter.csv', 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames = fields_state)

            writer.writerows(mydict)

    if message.topic =="inmachines/lasercutter/filename":
        global path_name_laser
        path_name_laser = str(message.payload.decode("utf-8"))

        pattern = '[\w-]+?(?=\.)'
        # searching the pattern
        a = re.search(pattern, path_name_laser)
        fileUpdateNameLaserLabel.configure(text=a.group())
        fileUpdateNameLaserLabel.update()

    if message.topic =="inmachines/lasercutter/starttime":
        global start_time_laser
        start_time_laser = str(message.payload.decode("utf-8"))
        startTimeUpdateLaserLabel.configure(text=start_time_laser)
        startTimeUpdateLaserLabel.update()

    if message.topic =="inmachines/lasercutter/endtime":
        global count_laser
        end_time_laser = str(message.payload.decode("utf-8"))
        endTimeUpdateLaserLabel.configure(text=end_time_laser)
        endTimeUpdateLaserLabel.update()

        try:
            laser_id.insert(parent='',index='end', iid=count_laser ,text='',values=(count_laser,path_name_laser,start_time_laser,end_time_laser))
            
            laser_id.pack()

            # data rows as dictionary objects 
            mydict =[{'ID': count_laser, 'Path': path_name_laser, 'StartTime': start_time_laser, 'EndTime': end_time_laser}]

            with open('job_laserCutter.csv', 'a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames = fields_job)
                writer.writerows(mydict)

            count_laser += 1
        except:
            print("path name not define")

    if message.topic =="inmachines/lasercutter/power":
        power = round(float(message.payload.decode("utf-8"))*230,2)
        powerUpdateLaserLabel.configure(text=str(power)+" Watt")
        powerUpdateLaserLabel.update()


    #########
    # CNC
    ##########

    #If the received message is light on then set the image the the ‘light on’ image
    if message.topic == "inmachines/cnc/state":
        state = str(message.payload.decode("utf-8"))
        statusUpdateCncLabel.configure(text=state)
        statusUpdateCncLabel.update()

        # datetime object containing current date and time
        now = datetime.now()

        # data rows as dictionary objects 
        mydict =[{'Time': now, 'State': state}]

        with open('state_cnc.csv', 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames = fields_state)
            writer.writerows(mydict)

    if message.topic =="inmachines/cnc/filename":
        global path_name_cnc
        path_name_cnc = str(message.payload.decode("utf-8"))

        pattern = '[\w-]+?(?=\.)'
        # searching the pattern
        a = re.search(pattern, path_name_cnc)

        fileUpdateNameCncLabel.configure(text=a.group())
        fileUpdateNameCncLabel.update()

    if message.topic =="inmachines/cnc/starttime":
        global start_time_cnc
        start_time_cnc = str(message.payload.decode("utf-8"))

        startTimeUpdateCncLabel.configure(text=start_time_cnc)
        startTimeUpdateCncLabel.update()

    if message.topic =="inmachines/cnc/endtime":
        global count_cnc
        end_time_cnc = str(message.payload.decode("utf-8"))
        endTimeUpdateCncLabel.configure(text=end_time_cnc)
        endTimeUpdateCncLabel.update()

        try:

            cnc_id.insert(parent='',index='end', iid=count_cnc ,text='',values=(count_cnc,path_name_cnc,start_time_cnc,end_time_cnc))
            
            cnc_id.pack()

            # data rows as dictionary objects 
            mydict =[{'ID': count_cnc, 'Path': path_name_cnc, 'StartTime': start_time_cnc, 'EndTime': end_time_cnc}]

            with open('job_cncCutter.csv', 'a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames = fields_job)
                writer.writerows(mydict)

            count_cnc += 1
        except:
            print("path name not define")


    if message.topic =="inmachines/cnc/power":
        power = round(float(message.payload.decode("utf-8"))*230,2)
        powerUpdateCncLabel.configure(text=str(power)+" Watt")
        powerUpdateCncLabel.update()

    #############
    # 3D Printer
    #############

    #If the received message is light on then set the image the the ‘light on’ image
    if message.topic == "inmachines/3dprinter/state":
        state = str(message.payload.decode("utf-8"))
        statusUpdatePrinterLabel.configure(text=state)
        statusUpdatePrinterLabel.update()

        # datetime object containing current date and time
        now = datetime.now()

        # data rows as dictionary objects 
        mydict =[{'Time': now, 'State': state}]

        with open('state_3dprinter.csv', 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames = fields_state)

            writer.writerows(mydict)

    if message.topic =="inmachines/3dprinter/filename":
        global path_name_printer
        path_name_printer = str(message.payload.decode("utf-8"))

        pattern = '[\w-]+?(?=\.)'
        # searching the pattern
        a = re.search(pattern, path_name_printer)

        fileUpdateNamePrinterLabel.configure(text=a.group())
        fileUpdateNamePrinterLabel.update()

    if message.topic =="inmachines/3dprinter/starttime":
        global start_time_printer
        start_time_printer= str(message.payload.decode("utf-8"))

        startTimePrinterUpdateLabel.configure(text=start_time_printer)
        startTimePrinterUpdateLabel.update()

    if message.topic =="inmachines/3dprinter/endtime":
        global count_printer
        end_time_printer = str(message.payload.decode("utf-8"))
        endTimeUpdatePrinterLabel.configure(text=end_time_printer)
        endTimeUpdatePrinterLabel.update()

        try:
            printer_id.insert(parent='',index='end', iid=count_printer ,text='',values=(count_printer,path_name_printer,start_time_printer,end_time_printer))
            
            printer_id.pack()

            # data rows as dictionary objects 
            mydict =[{'ID': count_printer, 'Path': path_name_printer, 'StartTime': start_time_printer, 'EndTime': end_time_printer}]

            with open('job_laserCutter.csv', 'a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames = fields_job)
                writer.writerows(mydict)

            count_printer += 1
        except:
            print("path name not define")

    if message.topic =="inmachines/3dprinter/power":
        power = round(float(message.payload.decode("utf-8"))*230,2)
        powerUpdatePrinterLabel.configure(text=str(power)+" Watt")
        powerUpdatePrinterLabel.update()

broker_address= "pi-mqtt-server" # Update broker address
print("creating new instance")
client = mqtt.Client("P1") #create new instance
client.on_message=on_message #attach function to callback

try:
    print("connecting to broker")
    client.connect(broker_address) #connect to broker
except:
    print("unable to connect to broker")

# Laser cutter
client.subscribe("inmachines/lasercutter/state", qos=1)
client.subscribe("inmachines/lasercutter/filename", qos=1)
client.subscribe("inmachines/lasercutter/starttime", qos=1)
client.subscribe("inmachines/lasercutter/endtime", qos=1)
client.subscribe("inmachines/lasercutter/power")

# CNC
client.subscribe("inmachines/cnc/state", qos=1)
client.subscribe("inmachines/cnc/filename", qos=1)
client.subscribe("inmachines/cnc/starttime", qos=1)
client.subscribe("inmachines/cnc/endtime", qos=1)
client.subscribe("inmachines/cnc/power")

# 3D Printer
client.subscribe("inmachines/3dprinter/state", qos=1)
client.subscribe("inmachines/3dprinter/filename", qos=1)
client.subscribe("inmachines/3dprinter/starttime", qos=1)
client.subscribe("inmachines/3dprinter/endtime", qos=1)
client.subscribe("inmachines/3dprinter/power")

# root window
root = Tk()
def_font = tkFont.nametofont("TkDefaultFont")
def_font.config(size=24)
root['bg'] = '#AC99F2'

s=ttk.Style()
s.theme_use('clam')

# Add the rowheight
s.configure('Treeview', rowheight=40)


#getting screen width and height of display
width= root.winfo_screenwidth()
height= root.winfo_screenheight()
column_width = int(width/12)-25

#setting tkinter window size
root.geometry("%dx%d" % (width, height))
root.title("Inmachines: Micro Factory Monitor")

####################
# Laser Cutter Frame
####################

laserFrame = LabelFrame(root, text="Laser Cutter",font=("Verdana", 60), fg='black')
laserFrame.pack(side=LEFT, padx=30, pady=30)

laserFrame1 = Frame(laserFrame)
laserFrame1.pack()

# Create left and right frames
leftSideLaserFrame = Frame(laserFrame1)
leftSideLaserFrame.pack(side='left',  fill='both',  padx=10,  pady=5,  expand=True)

rightSideLaserFrame = Frame(laserFrame1)
rightSideLaserFrame.pack(side='right',  fill='both',  padx=10,  pady=5,  expand=True)

# State
statusLaserLabel = Label(leftSideLaserFrame, text="State :", fg='black')
statusLaserLabel.pack(padx=10, pady=10, anchor="e")

statusUpdateLaserLabel = Label(rightSideLaserFrame, fg='black')
statusUpdateLaserLabel.pack(padx=10, pady=10)


# Power
powerLaserLabel = Label(leftSideLaserFrame, text="Power :", fg='black')
powerLaserLabel.pack(padx=10, pady=10, anchor="e")


powerUpdateLaserLabel = Label(rightSideLaserFrame, fg='black')
powerUpdateLaserLabel.pack(padx=10, pady=10)


# Job ID

fileNameLaserLabel = Label(leftSideLaserFrame, text="File Name :", fg='black')
fileNameLaserLabel.pack(padx=10, pady=10, anchor="e")

fileUpdateNameLaserLabel = Label(rightSideLaserFrame, fg='black')
fileUpdateNameLaserLabel.pack(padx=10, pady=10)

startTimeLaserLabel = Label(leftSideLaserFrame, text="Start Time :", fg='black')
startTimeLaserLabel.pack(padx=10, pady=10, anchor="e")

startTimeUpdateLaserLabel = Label(rightSideLaserFrame, fg='black')
startTimeUpdateLaserLabel.pack(padx=10, pady=10)

endTimeLaserLabel = Label(leftSideLaserFrame, text="End Time :", fg='black')
endTimeLaserLabel.pack(padx=10, pady=10, anchor="e")

endTimeUpdateLaserLabel = Label(rightSideLaserFrame, fg='black')
endTimeUpdateLaserLabel.pack(padx=10, pady=10)

# Job ID Table

#scrollbar
jobIDlaserFrame = Frame(laserFrame)
jobIDlaserFrame.pack(padx=5, pady=10, anchor="center")

laser_scroll = Scrollbar(jobIDlaserFrame)
laser_scroll.pack(side=RIGHT, fill=Y)

laser_scroll = Scrollbar(jobIDlaserFrame,orient='horizontal')
laser_scroll.pack(side= BOTTOM,fill=X)

laser_id = ttk.Treeview(jobIDlaserFrame,yscrollcommand=laser_scroll.set, xscrollcommand =laser_scroll.set )

laser_id['columns'] = ('job_id','file_name', 'start_time', 'end_time')

laser_id.column("#0", width=0,  stretch=NO)
laser_id.column("job_id",anchor=CENTER, width=column_width)
laser_id.column("file_name",anchor=CENTER, width=column_width)
laser_id.column("start_time",anchor=CENTER, width=column_width)
laser_id.column("end_time",anchor=CENTER, width=column_width)

laser_id.heading("#0",text="",anchor=CENTER)
laser_id.heading("job_id",text="ID",anchor=CENTER)
laser_id.heading("file_name",text="Path",anchor=CENTER)
laser_id.heading("start_time",text="Start Time",anchor=CENTER)
laser_id.heading("end_time",text="End Time",anchor=CENTER)

laser_id.pack()

####################
# CNC Frame
####################

cncFrame = LabelFrame(root, text="CNC 3 Axis",font=("Verdana", 60), fg='black')
cncFrame.pack(side=LEFT, padx=30, pady=30)

cncFrame1 = Frame(cncFrame)
cncFrame1.pack()

# Create left and right frames
leftSideCncFrame = Frame(cncFrame1)
leftSideCncFrame.pack(side='left',  fill='both',  padx=10,  pady=5,  expand=True)

rightSideCncFrame = Frame(cncFrame1)
rightSideCncFrame.pack(side='right',  fill='both',  padx=10,  pady=5,  expand=True)

# State
statusCncLabel = Label(leftSideCncFrame, text="State :", fg='black')
statusCncLabel.pack(padx=10, pady=10, anchor="e")

statusUpdateCncLabel = Label(rightSideCncFrame, fg='black')
statusUpdateCncLabel.pack(padx=10, pady=10)

# Power
powerCncLabel = Label(leftSideCncFrame, text="Power :", fg='black')
powerCncLabel.pack(padx=10, pady=10, anchor="e")

powerUpdateCncLabel = Label(rightSideCncFrame, fg='black')
powerUpdateCncLabel.pack(padx=10, pady=10)

# Job ID

fileNameCncLabel = Label(leftSideCncFrame, text="File Name :", fg='black')
fileNameCncLabel.pack(padx=10, pady=10, anchor="e")

fileUpdateNameCncLabel = Label(rightSideCncFrame, fg='black')
fileUpdateNameCncLabel.pack(padx=10, pady=10)

startTimeCncLabel = Label(leftSideCncFrame, text="Start Time :", fg='black')
startTimeCncLabel.pack(padx=10, pady=10, anchor="e")

startTimeUpdateCncLabel = Label(rightSideCncFrame, fg='black')
startTimeUpdateCncLabel.pack(padx=10, pady=10)

endTimeCncLabel = Label(leftSideCncFrame, text="End Time :", fg='black')
endTimeCncLabel.pack(padx=10, pady=10, anchor="e")

endTimeUpdateCncLabel = Label(rightSideCncFrame, fg='black')
endTimeUpdateCncLabel.pack(padx=10, pady=10)

# Job ID Table

#scrollbar
jobIDCncFrame = LabelFrame(cncFrame, fg='black')
jobIDCncFrame.pack(padx=5, pady=10, anchor="center")

cnc_scroll = Scrollbar(jobIDCncFrame)
cnc_scroll.pack(side=RIGHT, fill=Y)

cnc_scroll = Scrollbar(jobIDCncFrame,orient='horizontal')
cnc_scroll.pack(side= BOTTOM,fill=X)

cnc_id = ttk.Treeview(jobIDCncFrame,yscrollcommand=cnc_scroll.set, xscrollcommand =cnc_scroll.set)

cnc_id['columns'] = ('job_id','file_name', 'start_time', 'end_time')

cnc_id.column("#0", width=0,  stretch=NO)
cnc_id.column("job_id",anchor=CENTER, width=column_width)
cnc_id.column("file_name",anchor=CENTER, width=column_width)
cnc_id.column("start_time",anchor=CENTER, width=column_width)
cnc_id.column("end_time",anchor=CENTER, width=column_width)

cnc_id.heading("#0",text="",anchor=CENTER)
cnc_id.heading("job_id",text="ID",anchor=CENTER)
cnc_id.heading("file_name",text="Path",anchor=CENTER)
cnc_id.heading("start_time",text="Start Time",anchor=CENTER)
cnc_id.heading("end_time",text="End Time",anchor=CENTER)

cnc_id.pack()

####################
# 3D Printer Frame
####################

printerFrame = LabelFrame(root, text="3D Printer",font=("Verdana", 60), fg='black')
printerFrame.pack(side=LEFT, padx=30, pady=30)

printerFrame1 = Frame(printerFrame)
printerFrame1.pack()

# Create left and right frames
leftSidePrinterFrame = Frame(printerFrame1)
leftSidePrinterFrame.pack(side='left',  fill='both',  padx=10,  pady=5,  expand=True)

rightSidePrinterFrame = Frame(printerFrame1)
rightSidePrinterFrame.pack(side='right',  fill='both',  padx=10,  pady=5,  expand=True)


# State
statusPrinterLabel = Label(leftSidePrinterFrame, text="State :", fg='black')
statusPrinterLabel.pack(padx=10, pady=10, anchor="e")

statusUpdatePrinterLabel = Label(rightSidePrinterFrame, fg='black')
statusUpdatePrinterLabel.pack(padx=10, pady=10)

# Power
powerPrinterLabel = Label(leftSidePrinterFrame, text="Power :", fg='black')
powerPrinterLabel.pack(padx=10, pady=10, anchor="e")


powerUpdatePrinterLabel = Label(rightSidePrinterFrame, fg='black')
powerUpdatePrinterLabel.pack(padx=10, pady=10)

# Job ID

fileNamePrinterLabel = Label(leftSidePrinterFrame, text="File Name :", fg='black')
fileNamePrinterLabel.pack(padx=10, pady=10, anchor="e")

fileUpdateNamePrinterLabel = Label(rightSidePrinterFrame, fg='black')
fileUpdateNamePrinterLabel.pack(padx=10, pady=10)

startTimePrinterLabel = Label(leftSidePrinterFrame, text="Start Time :", fg='black')
startTimePrinterLabel.pack(padx=10, pady=10, anchor="e")

startTimePrinterUpdateLabel = Label(rightSidePrinterFrame, fg='black')
startTimePrinterUpdateLabel.pack(padx=10, pady=10)

endTimePrinterLabel = Label(leftSidePrinterFrame, text="End Time :", fg='black')
endTimePrinterLabel.pack(padx=10, pady=10, anchor="e")

endTimeUpdatePrinterLabel = Label(rightSidePrinterFrame, fg='black')
endTimeUpdatePrinterLabel.pack(padx=10, pady=10)


# Job ID Table

#scrollbar

jobIDprinterFrame = Frame(printerFrame)
jobIDprinterFrame.pack(padx=5, pady=10, anchor="center")

printer_scroll = Scrollbar(jobIDprinterFrame)
printer_scroll.pack(side=RIGHT, fill=Y)

printer_scroll = Scrollbar(jobIDprinterFrame,orient='horizontal')
printer_scroll.pack(side= BOTTOM,fill=X)

printer_id = ttk.Treeview(jobIDprinterFrame,yscrollcommand=laser_scroll.set, xscrollcommand =laser_scroll.set)

printer_id['columns'] = ('job_id','file_name', 'start_time', 'end_time')

printer_id.column("#0", width=0,  stretch=NO)
printer_id.column("job_id",anchor=CENTER, width=column_width)
printer_id.column("file_name",anchor=CENTER, width=column_width)
printer_id.column("start_time",anchor=CENTER, width=column_width)
printer_id.column("end_time",anchor=CENTER, width=column_width)

printer_id.heading("#0",text="",anchor=CENTER)
printer_id.heading("job_id",text="ID",anchor=CENTER)
printer_id.heading("file_name",text="Path",anchor=CENTER)
printer_id.heading("start_time",text="Start Time",anchor=CENTER)
printer_id.heading("end_time",text="End Time",anchor=CENTER)

printer_id.pack()


client.loop_start() #Start the MQTT Mosquito process loop
root.mainloop()