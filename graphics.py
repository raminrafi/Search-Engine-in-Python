from tkinter import *

import PIL
from PIL import Image, ImageTk as tk

label=[]

def printResult():
    strr=""
    file = open("C:\\Users\\Ramin Rafi\\AIproject\\BM25.txt", "r", errors='ignore')
    while True:
        line= file.readlines()
        if not line:
            break

        sb = Scrollbar(root2)
        sb.pack(side=RIGHT, fill=Y)
        mylist = Listbox(root2,yscrollcommand=sb.set)
        for i in range(len(line)):
            strr = str(line[i])
            #label = Label(root2, text=strr)
            mylist.insert(END, strr)
            mylist.pack(side=LEFT, fill=BOTH,expand=True)
            i = i + 1


        # i=0
        # for i in range(len(line)):
        #     strr=str(line[i])
        #     label = Label(root2,text=strr)
        #     label.pack()
        #     print(line[i])
        #     i=i+1





root2 = Tk()
root2.title("My Search Engine")
root2.geometry("900x450")
root2.configure(bg='white')
root2.iconbitmap("C:\\Users\\Ramin Rafi\\AIproject\\Google.ico")
button = Button(root2, text="Show Result", command=printResult)
button.pack()
root2.mainloop()



# root = Tk()
# # root.title("My Search Engine")
# # root.geometry("900x450")
# # root.configure(bg='white')
# # root.iconbitmap("C:\\Users\\Ramin Rafi\\AIproject\\Google.ico")
# #
# #
# # try:
# #     temp = Image.open("googlee.png")
# #     width, height = temp.size
# #
# #     temp = temp.resize((int(width / 4), int(height / 4)))
# #     temp.save("new.png")
# # except IOError:
# #     pass
# #
# # img = PhotoImage(file="new.png")
# # label = Label(root, image = img,bg='white')
# # label.pack()
# #
# # name_var=StringVar()
# # name_var.set("")
# # name_entry = Entry(root, textvariable = name_var,font=('calibre',10,'normal'))
# # name_entry.pack()
# #
# #
# # sub_btn=Button(root,text = 'Submit', command = submit)
# # sub_btn.pack()
# #
# # root.mainloop()