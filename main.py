import gzip_extract
import database
import tableContent
import migration
import Tkinter as tk
from Tkinter import *
import tkFont
import tkMessageBox
from os import listdir, path,makedirs


def infoCallBack(result):
   tkMessageBox.showinfo( "Information", result)

class gui_app(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("1340x300+130+180")
        
        helv24 = tkFont.Font(family="Helvetica",size=24,weight="bold")
        
        list_directory = database.list()
        
        L1 = tk.Label(self, text="list directory")
        L1 =  L1.grid(row=1, column=0)
        
        self.LB1 = tk.Listbox(self,selectmode=MULTIPLE)
        self.LB1.grid(row=2, column=0)
        yscroll = tk.Scrollbar(command=self.LB1.yview, orient=tk.VERTICAL)
        yscroll.grid(row=2, column=0, sticky=NS+E,pady=1)
        self.LB1.configure(yscrollcommand=yscroll.set)
        self.list_directory_refresh()
        #index = 0
        #for line in list_directory:
        #    self.LB1.insert(index,line)
        #    index += 1
            
        L2 = tk.Label(self, text="source directory")
        L2 =  L2.grid(row=1, column=1)
        
        list = listdir('.')   
        list_file=[]     
        for file in list:
            if path.isfile(file) or file[0] =='.': pass
            else: list_file.append(file)
        self.LB2 = tk.Listbox(self)
        self.LB2.grid(row=2, column=1)
        yscroll2 = tk.Scrollbar(command=self.LB2.yview, orient=tk.VERTICAL)
        yscroll2.grid(row=2, column=1, sticky=NS+E,pady=1)
        self.LB2.configure(yscrollcommand=yscroll2.set)
        self.list_file_refresh()
        #index = 0
        #for line in list_file:
        #    self.LB2.insert(index,line)
        #    index += 1
        
        
        L3 = tk.Label(self, text="destination directory")
        L3 =  L3.grid(row=1, column=2)
        self.E3 = Entry(self, bd =1)
        self.E3.grid(row=1, column=3)
        
        B1 = tk.Button(self, text ="Backup",width = 15,height=2, font=helv24, command = lambda: self.backup(list_directory), justify="center",wraplength=1)
        B2 = tk.Button(self, text ="Create Empty",width = 15,height=2, font=helv24,command = lambda: self.migrate_empty(list_file), justify="center",wraplength=1)
        B3 = tk.Button(self, text ="Migrate",width = 15,height=2, font=helv24,command = lambda: self.migrate(list_file), justify="center",wraplength=1)
        B4 = tk.Button(self, text ="Restore",width = 15,height=2,font=helv24,command = lambda: self.restore(list_file), justify="center",wraplength=1)
        B5 = tk.Button(self, text ="Drop",width = 15,height=2,font=helv24,command = lambda: self.drop(list_directory), justify="center",wraplength=1)
        B6 = tk.Button(self, text ="Modules",width = 15,height=2,font=helv24,command = lambda: self.modules(list_directory), justify="center",wraplength=1)
        
        B1.grid(row=0, column=0)
        B2.grid(row=0, column=1)
        B3.grid(row=0, column=2)
        B4.grid(row=0, column=3)
        B5.grid(row=0, column=4)
        B6.grid(row=0, column=5)
      
    def list_directory_refresh(self):
        list_directory = database.list()
        index = 0
        self.LB1.delete(0,self.LB1.size())
        for line in list_directory:
            self.LB1.insert(index,line)
            index += 1
            
    def list_file_refresh(self):
        list = listdir('.')   
        list_file=[]     
        for file in list:
            if path.isfile(file) or file[0] =='.': pass
            else: list_file.append(file)
        self.LB2.delete(0,self.LB2.size())
        index = 0
        for line in list_file:
            self.LB2.insert(index,line)
            index += 1
        
    def backup(self,databases):
        items = map(int, self.LB1.curselection())
        ids = self.LB1.curselection()
        list_directory = []
        
        for id in ids:
            list_directory.append(databases[int(id)])
                     
        database.backup(list_directory)
        gzip_extract.extract(list_directory)
        database.backup_plain(list_directory)
        tableContent.obtain(list_directory)
        tableContent.compare(list_directory)
        
        
        self.list_file_refresh()
        infoCallBack("ok")
    
    def drop(self,databases):
        items = map(int, self.LB1.curselection())
        ids = self.LB1.curselection()
        list_directory = []
        
        for id in ids:
            list_directory.append(databases[int(id)])
                     
        database.drop(list_directory)
        self.list_directory_refresh()
        infoCallBack("ok")
    
    def restore(self, list_file):
        items = map(int, self.LB2.curselection())
        ids = self.LB2.curselection()
        
        source_directory = [list_file[int(ids[0])]]
        destination_directory = [self.E3.get()]
        
        database.create(destination_directory)
        database.restore(source_directory,destination_directory)
        self.list_directory_refresh()
        infoCallBack("ok")
    
    def migrate_empty(self, list_file):
        items = map(int, self.LB2.curselection())
        ids = self.LB2.curselection()
        
        source_directory = [list_file[int(ids[0])]]
        destination_directory = [self.E3.get()]
        
        migration.empty(source_directory, destination_directory)
        infoCallBack("ok")

    def migrate(self, list_file):
        items = map(int, self.LB2.curselection())
        ids = self.LB2.curselection()
        
        source_directory = [list_file[int(ids[0])]]
        destination_directory = [self.E3.get()]

        migration.create(source_directory, destination_directory)
        infoCallBack("ok")

    def modules(self, databases):
        items = map(int, self.LB1.curselection())
        ids = self.LB1.curselection()
        list_directory = []
        
        for id in ids:
            list_directory.append(databases[int(id)])
                     
        modules_databases = database.listModules(list_directory)
        for db, modules in modules_databases.iteritems():
            if not path.exists(db):
                makedirs(db)
            f = open(path.join(db, "modules.dat"), "w")
            f.write("Number of modules: %d\n\n" % len(modules))
            modules.sort()
            f.write("\n".join(modules))
            f.close()
        
        self.list_file_refresh()
        infoCallBack("OK. Modules listed.")


if __name__ == '__main__':    
    app = gui_app()
    app.mainloop()