__author__ = 'Tom'

import time
import pygame
from Tkinter import *
from datetime import datetime, timedelta

pygame.mixer.init()
alarm_sound = pygame.mixer.Sound('alarm_clock_1.wav')

class Alarm:
    """ A simple Alarm Clock Tk demonstration """
    def __init__(self, root):
        """ Initialize new alarm clock GUI """
        self.frame = Frame(root, padx=10, pady=10)
        self.frame.pack()
        self.root = root
        self.alarm_set_counter = 0
        self.alarm_btn_press = 0
        self.alarm_set_times = ["00:00", "  :  "]
        self.is_set_alarm = False
        self.is_alarm_being_set = False
        self.after_method = None
        self.add_current_time()
        self.add_alarm_time()
        self.add_number_panel()
        self.add_alarm_button()
        self.add_pomodoro_buttons()

    def add_current_time(self):
        """ Add label displaying current time """
        Label(self.frame, text="Current Time").grid(row=0, column=4)
        self.current_time = Label(self.frame, text=time.strftime("%H:%M:%S"))
        self.current_time.grid(row=1, column=4)
        self.current_time.after(200, self.tick)

    def tick(self):
        """ Updates current time label. Play sound if alarm
         has been set. """
        alarm_time = time.strftime("%H:%M:%S")
        self.current_time.config(text=alarm_time)
        self.current_time.after(200, self.tick)
        if self.is_set_alarm:
            if alarm_time[:-3] == self.alarm_set_times[0]:
                self.create_sound()
                self.is_set_alarm = False
                
    def create_sound(self):
        """ Play alarm clock .wav file """
        pygame.mixer.Sound.play(alarm_sound)
        pygame.mixer.music.stop()

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
        if self.is_alarm_being_set:
            alarm_time = self.alarm_set_times[0]
            alarm_time = alarm_time[:self.alarm_btn_press] + str(num) + alarm_time[self.alarm_btn_press + 1:]
            self.alarm_set_times[0] = alarm_time
            self.alarm_btn_press += 2 if self.alarm_btn_press == 1 else 1 
            if self.alarm_btn_press >= 5:
                self.alarm.after_cancel(self.after_method)
                self.alarm.config(text=self.alarm_set_times[0])
                self.alarm_btn_press = 0
                self.is_set_alarm = True
                self.is_alarm_being_set = False

    def add_alarm_button(self):
        """ Add button to set the alarm clock wake-up time """
        frame = Frame(self.root)
        frame.pack()
        Button(frame, text="Set Alarm Time", command=self.set_alarm_time).grid(row=5, column=1)

    def set_alarm_time(self):
        """ Make alarm time blink so the user knows it is being set """
        if not self.is_alarm_being_set:
            self.is_alarm_being_set = True
            self.after_method = self.alarm.after(500, self.blink)
        self.is_set_alarm = False
    
    def blink(self):
        """ Recursive function used to blink the alarm
        when its time is being set """
        if self.is_alarm_being_set:
            self.alarm.config(text=self.alarm_set_times[self.alarm_set_counter % 2])
            self.alarm_set_counter += 1
            self.after_method = self.alarm.after(500, self.blink)

    def add_pomodoro_buttons(self):
        frame = Frame(self.root)
        self.add_pomodoro_start(frame)
        self.add_pomodoro_break(frame)
        frame.pack()

    def add_pomodoro_start(self, frame):
        Button(frame, text='Start 25 min. Pomodoro', command=self.start_pomodoro).grid(row=6, column=1)

    def add_pomodoro_break(self, frame):
        Button(frame, text='Break Pomodoro', command=self.break_pomodoro).grid(row=7, column=1)

    def start_pomodoro(self):
        if self.is_alarm_being_set:
            self.alarm.after_cancel(self.after_method)
            self.is_alarm_being_set = False
        alarm_time = datetime.now() + timedelta(minutes=25)
        self.alarm_set_times[0] = alarm_time.strftime("%H:%M")
        self.alarm.config(text=self.alarm_set_times[0])
        self.alarm_btn_press = 0
        self.is_set_alarm = True

    def break_pomodoro(self):
        if self.is_alarm_being_set:
            self.alarm.after_cancel(self.after_method)
            self.is_alarm_being_set = False
        alarm_time = datetime.now() + timedelta(minutes=5)
        self.alarm_set_times[0] = alarm_time.strftime("%H:%M")
        self.alarm.config(text=self.alarm_set_times[0])
        self.alarm_btn_press = 0
        self.is_set_alarm = True        


if __name__ == '__main__':
    root = Tk()
    root.title('Alarm Clock')
    alarm = Alarm(root)
    root.mainloop()
