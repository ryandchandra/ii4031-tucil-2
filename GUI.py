import tkinter as tk
import tkinter.scrolledtext as st
import tkinter.filedialog as fd
import math

from Components import *

from ModifiedRC4Lib import *

class GUI:
    def __init__(self,parent):
        #--- init ---#
        self.parent = parent
        self.parent.title("Kriptografi")
        
        #--- define grid ---#
        self.parent.columnconfigure([0,1,2,3],weight=1)
        self.parent.rowconfigure([0,1,2],weight=1,minsize=100)
        
        #--- plaintext ---#
        self.plaintext = TextFrame(
            title="Plaintext",
            width=50,
            height=5
        )
        self.plaintext.frame.grid(row=0,column=0,columnspan=3)
        
        #--- encrypt button ---#
        self.encrypt_button = tk.Button(text="Encrypt",command=self.Encrypt)
        self.encrypt_button.grid(row=1,column=0,padx=10,pady=10)

        #--- keyframe ---#
        self.keyframe = KeyFrame(title="Key",width=34)
        self.keyframe.frame.grid(row=1,column=1)

        #--- decrypt button ---#
        self.decrypt_button = tk.Button(text="Decrypt",command=self.Decrypt)
        self.decrypt_button.grid(row=1,column=2,padx=10,pady=10)
        
        #--- ciphertext ---#
        self.ciphertext = TextFrame(
            title="Ciphertext",
            width=50,
            height=5
        )
        self.ciphertext.frame.grid(row=2,column=0,columnspan=3)
        
        #--- info ---#
        self.info = tk.Label(text="Modified RC4");
        self.info.grid(row=0,column=3);
        
        #--- file frame ---#
        file_method_list = ["Open Plaintext from File","Open Ciphertext from File","Save Plaintext to File","Save Ciphertext to File","Encrypt/Decrypt File"]
        self.file_frame = ButtonListFrame(
            title = "File",
            labels = file_method_list,
            width = 25
        )
        self.file_frame.button_list[0].bind("<Button-1>",lambda event,text="plaintext": self.OpenFileText(event,text))
        self.file_frame.button_list[1].bind("<Button-1>",lambda event,text="ciphertext": self.OpenFileText(event,text))
        self.file_frame.button_list[2].bind("<Button-1>",lambda event,text="plaintext": self.SaveFileText(event,text))
        self.file_frame.button_list[3].bind("<Button-1>",lambda event,text="ciphertext": self.SaveFileText(event,text))
        self.file_frame.button_list[4].bind("<Button-1>",self.EncryptDecryptFileWindow)
        self.file_frame.frame.grid(row=1,column=3,rowspan=2)  
        
    def Encrypt(self):
        # Event handler when encrypt button is pressed
        # Encrypt plaintext and key
        
        # Take the plaintext and key from the field
        plaintext = self.plaintext.entry.get("1.0",tk.END)[:-1]
        key = self.keyframe.entry.get()
            
        # Check for validity
        if (len(plaintext)==0): # Empty plaintext
            self.AlertWindow("Please insert plaintext")
        elif (len(key)==0): # Empty key
            self.AlertWindow("Please insert key")
        else:
            plaintext_byteintarray = StringToByteIntArray(plaintext)
            key_byteintarray = StringToByteIntArray(key)
            
            # Encrypt
            ciphertext_byteintarray = ModifiedRC4Encrypt(plaintext_byteintarray,key)
            ciphertext = bytes(ciphertext_byteintarray)
            
            # Insert into ciphertext field
            self.ciphertext.entry.delete("1.0",tk.END)
            self.ciphertext.entry.insert("1.0",ciphertext)

            
    def Decrypt(self):
        # Event handler when decrypt button is pressed
        # Decrypt ciphertext and key
        
        # Take the ciphertext and key from the field
        key = self.keyframe.entry.get()
        ciphertext = self.ciphertext.entry.get("1.0",tk.END)[:-1]

        # Check for validity
        if (len(ciphertext)==0): # Empty ciphertext
            self.AlertWindow("Please insert ciphertext")
        elif (len(key)==0): # Empty key
            self.AlertWindow("Please insert key")
        else:
            ciphertext_byteintarray = StringToByteIntArray(ciphertext)
            key_byteintarray = StringToByteIntArray(key)
            
            # Decrypt
            plaintext_byteintarray = ModifiedRC4Decrypt(ciphertext_byteintarray,key)
            plaintext = bytes(plaintext_byteintarray)
            
            # Insert into plaintext field
            self.plaintext.entry.delete("1.0",tk.END)
            self.plaintext.entry.insert("1.0",plaintext)
        
    def OpenFileText(self,event,text):
        # Open file using open file dialog
        
        # Take filename
        filename = fd.askopenfilename(
            initialdir = "/",
            title = "Select " + text + " file",
            filetypes = [("Text files (.txt)","*.txt"),("All files","*.*")]
        )
        
        if (filename!=""): # If filename is chosen
            content = OpenFileAsByteIntArray(filename)
            content_bytes = bytes(content)
            
            if (text=="plaintext"): # For plaintext, insert to plaintext field
                self.plaintext.entry.delete("1.0",tk.END)
                self.plaintext.entry.insert("1.0",content_bytes)
            elif (text=="ciphertext"): # For ciphertext, insert to ciphertext field
                self.ciphertext.entry.delete("1.0",tk.END)
                self.ciphertext.entry.insert("1.0",content_bytes)
        
        return "break"
        
    def SaveFileText(self,event,text):
        # Save file using save file dialog
        
        # Take filename
        filename = fd.asksaveasfilename(
            initialdir = "/",
            title = "Select " + text + " file",
            filetypes = [("Text files (.txt)","*.txt"),("All files","*.*")],
            defaultextension = [("Text files (.txt)","*.txt"),("All files","*.*")]
        )
        
        if (filename!=""): # If file name is chosen
            file = open(filename,"wb")
            if (text=="plaintext"): # For plaintext, insert the plaintext
                plaintext = self.plaintext.entry.get("1.0",tk.END)[:-1]
                plaintext_byteintarray = StringToByteIntArray(plaintext)
                for byteint in plaintext_byteintarray:
                    file.write(byteint.to_bytes(1,byteorder='little'))
            elif (text=="ciphertext"): # For ciphertext, insert the ciphertext
                ciphertext = self.ciphertext.entry.get("1.0",tk.END)[:-1]
                ciphertext_byteintarray = StringToByteIntArray(ciphertext)
                for byteint in ciphertext_byteintarray:
                    file.write(byteint.to_bytes(1,byteorder='little'))
                
            file.close()
        
        return "break"
        
    def AlertWindow(self,text):
        # Create new window for alert
        # Components : label with input text and dismiss button
        alert_window = tk.Toplevel(self.parent)
        alert_window.title("Alert")
        
        tk.Label(master=alert_window,text=text).pack(padx=120,pady=20)
        tk.Button(master=alert_window,text="OK",width=10,command=lambda:alert_window.destroy()).pack(pady=10)
        
        alert_window.grab_set()
        
    def EncryptDecryptFileWindow(self,event):
        # Create new window for file encrypt/decrypt
        # Components : label, key entry, and buttons
        new_window = tk.Toplevel(self.parent)
        new_window.title("Encrypt/Decrypt File")
        
        self.file = ""

        # Define elements
        self.file_label = tk.Label(master=new_window,text="File : " + self.file,width=50)
        self.file_label.grid(row=0,column=0,columnspan=2,sticky="we",padx=120,pady=2)
        self.key_label = tk.Label(master=new_window,text="Key :")
        self.key_label.grid(row=1,column=0,columnspan=2,pady=2)
        self.key_entry = tk.Entry(master=new_window,width=15)
        self.key_entry.grid(row=2,column=0,columnspan=2,pady=2)
        
        # Button list
        tk.Button(master=new_window,text="Choose File",width=20,command=self.ChooseFile).grid(row=3,column=0,columnspan=2,pady=2)
        tk.Button(master=new_window,text="Encrypt and Save",width=20,command=self.SaveEncryptedFile).grid(row=4,column=0,columnspan=2,pady=2)
        tk.Button(master=new_window,text="Decrypt and Save",width=20,command=self.SaveDecryptedFile).grid(row=5,column=0,columnspan=2,pady=2)
        tk.Button(master=new_window,text="Unselect File",width=20,command=self.UnselectFile).grid(row=6,column=0,columnspan=2,pady=2)

        new_window.grab_set()
        
    def ChooseFile(self):
        # Take filename
        filename = fd.askopenfilename(
            initialdir = "/",
            title = "Select  file",
            filetypes = [("All files","*.*")],
        )
        
        if (filename!=""):
            self.file_label["text"] = "File : " + filename
            self.file = filename
                
    def SaveEncryptedFile(self):
        # buka file di self.file 
        if (self.file==""):
            self.AlertWindow("Please choose a file")
        else:
            #encrypt
            key = self.key_entry.get()
            if (len(key)==0):
                self.AlertWindow("Please insert key")
            else:
                # baca per byte lalu masukkan ke array dalam bentuk int
                plaintext_byteintarray = OpenFileAsByteIntArray(self.file)
                
                key_byteintarray = StringToByteIntArray(key)
                
                # encrypt
                ciphertext_byteintarray = ModifiedRC4Encrypt(plaintext_byteintarray,key)
                
                # save
                filename = fd.asksaveasfilename(
                    initialdir = "/",
                    title = "Save file",
                    filetypes = [("All files","*.*")],
                    defaultextension = [("All files","*.*")]
                )
                if (filename!=""):
                    output_file = open(filename, "wb")
                    
                    for byteint in ciphertext_byteintarray:
                        output_file.write(byteint.to_bytes(1,byteorder='little'))
                    
                    output_file.close()
        
    def SaveDecryptedFile(self):
        # buka file di self.file 
        if (self.file==""):
            self.AlertWindow("Please choose a file")
        else:
            # decrypt
            key = self.key_entry.get()
            if (len(key)==0):
                self.AlertWindow("Please insert key")
            else:
                # baca per byte lalu masukkan ke array dalam bentuk int
                ciphertext_byteintarray = OpenFileAsByteIntArray(self.file)
                
                key_byteintarray = StringToByteIntArray(key)
                
                # decrypt
                plaintext_byteintarray = ModifiedRC4Encrypt(ciphertext_byteintarray,key)

                # save
                filename = fd.asksaveasfilename(
                    initialdir = "/",
                    title = "Save file",
                    filetypes = [("All files","*.*")],
                    defaultextension = [("All files","*.*")]
                )
                if (filename!=""):
                    output_file = open(filename, "wb")
                    
                    for byteint in plaintext_byteintarray:
                        output_file.write(byteint.to_bytes(1,byteorder='little'))
                    
                    output_file.close()
    
    def UnselectFile(self):
        self.file = ""
        self.file_label["text"] = "File : " + self.file
