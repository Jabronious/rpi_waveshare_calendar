from helpers.Image import draw_black, small_font, medium_font, large_font, epd, h_black_image, h_red_image
from datetime import datetime, timedelta
from calendar import month_abbr, day_name, mdays
import pandas
import gspread

days_dict = { 'Sunday': 0, 'Monday': 35, 'Tuesday': 75, 'Wednesday': 115, 'Thursday': 155, 'Friday': 195, 'Saturday': 235 }

def draw_calendar(width, height):
    today = datetime.today()
    draw_black.text((0, 0), month_abbr[today.month], font=large_font, fill=0)
    draw_black.text((200, 0), str(today.year), font=large_font, fill=0)
    draw_weekdays()
    draw_grid(width, height)
    draw_numbers(today)

def draw_weekdays():
    for key in days_dict.keys():
        draw_black.text((days_dict[key], 26), key[0:3], font=medium_font, fill=0)

def draw_grid(width, height):
    start_hor = 52
    start_vert = 32
    while start_vert < width:
        draw_black.line([(start_vert, start_hor), (start_vert, height)], fill=0, width=2)
        start_vert += 40
    while start_hor < height:
        draw_black.line([(0, start_hor), (width, start_hor)], fill=0, width=2)
        start_hor += 20

def draw_numbers(today):
    gc = gspread.service_account(filename='./client_secret.json')
    data = gc.open('daily_check').sheet1.get_all_values()
    headers = data.pop(0)
    dc_data = pandas.DataFrame(data, columns=headers)
    used_dates = dc_data['date'].tolist()
    date_to_draw = datetime(today.year, today.month, 1)
    row = 54
    while today.month == date_to_draw.month:
        draw_black.text((days_dict[day_name[date_to_draw.weekday()]], row), str(date_to_draw.day), font=small_font, fill=0)
        if date_to_draw.date().isoformat() in used_dates:
            draw_black.text((days_dict[day_name[date_to_draw.weekday()]] + 17, row), "©", font=small_font, fill=0)
        if day_name[date_to_draw.weekday()] == 'Saturday':
            row += 20
        date_to_draw = date_to_draw + timedelta(days=1)