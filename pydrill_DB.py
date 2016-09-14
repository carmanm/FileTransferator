from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import stat
import datetime
import os
import time
import shutil
import file_transfer_mod
import sqlite3
     


class Transfer:

    def __init__(self, master):

        

        self.style = ttk.Style()

        self.style.configure("TFrame",
                             background ="lightblue"
                             )

        self.frame_header = ttk.Frame(master)
        self.frame_header.pack()
        
        ttk.Label(self.frame_header, text = "File Transferator", font = (30)).grid(row = 0, column = 1, pady = 20)

        master.configure(background = 'lightblue')
        master.title("Transfer File")

        self.tree_frame = ttk.Frame(master)
        self.tree_frame.pack()

        self.s_folder = ttk.Label(self.tree_frame, text = "Source Folder")
        self.d_folder = ttk.Label(self.tree_frame, text = "Destination Folder")
        self.t_folder = ttk.Label(self.tree_frame, text = "Previous Transfers")
        self.f_folder = ttk.Label(self.tree_frame, text = "Previous Transfer Files")
        self.s_folder.grid(row = 0, column = 0, pady = (10, 0))
        self.d_folder.grid(row = 0, column = 1, pady = (10,0))
        self.t_folder.grid(row = 0, column = 2, pady = (10,0))
        self.f_folder.grid(row = 0, column = 3, pady = (10,0))
        self.s_folder.config(width = 28)
        self.d_folder.config(width = 28)
        self.t_folder.config(width = 28)
        self.f_folder.config(width = 28)
        

        self.treeview = ttk.Treeview(self.tree_frame)
        self.treeview.grid(row = 1, column = 0, padx = 30, pady = (0,30))
        self.treeview.config(selectmode = 'none')
        
        self.treeview2 = ttk.Treeview(self.tree_frame)
        self.treeview2.grid(row = 1, column = 1, padx = 30, pady = (0,30))
        self.treeview2.config(selectmode = 'none')

        self.treeview3 = ttk.Treeview(self.tree_frame)
        self.treeview3.grid(row = 1, column = 2, padx = 30, pady = (0,30))
        
    
        
        self.treeview4 = ttk.Treeview(self.tree_frame)
        self.treeview4.grid(row = 1, column = 3, padx = 30, pady = (0,30))
        self.treeview4.config(selectmode = 'none')

        
        
        
        self.button_frame = ttk.Frame(master)
        self.button_frame.pack(side = LEFT)

        ttk.Button(self.button_frame, text = 'Browse Source', command = self.browseButton1).grid(row = 0, column = 0, padx = 90, pady = (10,30))
        
        ttk.Button(self.button_frame, text = 'Browse Destination', command = self.browseButton2).grid(row = 0, column = 1, padx = 70, pady = (10,30))
        
        ttk.Button(self.button_frame, text = 'TRANSFER', command = self.runTransfer).grid(row = 1, column = 0, columnspan = 2, pady = (0, 30))
        
        ttk.Button(self.button_frame, text = 'View Previous Transfer Files', command = self.treeviewClick).grid(row = 0, column = 3, padx = 70, pady = (10,30))

        self.initialLastTransfer()
        self.treeviewInsert()    
        
    def browseButton1(self):
        from tkinter import filedialog
        global select
        global dirs
        global dirs_name
        global true_path

        (self.treeview).delete(*self.treeview.get_children())
        
        self.select = filedialog.askdirectory()
        
        dirs = os.listdir(self.select)
        dirs_name = os.path.dirname(self.select)

        #treeview heading changes to current directory
        self.treeview.heading(column = "#0", text = self.select)

        
        
        for i, file in enumerate(dirs):
            print(self.select + "/" + file)
            true_path = self.select + "/" + file
            self.treeview.insert('', i, text = file)
            

    def browseButton2(self):
        global select2
        
        from tkinter import filedialog
        self.select2 = filedialog.askdirectory()

        #treeview heading changes to current directory
        self.treeview2.heading(column = "#0", text = self.select2)

    
    
    def runTransfer(self):
        global transferList

        (self.treeview).delete(*self.treeview.get_children())
        (self.treeview2).delete(*self.treeview2.get_children())
        
        for file in dirs:
            print("Files moved: ", file)
            true_path2 = self.select + "/" + file
            shutil.move(true_path2, self.select2)

        
        
        
        for i, file in enumerate(dirs):
            true_path = self.select + "/" + file
            self.treeview2.insert('', i, text = file)

            
        fileStamp= self.treeview2.get_children()
        transferList = []
        for item in fileStamp:
            transferList.append((self.treeview2).item(item)['text'])

        self.timeStamp()

    
    
    def timeStamp(self):
        global transferList
        global c
        global conn
        
        conn = sqlite3.connect('timestamp.db')
        c = conn.cursor()
        
        #c.execute('DROP TABLE transferTime')
        #c.execute('DROP TABLE timeFiles')
        c.execute('CREATE TABLE IF NOT EXISTS transferTime(transferFile VARCHAR NOT NULL, date_ID VARCHAR NOT NULL)')
        c.execute('CREATE TABLE IF NOT EXISTS timeFiles(transferName VARCHAR NOT NULL)')
        
        TS = str(datetime.datetime.now().time())
        tStamp = TS[0:8]

        DS = str(datetime.datetime.now())
        dStamp = DS[0:11]

        offStamp = tStamp + ' | ' + dStamp
        print(offStamp)

    
        
        
        for fileName in transferList:
            c.execute('INSERT INTO transferTime VALUES(?,?)', (fileName, offStamp))
            c.execute('INSERT INTO timeFiles(transferName) VALUES(?)', (offStamp,))
            
            conn.commit()
        
        
        self.treeviewInsert()

        
    
    def treeviewInsert(self):
        conn = sqlite3.connect('timestamp.db')
        c = conn.cursor()

        
        select_distinct = c.execute('SELECT DISTINCT date_ID FROM transferTime').fetchall()
        select_last_entry = c.execute('SELECT * FROM timeFiles ORDER BY transferName LIMIT 1').fetchall()

        self.treeview3.delete(*self.treeview3.get_children())

        print('select_distinct', select_distinct)

        for i,item in enumerate(select_distinct):

            self.treeview3.heading(column = "#0", text = 'Last Transfer: ' + str(item)[2:23])
            self.treeview3.insert('', i, text = str(item)[2:23])

      

    
    def treeviewClick(self):
        conn = sqlite3.connect('timestamp.db')
        c = conn.cursor()
        self.treeview4.delete(*self.treeview4.get_children())
        select_distinct = c.execute('SELECT DISTINCT date_ID FROM transferTime').fetchall()
        select_last_entry = c.execute('SELECT * FROM timeFiles ORDER BY transferName desc LIMIT 1').fetchall()

        timeFiles_all = c.execute('SELECT * FROM timeFiles').fetchall()

        
        date_list = []  
        for value in select_distinct:
            date_list.append(value)
            
            
        
        
        for i, thing in enumerate(date_list):
            
            select_files = c.execute('SELECT transferFile FROM transferTime WHERE date_ID = ?', (date_list[i])).fetchall()
            curItem = self.treeview3.focus()
            select_treeview = self.treeview3.item(str(curItem))['text']
        
            self.treeview4.heading(column = "#0", text = 'File View: ' + str(select_treeview))
            self.treeview4.delete(*self.treeview.get_children())
        
            print('Select', str(date_list[i])[2:23] )             
            if select_treeview == str(date_list[i])[2:23]:
                
                for item in select_files:
                    self.treeview4.insert('', i, text = str(item).replace('(', '').replace(')', '').replace("'",'').replace(',', ''))
                    
            else:
                self.treeview4.delete(*self.treeview.get_children())


    def initialLastTransfer(self):
        conn = sqlite3.connect('timestamp.db')
        c = conn.cursor()

        select_last_entry = c.execute('SELECT * FROM timeFiles ORDER BY transferName desc LIMIT 1').fetchall()
    
        for datetime in select_last_entry:
            
            self.treeview3.heading(column = "#0", text = 'Last Transfer: ' + str(datetime)[2:23])
                


               
def main():
    
    root = Tk()
    transfer = Transfer(root)
    root.mainloop()


if __name__ == "__main__": main()
