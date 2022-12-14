import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import askopenfile
from selenium import webdriver
from selenium.webdriver.common.by import By
from tkinter.messagebox import showinfo
import requests
from time import sleep
from os import system, path, makedirs, chdir
import os
import sys
import signal
from moviepy.editor import *

import undetected_chromedriver as uc


def verify(key):
    global score
    score = 0

    check_digit = key[2]
    check_digit_count = 0

    chuncks = key.split('-')
    for chunck in chuncks:
        if len(chunck) != 4:
            return False
        else:
            return True


def download():
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    options = uc.ChromeOptions()
    options.headless = True
    options.add_argument('--headless')
    driver = uc.Chrome(options=options)
    uagent = driver.execute_script("return navigator.userAgent;")
    headers['User-Agent'] = uagent
    url = "{}{}".format(baseurl, username)
    n = 0
    urls = []
    driver.get(url)
    driver.maximize_window()
    keeplooking = True
    vidurls = driver.find_elements(
        By.XPATH, "//div[contains(@class, 'DivWrapper')]/a")
    while keeplooking == True:
        prev_vidurls = len(vidurls)
        for vidurl in vidurls:
            h = vidurl.get_attribute('href')
            if h in urls:
                pass
            else:
                urls.append(h)
        driver.execute_script("window.scrollBy(0,document.body.scrollHeight);")
        sleep(3)
        vidurls = driver.find_elements(
            By.XPATH, "//div[contains(@class, 'DivWrapper')]/a")
        for vidurl in vidurls:
            h = vidurl.get_attribute('href')
            if h in urls:
                pass
            else:
                urls.append(h)
        print("Found " + str(len(vidurls)) + " videos.", end="\r")
        if prev_vidurls == len(vidurls):
            keeplooking = False
            n = len(vidurls)

        showinfo('Tiktok', 'Download started')

        chdir(filename)
        dirname = username[1:]
        makedirs(dirname, exist_ok=True)
        chdir(dirname)

        for url in urls:
            driver.get(url)
            sleep(5)
            title = driver.find_element(
                By.XPATH, "//span[contains(@class, 'SpanText')]").text
            title = title.replace('/', '\u2044')
            p = '{0:03d}'.format(n)
            title = p + '_' + title + '.mp4'
            print(title)
            title_len = len(title)
            if path.exists(title):
                pass
            else:
                if watermark:
                    vid = driver.find_element(By.XPATH, "//video")
                    url = vid.get_attribute("src")
                    video = requests.get(url, headers=headers)
                    with open(title, 'wb') as v:
                        v.write(video.content)
                else:
                    system('yt-dlp -q --no-warnings -o "{}" "{}"'.format(title, url))
            n = n - 1
        driver.quit()
        driver.quit()
    manipulation()
    showinfo('Tiktok', 'Starting video manipulation')


def manipulation():
    filelist = os.listdir(filename + '/' + username[1:])
    k = 0
    for i in filelist:
        clip = VideoFileClip(filename + '/' + username[1:] + '/' + i)
        if mirror == 1:
            clip = clip.fx(vfx.mirror_x)
        if contrast == 1:
            clip = clip.fx(vfx.colorx, 1.5)
        if crop == 1:
            clip = clip.fx(vfx.crop, x1=20, y1=20)
        clip.write_videofile(f'{filename}/../Manipulated/{k}.mp4')
        print(f'{i} Edited successfully')
        k += 1


def show_entry_fields():
    global username
    username = '@' + e1.get()
    download()

def browse_button():
    global filename
    filename = filedialog.askdirectory()
    folder_path.set(filename)


def print_selection():
    global contrast
    global crop
    global mirror
    contrast = var1.get()
    crop = var2.get()
    mirror = var3.get()


def signal_handler(signum, frame):
    try:
        driver.quit()
    except Exception:
        pass

    sys.exit(1)


key = input('Enter key: ')
if verify(key):
    master = tk.Tk()
    master.geometry("300x230")
    master.resizable(0, 0)
    master.title('Tiktok downloader')
    my_font1 = ('monospace', 14, 'bold')
    baseurl = "https://www.tiktok.com/"
    watermark = False
    headers = {}
    folder_path = tk.StringVar()
    tk.Label(master,
            text="Username ", font=my_font1).grid(row=0, pady=10, padx=10)
    tk.Label(master,
            text="Save Path", font=my_font1).grid(row=1, padx=10)
    button2 = tk.Button(text="Browse", command=browse_button, width=16, height=1)
    button2.grid(row=1, column=1)

    e1 = tk.Entry(master)
    e1.grid(row=0, column=1)

    tk.Button(master,
            text='Quit',
            command=master.quit).grid(row=7,
                                        column=0,
                                        sticky="NESW",
                                        pady=4,
                                        padx=10)
    tk.Button(master,
            text='Download', command=show_entry_fields).grid(row=7,
                                                            column=1,
                                                            sticky="NESW",
                                                            pady=4,
                                                            )

    var1 = tk.IntVar()
    var2 = tk.IntVar()
    var3 = tk.IntVar()

    text = tk.Label(master, text='Video Tools', font=my_font1).grid(
        row=3, column=0, columnspan=2, ipadx=50, pady=10)

    tk.Checkbutton(master, text="Contrast", variable=var1, font=(
        'Arial', 12), command=print_selection).grid(row=4, sticky=tk.W)
    tk.Checkbutton(master, text="Crop", variable=var2, font=(
        'Arial', 12), command=print_selection).grid(row=5, sticky=tk.W)
    tk.Checkbutton(master, text="Mirror", variable=var3, font=(
        'Arial', 12), command=print_selection).grid(row=6, sticky=tk.W)


    tk.mainloop()
    master.mainloop()
else:
    pass