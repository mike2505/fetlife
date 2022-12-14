from selenium import webdriver
from selenium.webdriver.common.by import By

import tkinter as tk
import time
import undetected_chromedriver as uc

headless = 0

def follow(user, password, user_toFollow, headless, count):
    options = uc.ChromeOptions()
    if headless:
        options.headless = True
        options.add_argument('--headless')
    driver = uc.Chrome(options=options)

    driver.get('https://fetlife.com/users/sign_in')
    driver.find_element(By.XPATH, '//*[@id="user_login"]').send_keys(user)
    driver.find_element(
        By.XPATH, '//*[@id="user_password"]').send_keys(password)
    driver.find_element(
        By.XPATH, '/html/body/div[3]/div/div[3]/div/main/div/div[1]/form/div[2]/button').click()

    driver.get(f'https://fetlife.com/search?q={user_toFollow}')
    try:
        driver.find_element(
            By.XPATH, '/html/body/div[3]/div/form/div/div/main/div/div/div/div').click()
    except:
        driver.find_element(
            By.XPATH, '/html/body/div[3]/div/form/div/div/main/div/div/div[1]/div[1]').click()

    try:
        user_id = driver.current_url.split('/')[-1].split('?')[0]
    except:
        user_id = driver.current_url.split('/')[-1]

    driver.get(f'https://fetlife.com/users/{user_id}/followers')

    for i in range(1000):
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")

    k = 1
    time.sleep(1)

    for i in driver.find_elements(By.XPATH, "//button[text()='Follow']"):
        try:
            i.click()
            k += 1
            if k == count:
                break
            time.sleep(0.5)
        except:
            pass
    driver.quit()



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

def print_selection():
    global headless
    headless = var1.get()

def show_entry_fields():
    global username
    global password
    global user
    global count
    username = e1.get()
    password = e2.get()
    user = e3.get()
    count = e4.get()
    follow(username, password, user, headless, count)

key = input('Enter key: ')
if verify(key):
    master = tk.Tk()
    master.geometry("275x200")
    master.resizable(0, 0)
    master.title('FetLife Follow Bot')
    my_font1 = ('monospace', 14, 'bold')
    baseurl = "https://www.tiktok.com/"
    watermark = False
    headers = {}
    folder_path = tk.StringVar()
    tk.Label(master,
             text="Username ", font=my_font1).grid(row=0, pady=5, padx=5)
    tk.Label(master,
             text="Password ", font=my_font1).grid(row=1, pady=5, padx=5)
    tk.Label(master,
             text="User", font=my_font1).grid(row=2, pady=5, padx=5)
    tk.Label(master,
             text="Count", font=my_font1).grid(row=3, pady=5, padx=5)

    var1 = tk.IntVar()

    tk.Checkbutton(master, text="Headless", variable=var1, font=(
        'Arial', 12), command=print_selection).grid(row=4, sticky=tk.W)


    e1 = tk.Entry(master)
    e2 = tk.Entry(master)
    e3 = tk.Entry(master)
    e4 = tk.Entry(master)

    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)
    e3.grid(row=2, column=1)
    e4.grid(row=3, column=1)

    tk.Button(master,
              text='Quit',
              command=master.quit).grid(row=5,
                                        column=0,
                                        sticky="NESW",
                                        pady=4, padx=5)
    tk.Button(master,
              text='Follow',
              command=show_entry_fields).grid(row=5,
                                        column=1,
                                        sticky="NESW",
                                        pady=4,)
    tk.mainloop()
    master.mainloop()
else:
    pass
