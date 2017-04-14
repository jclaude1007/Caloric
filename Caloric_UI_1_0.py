""" GUI application that supports the Caloric device. """
# 4/10/2017 Initial release


import serial
import sys
from tkinter import *
import threading

port = "COM9"
baud = 115200
serBuffer = ""
comm = ""
packet = ""

ser = serial.Serial(port, baud, timeout=1)
 
class SerialComm(threading.Thread):
    def __init__(self):
        super().__init__()
        self._exit_event = threading.Event()

    def request_exit(self):
        self._exit_event.set()

    def run(self):
        print("starting thread")
        """ Read a packet with integer data from the device """

        # get the buffer from outside of this function
        global serBuffer 

        while not self._exit_event.is_set():
            c = ser.read() # attempt to read a character from Serial
           
            #was anything read?
            #debug if len(c) == 0:
                #debug break
                                   
            # check if character is start of packet
            if c == b'$':
                #c = '' # don't want returns. chuck it
                serBuffer = "" # empty the buffer
                                              
            elif c == b'#': # end of packet
                #self.mpsi_txt.delete(0.0,END)
                #self.mpsi_txt.insert(0.0, serBuffer
                packet = serBuffer
                print(packet)
                
            elif c == b'0':         #packet data, convert to string
                serBuffer += "0"
            elif c == b'1':
                serBuffer += "1"
            elif c == b'2':
                serBuffer += "2"
            elif c == b'3':
                serBuffer += "3"
            elif c == b'4':
                serBuffer += "4"
            elif c == b'5':
                serBuffer += "5"
            elif c == b'6':
                serBuffer += "6"
            elif c == b'7':
                serBuffer += "7"
            elif c == b'8':
                serBuffer += "8"
            elif c == b'9':
                serBuffer += "9"
            else:
                serBuffer += ""
                
        #debug root.after(10, readSerial(self)) #check serial again soon
 
    
