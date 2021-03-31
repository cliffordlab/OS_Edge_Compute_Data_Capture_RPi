#!/usr/bin/env python3
"""
Author: Pradyumna Byppanahalli Suresha (alias Pradyumna94)
Last Modified: Apr 29th, 2020

License:

BSD-3 License

Copyright [2020] [Clifford Lab]

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation and/or
other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors
may be used to endorse or promote products derived from this software without
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
from tkinter import  Tk, Label,  Button, StringVar, Entry, messagebox
from datetime import datetime

# The GUI class
class mpopup:
	def __init__(self, mmaster):
		""" Initialization """
		self.mmaster = mmaster
		mmaster.title("Auto Record - Set Timer")

		self.mlabel0 = Label(mmaster, text="Auto Record Menu")
		self.mlabel0.grid(row = 0, columnspan = 8)

		self.mlabel1 = Label(mmaster, text="Start Time ([HH:MM:SS:(AM/PM)]) ([00,11]:[00:59],[00:59],{AM,PM})", bg="yellow", )
		self.mlabel1.grid(row=1, columnspan = 8)

		self.mlabel1hr = Label(mmaster,text="Hr:")
		self.mlabel1hr.grid(row=2,column=0,columnspan = 2)

		self.mlabel1min = Label(mmaster,text=":M:")
		self.mlabel1min.grid(row=2,column=2,columnspan = 2)

		self.mlabel1sec = Label(mmaster,text=":S:")
		self.mlabel1sec.grid(row=2,column=4,columnspan = 2)

		self.mlabel1ap = Label(mmaster,text="AM/PM")
		self.mlabel1ap.grid(row=2,column=6,columnspan = 2)

		self.mlabel2 = Label(mmaster, text="End Time", bg="yellow")
		self.mlabel2.grid(row=4, columnspan = 8)

		self.mlabel2hr = Label(mmaster,text="Hr:")
		self.mlabel2hr.grid(row=5,column=0,columnspan = 2)

		self.mlabel2min = Label(mmaster,text=":M:")
		self.mlabel2min.grid(row=5,column=2,columnspan = 2)

		self.mlabel2sec = Label(mmaster,text=":S:")
		self.mlabel2sec.grid(row=5,column=4,columnspan = 2)

		self.mlabel2ap = Label(mmaster,text="AM/PM")
		self.mlabel2ap.grid(row=5,column=6,columnspan = 2)

		def focus_next_window(event):
			event.widget.tk_focusNext().focus()
			return("break")

		def callback(sv):
			c = sv.get()[0:1]
			#print("c=",c)
			sv.set(c)

		def callback2(sv):
			c = sv.get()[0:2]
			#print("c=",c)
			sv.set(c)
				
		self.sv1 = StringVar()
		self.sv1.trace("w", lambda name, index, mode, sv1=self.sv1: callback(self.sv1))
		self.sv1.set("0")        
		self.mbeghr1 = Entry(mmaster,  width=1, textvariable=self.sv1)
		self.mbeghr1.grid(row = 3, column = 0)
		self.mbeghr1.bind("<Tab>", focus_next_window)

		self.sv2 = StringVar()
		self.sv2.trace("w", lambda name, index, mode, sv2=self.sv2: callback(self.sv2))
		self.sv2.set("6")  
		self.mbeghr2 = Entry(mmaster,  width=1 , textvariable=self.sv2)
		self.mbeghr2.grid(row = 3, column = 1)
		self.mbeghr2.bind("<Tab>", focus_next_window)

		self.sv3 = StringVar()
		self.sv3.trace("w", lambda name, index, mode, sv3=self.sv3: callback(self.sv3))
		self.sv3.set("0")  
		self.mbegmin1 = Entry(mmaster,  width=1, textvariable=self.sv3)
		self.mbegmin1.grid(row = 3, column = 2)
		self.mbegmin1.bind("<Tab>", focus_next_window)

		self.sv4 = StringVar()
		self.sv4.trace("w", lambda name, index, mode, sv4=self.sv4: callback(self.sv4))
		self.sv4.set("0")  
		self.mbegmin2 = Entry(mmaster,  width=1, textvariable=self.sv4)
		self.mbegmin2.grid(row = 3, column = 3)
		self.mbegmin2.bind("<Tab>", focus_next_window)

		self.sv5 = StringVar()
		self.sv5.trace("w", lambda name, index, mode, sv5=self.sv5: callback(self.sv5))
		self.sv5.set("0")          
		self.mbegsec1 = Entry(mmaster,  width=1, textvariable=self.sv5)
		self.mbegsec1.grid(row = 3, column = 4)
		self.mbegsec1.bind("<Tab>", focus_next_window)

		self.sv6 = StringVar()
		self.sv6.trace("w", lambda name, index, mode, sv6=self.sv6: callback(self.sv6))
		self.sv6.set("0")          
		self.mbegsec2 = Entry(mmaster,  width=1, textvariable=self.sv6)
		self.mbegsec2.grid(row = 3, column = 5)
		self.mbegsec2.bind("<Tab>", focus_next_window)

		self.sv7 = StringVar()
		self.sv7.trace("w", lambda name, index, mode, sv7=self.sv7: callback2(self.sv7))
		self.sv7.set("PM")          
		self.mbegap = Entry(mmaster,  width=2, textvariable=self.sv7)
		self.mbegap.grid(row = 3, column = 6,columnspan=2)
		self.mbegap.bind("<Tab>", focus_next_window)

		self.sv8 = StringVar()
		self.sv8.trace("w", lambda name, index, mode, sv8=self.sv8: callback(self.sv8))        
		self.sv8.set("0")  
		self.mendhr1 = Entry(mmaster,  width=1, textvariable=self.sv8)
		self.mendhr1.grid(row = 6, column = 0)
		self.mendhr1.bind("<Tab>", focus_next_window)

		self.sv9 = StringVar()
		self.sv9.trace("w", lambda name, index, mode, sv9=self.sv9: callback(self.sv9))
		self.sv9.set("9")  
		self.mendhr2 = Entry(mmaster,  width=1, textvariable=self.sv9)
		self.mendhr2.grid(row = 6, column = 1)
		self.mendhr2.bind("<Tab>", focus_next_window)

		self.sv10 = StringVar()
		self.sv10.trace("w", lambda name, index, mode, sv10=self.sv10: callback(self.sv10))        
		self.sv10.set("0")  
		self.mendmin1 = Entry(mmaster,  width=1, textvariable=self.sv10)
		self.mendmin1.grid(row = 6, column = 2)
		self.mendmin1.bind("<Tab>", focus_next_window)

		self.sv11 = StringVar()
		self.sv11.trace("w", lambda name, index, mode, sv11=self.sv11: callback(self.sv11))
		self.sv11.set("0")  
		self.mendmin2 = Entry(mmaster,  width=1, textvariable=self.sv11)
		self.mendmin2.grid(row = 6, column = 3)
		self.mendmin2.bind("<Tab>", focus_next_window)

		self.sv12 = StringVar()
		self.sv12.trace("w", lambda name, index, mode, sv12=self.sv12: callback(self.sv12))        
		self.sv12.set("0")  
		self.mendsec1 = Entry(mmaster,  width=1, textvariable=self.sv12)
		self.mendsec1.grid(row = 6, column = 4)
		self.mendsec1.bind("<Tab>", focus_next_window)

		self.sv13 = StringVar()
		self.sv13.trace("w", lambda name, index, mode, sv13=self.sv13: callback(self.sv13))        
		self.sv13.set("0")  
		self.mendsec2 = Entry(mmaster,  width=1, textvariable=self.sv13)
		self.mendsec2.grid(row = 6, column = 5)
		self.mendsec2.bind("<Tab>", focus_next_window)

		self.sv14 = StringVar()
		self.sv14.trace("w", lambda name, index, mode, sv14=self.sv14: callback2(self.sv14))        
		self.sv14.set("AM")  
		self.mendap = Entry(mmaster,  width=2, textvariable=self.sv14)
		self.mendap.grid(row = 6, column = 6,columnspan=2)
		self.mendap.bind("<Tab>", focus_next_window)

		self.msave_button = Button(mmaster, text="Save", command=self.message)
		self.msave_button.grid(row = 7, column = 0, columnspan=4)

		self.mclose_button = Button(mmaster, text="Close", command=mmaster.quit)
		self.mclose_button.grid(row = 7, column = 4, columnspan=4)
        
	def message(self):
		""" Message that pops up upon clicking Save """
		tt = ""
		try:
			beghr = int(self.sv1.get()+self.sv2.get())
		except ValueError:
			beghr = 6
			tt=tt+"Begin Hour should be a number between 01 and 12\n"

		try:
			begmin = int(self.sv3.get()+self.sv4.get())
		except ValueError:
			begmin = 0
			tt=tt+"Begin Minute should be a number between 00 and 59\n"
		
		try:
			begsec = int(self.sv5.get()+self.sv6.get())
		except ValueError:
			begsec = 0
			tt=tt+"Begin Second should be a number between 00 and 59\n"
		
		begap = self.sv7.get()

		try:
			endhr = int(self.sv8.get()+self.sv9.get())
		except ValueError:
			endhr = 0
			tt=tt+"End Hour should be a number between 01 and 12\n"
		
		try:
			endmin = int(self.sv10.get()+self.sv11.get())
		except ValueError:
			endmin = 0
			tt=tt+"End Minute should be a number between 00 and 59\n"
		
		try:
			endsec = int(self.sv12.get()+self.sv13.get())
		except ValueError:
			ebdsec = 0
			tt=tt+"End Second should be a number between 00 and 59\n"

		endap = self.sv14.get()

		if beghr>12 or beghr<1:
			tt=tt+"Begin hour is outside 01 and 12. Please input a number in between 01 and 12\n"
		
		if begmin>59:
			tt=tt+"Begin min is greater than 59. Please input a number in between 00 and 59\n"

		if begsec>59:
			tt=tt+"Begin sec is greater than 59. Please input a number in between 00 and 59\n"
		
		if endhr>12 or endhr<1:
			tt=tt+"End hour is outside 01 and 12. Please input a number in between 01 and 12\n"
		
		if endmin>59:
			tt=tt+"End min is greater than 59. Please input a number in between 00 and 59\n"
		
		if endsec>59:
			tt=tt+"End sec is greater than 59. Please input a number in between 00 and 59\n"

		if tt=="":
			tt=tt+"All good! Click Ok and then click Close to exit to main menu"
			with open('/home/pi/PIR-interface/codes/autorec_time_tracker','w') as f:
				f.write(str(beghr)+'\n'+str(begmin)+'\n'+str(begsec)+'\n'+begap+'\n'+str(endhr)+'\n'+str(endmin)+'\n'+str(endsec)+'\n'+endap+'\n')
				
		messagebox.showinfo("", tt)

""" Display GUI """
menu = Tk()
menu.geometry("{0}x{1}+0+0".format(menu.winfo_screenwidth(), menu.winfo_screenheight()))
my_menu= mpopup(menu)
menu.mainloop()
