__author__ = 'Tom'

import time
import winsound
from Tkinter import *

class Alarm:
    """ A simple Alarm Clock Tk demonstration """
    def __init__(self, root):
        """ Initialize new alarm clock GUI """
        self.frame = Frame(root, padx=10, pady=10)
        self.frame.pack()
        self.root = root
        self.alarm_set_counter = 0 # variable used to blink alarm when being set
        self.alarm_btn_press = 0 # a character index into self.alarm_set_times[0] use to change alarm time
        self.alarm_set_times = ["00:00", "  :  "]
        self.is_set_alarm = True # used to check if alarm has been set
        self.after_method = None
        self.add_current_time()
        self.add_alarm_time()
        self.add_number_panel()
        self.add_alarm_button()

    def add_current_time(self):
        """ Add label displaying current time """
        Label(self.frame, text="Current Time").grid(row=0, column=4)
        self.current_time = Label(self.frame, text=time.strftime("%H:%M:%S"))
        self.current_time.grid(row=1, column=4)
        self.current_time.after(200, self.tick) # change text to time every 200 ms

    def tick(self):
        """ Updates current time label. Play sound if alarm
         has been set. """
        alarm_time = time.strftime("%H:%M:%S")
        self.current_time.config(text=alarm_time)
        self.current_time.after(200, self.tick)
        if self.is_set_alarm and self.after_method: # enter here if alarm has been set
            if alarm_time[:-3] == self.alarm_set_times[0]: # play sound if alarm time is current time
                self.create_sound()
                self.is_set_alarm = False
                
    def create_sound(self):
        """ Play alarm clock .wav file """
        winsound.PlaySound("alarm_clock_1.wav", winsound.SND_ALIAS)

    def add_alarm_time(self):
        """ Add label for the alarm time """
        Label(self.frame, text="Alarm Time").grid(row=3, column=4)
        self.alarm = Label(self.frame, text=self.alarm_set_times[0])
        self.alarm.grid(row=4, column=4)

    def add_number_panel(self):
        """ Add buttons for setting the alarm """
        for i in range(9):
            Button(self.frame, text=(i + 1), command= lambda x = (i + 1):self.num_click_handler(x)).grid(row=(i / 3), column=(i % 3))
        Button(self.frame, text="0", command= lambda x = 0:self.num_click_handler(x)).grid(row=3, column=1)

    def num_click_handler(self, num):
        """ Event handler for button press """
        if not self.is_set_alarm:
            alarm_time = self.alarm_set_times[0]
            alarm_time = alarm_time[:self.alarm_btn_press] + str(num) + alarm_time[self.alarm_btn_press + 1:]
            self.alarm_set_times[0] = alarm_time
            self.alarm_btn_press += 2 if self.alarm_btn_press == 1 else 1  # move index past the semicolon
            if self.alarm_btn_press >= 5:  # numbers pressed 4 times
                self.alarm.after_cancel(self.after_method) # cancel alarm blink
                self.alarm.config(text=self.alarm_set_times[0]) # set alarm time
                self.alarm_btn_press = 0 # reset number of times number has been pressed
                self.is_set_alarm = True

    def add_alarm_button(self):
        """ Add button to set the alarm clock wake-up time """
        frame = Frame(self.root)
        frame.pack()
        Button(frame, text="Set Alarm Time", command=self.set_alarm_time).grid(row=5, column=1)

    def set_alarm_time(self):
        """ Make alarm time blink so the user knows it is being set """
        self.is_set_alarm = False
        self.after_method = self.alarm.after(500, self.blink)
    
    def blink(self):
        """ Recursive function used to blink the alarm
        when its time is being set """
        self.alarm.config(text=self.alarm_set_times[self.alarm_set_counter % 2])
        self.alarm_set_counter += 1
        self.after_method = self.alarm.after(500, self.blink)

if __name__ == '__main__':
    root = Tk()
    alarm = Alarm(root)
    root.mainloop()