class Application(Frame):
  
    """ GUI frame """
    def __init__(self, master):
        """ Initialize Frame. """
        super(Application, self).__init__(master)  
 
        self.teu_value = 128     #TEU power value
        self.flow_value = 128    #Air flow value
        self.teu_mode = StringVar()
        self.teu_mode.set(None)
        self.serBuffer = ""
        self.grid()
        self.create_widgets()   #build screen widgets
        self.open_serial()      #update serial port state
        #self.readSerial()       #initial read seral port

        self.serial_comm_thread = SerialComm()
        self.serial_comm_thread.start()
        
          
    def create_widgets(self):
        """ Create widgets to control device and display operational parameters """

        # create a row space (in row 1)
        Label(self,
              text = "       "
              ).grid(row = 1, column = 1, sticky = W)

        row1 = 2
        # create an air temp label and text display
        Label(self,
              text = "Air Temp (C): "
              ).grid(row = row1, column = 0, sticky = W)
        self.air_temp = Text(self, width = 5, height = 1, wrap = WORD)
        self.air_temp.grid(row = row1, column = 1, columnspan = 1, sticky = W)

        # create a column space
        Label(self,
              text = "       "
              ).grid(row = row1, column = 2, sticky = W)

        # create an TEU label and  text display
        Label(self,
              text = "TEU: "
              ).grid(row = row1, column = 3, sticky = W)

        self.teu_count = Text(self, width = 5, height = 1, wrap = WORD)
        self.teu_count.grid(row = row1, column = 4, columnspan = 1, sticky = W)

        
        # create Decrement TEU button
        Button(self,
               text = "<" ,
               command = self.decrement_teu
               ).grid(row = row1, column = 5, columnspan = 1, sticky = W)
       
              
       # create Increment TEU button
        Button(self,
               text = ">" ,
               command = self.increment_teu
               ).grid(row = row1, column = 6, columnspan = 1, sticky = W)


        # create a column space
        Label(self,
              text = "       "
              ).grid(row = row1, column = 7, sticky = W)

        # create an TEU Mode label
        Label(self,
              text = "TEU Mode: "
              ).grid(row = row1, column = 8, sticky = W)


        # create Heating radiobutton
        Radiobutton(self,
                    text = "Heating",
                    variable = self.teu_mode,
                    value = 1,
                    command = self.update_mode
                    ).grid(row = row1, column = 9, sticky = W)
                    
        # create Coolinging radiobutton
        Radiobutton(self,
                    text = "Cooling",
                    variable = self.teu_mode,
                    value = 0,
                    command = self.update_mode
                    ).grid(row = row1, column = 10, sticky = W)
   

        
        # create a row space (in row 2)
        Label(self,
              text = "       "
              ).grid(row = 3, column = 2, sticky = W)
        row2 = 4

        # create a heatsink label and text display
        Label(self,
              text = "Heatsink (C): "
              ).grid(row = row2, column = 0, sticky = W)

        self.hs_temp = Text(self, width = 5, height = 1, wrap = WORD)
        self.hs_temp.grid(row = row2, column = 1, columnspan = 1, sticky = W)

        # create a space
        Label(self,
              text = "       "
              ).grid(row = row2, column = 2, sticky = W)

        # create an flow label and  text display
        Label(self,
              text = "Flow: "
              ).grid(row = row2, column = 3, sticky = W)

        self.flow_count = Text(self, width = 5, height = 1, wrap = WORD)
        self.flow_count.grid(row = row2, column = 4, columnspan = 1, sticky = W)

        # create decrement flow button
        Button(self,
               text = "<",
               command = self.decrement_flow
               ).grid(row = row2, column = 5, columnspan = 1, sticky = W)

       # create increment flow button
        Button(self,
               text = ">",
               command = self.increment_flow
               ).grid(row = row2, column = 6, columnspan = 1, sticky = W)


        # create a row space (In row 4)
        Label(self,
              text = "       "
              ).grid(row = 5, column = 2, sticky = W)
        row3 = 6

       # create a baffle label and text display
        Label(self,
              text = "Baffle (C): "
              ).grid(row = row3, column = 0, sticky = W)
        self.baffle_temp = Text(self, width = 5, height = 1, wrap = WORD)
        self.baffle_temp.grid(row = row3, column = 1, columnspan = 1, sticky = W)

        # create a space
        Label(self,
              text = "       "
              ).grid(row = row3, column = 2, sticky = W)

        # create an pressure label and  text display
        Label(self,
              text = "mPSI: "
              ).grid(row = row3, column = 3, sticky = W)

        self.mpsi_txt = Text(self, width = 5, height = 1, wrap = WORD)
        self.mpsi_txt.grid(row = row3, column = 4, columnspan = 1, sticky = W)
        

        # create a row space (In row 4)
        Label(self,
              text = "       "
              ).grid(row = 7, column = 2, sticky = W)
        row4 = 8

       # create a baffle label and text display
        Label(self,
              text = "Serial Port: "
              ).grid(row = row4, column = 0, sticky = W)
        self.commport_txt = Text(self, width = 10, height = 1, wrap = WORD)
        self.commport_txt.grid(row = row4, column = 1, columnspan = 1, sticky = W)
        

    def decrement_teu(self):
        """ decrement TEU power level """
        if self.teu_value > 0:
            self.teu_value -= 1

        self.teu_count.delete(0.0,END)
        self.teu_count.insert(0.0,str(self.teu_value))    
   
    def increment_teu(self):
        """ increment TEU power level """
        if self.teu_value < 255:
            self.teu_value += 1

        self.teu_count.delete(0.0,END)
        self.teu_count.insert(0.0,str(self.teu_value))    

    def decrement_flow(self):
        """ decrement flow power level """
        if self.flow_value > 0:
            self.flow_value -= 1

        self.flow_count.delete(0.0,END)
        self.flow_count.insert(0.0,str(self.flow_value))    
   
    def increment_flow(self):
        """ increment flow power level """
        if self.flow_value < 255:
            self.flow_value += 1

        self.flow_count.delete(0.0,END)
        self.flow_count.insert(0.0,str(self.flow_value))   

    def update_mode(self):
        """ TEU hot or cold """
        #mode = self.teu_mode.get()
        self.mpsi_txt.delete(0.0,END)
        self.mpsi_txt.insert(0.0, self.teu_mode.get() )
    
        
    def open_serial(self):
        """ display serial port status """
        global comm
        if comm == "OPEN":
            self.commport_txt.delete(0.0, END)
            self.commport_txt.insert(0.0, ser.name + ' Open')
                   
        else:
            self.commport_txt.delete(0.0, END)
            self.commport_txt.insert(0.0, ' Closed')

                    
   
                  
# main
root = Tk()
root.title("Caloric User Interface Ver 1.0")
root.geometry("600x400")
app = Application(root)

#debug root.after(100, readSerial(self)) #check serial again soon

root.mainloop()
ser.close()
