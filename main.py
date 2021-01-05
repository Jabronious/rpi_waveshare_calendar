from flask import Flask
from helpers.epaper_calendar import draw_calendar
from helpers.Image import epd, h_black_image, h_red_image
from datetime import date
import gspread

from gpiozero import Button
# 5,6,13,19
btn1 = Button(5)
btn2 = Button(6)
btn3 = Button(13)
btn4 = Button(19)

def handleBtnPress(btn):
	pinNum = btn.pin.number
	switcher = {
		5: "1",
		6: "2",
		13: "3",
		19: "4"
	}
	msg = switcher.get(pinNum, "Error")

	gc = gspread.service_account(filename='./client_secret.json')
	sheet = gc.open('daily_check')
	sheet.sheet1.append_row([date.today().isoformat(), msg])
	print_to_display()

btn1.when_pressed = handleBtnPress
btn2.when_pressed = handleBtnPress
btn3.when_pressed = handleBtnPress
btn4.when_pressed = handleBtnPress

def print_to_display():
	epd.Clear()
	draw_calendar(epd.height, epd.width)
	epd.display(epd.getbuffer(h_black_image), epd.getbuffer(h_red_image))

app = Flask(__name__)

@app.route('/')
def refresh_screen():
	print_to_display()
	return 'Ok'