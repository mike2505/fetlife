from tkinter import *
import random

root = Tk()
root.geometry("300x110")
root.resizable(0, 0)
def generate():
    key_label.delete(0, END)

    key = ''
    blob = ''
    ckeck_digit_count = 0
    aplhabet = 'abcdefghijklmnopqrstuvwxyz1234567890'.upper()

    while len(key) < 25:
        char = random.choice(aplhabet)
        key += char
        blob += char

        if len(blob) == 4:
            key += '-'
            blob = ''

    key = key[:-1]

    key_label.insert(0,key)

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

generate_button = Button(root, text='Generate', command=generate)
generate_button.pack(pady=10)

key_label = Entry(root, bd=0, width=30)
key_label.pack(pady=10,padx=50)

root.mainloop()
