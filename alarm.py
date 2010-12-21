import math, time
import winsound
from Tkinter import *

class Alarm:
    def __init__(self, root):
        frame = Frame(root, padx=10, pady=10)
        frame.pack()
        Label(frame, text="Current Time").grid(row=0, column=4)
        self.curtime = Label(frame, text=time.strftime("%H:%M:%S"))
        self.curtime.grid(row=1, column=4)
        Label(frame, text="Alarm Time").grid(row=3, column=4)
        self.alarm_set_counter = 0
        self.alarm_btn_press = 0
        self.alarm_set_times = ["00:00", "  :  "]
        self.is_set_alarm = True
        self.after_method = None
        self.alarm = Label(frame, text=self.alarm_set_times[0])
        self.alarm.grid(row=4, column=4)
        for i in range(1, 10):
            Button(frame, text=i, command= lambda x = i:self.num_click_handler(x)).grid(row=int(math.ceil((i + 0.0) / 3)), column=(i - 1) % 3)
        Button(frame, text="0", command= lambda x = 0:self.num_click_handler(x)).grid(row=4, column=1)
        frame = Frame(root)
        frame.pack()
        Button(frame, text="Set Alarm Time", command=self.set_alarm_time).grid(row=5, column=1)
        self.curtime.after(200, self.tick)
        
    def num_click_handler(self, num):
        if not self.is_set_alarm:
            alarmtime = self.alarm_set_times[0]
            alarmtime = alarmtime[:self.alarm_btn_press] + str(num) + alarmtime[self.alarm_btn_press + 1:]
            self.alarm_set_times[0] = alarmtime
            self.alarm_btn_press += 2 if self.alarm_btn_press == 1 else 1 
            if self.alarm_btn_press >= 5:
                self.alarm.after_cancel(self.after_method)
                self.alarm.config(text=self.alarm_set_times[0])
                self.alarm_btn_press = 0
                self.is_set_alarm = True

    def tick(self):
    	alarm_time = time.strftime("%H:%M:%S")
        self.curtime.config(text=alarm_time)  
        self.curtime.after(200, self.tick)
        if self.is_set_alarm and self.after_method:
            if alarm_time[:-3] == self.alarm_set_times[0]:
            	self.create_sound()
            	self.is_set_alarm = False
    
    def set_alarm_time(self):
        self.is_set_alarm = False
        self.after_method = self.alarm.after(500, self.blink)
    
    def blink(self):
        self.alarm.config(text=self.alarm_set_times[self.alarm_set_counter % 2])
        self.alarm_set_counter += 1
        self.after_method = self.alarm.after(500, self.blink)
        
    def create_sound(self):
        winsound.PlaySound("alarm_clock_1.wav", winsound.SND_ALIAS)
        
root = Tk()
alarm = Alarm(root)
root.mainloop()
