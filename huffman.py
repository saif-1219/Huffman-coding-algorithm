import tkinter as tk
from tkinter import *
from tkinter.ttk import Combobox
from tkinter import filedialog
from tkinter.filedialog import askopenfile
import time

def calc_frequency(data):
    #This function calculates the frequency of characters in the data and return a dict
    freq = {}
    for i in data:
        if i not in freq:
            freq[i] = 1
        else:
            freq[i]+=1    
    return freq

def sort_dict_by_value(d):
    #This function sorts the dictionary by value
    sorted_dict = {k: v for k, v in sorted(d.items(), key=lambda item: item[1])}
    return sorted_dict

def create_huff_tree(sorted_freq_data):    
    #This function creates a huffman tree from the sorted frequency dict
    nodes = [{'sym': sym, 'freq': freq} for sym, freq in sorted_freq_data.items()]
    # print(nodes)
    while len(nodes) > 1:
        # Find the two nodes with the smallest frequencies
        min1_idx, min2_idx = 0, 1
        if nodes[min1_idx]['freq'] > nodes[min2_idx]['freq']:
            min1_idx, min2_idx = min2_idx, min1_idx
        for i in range(2, len(nodes)):
            if nodes[i]['freq'] < nodes[min1_idx]['freq']:
                min2_idx = min1_idx
                min1_idx = i
            elif nodes[i]['freq'] < nodes[min2_idx]['freq']:
                min2_idx = i
        
        # Combine the two nodes into a new node
        new_node = {'left': nodes[min1_idx], 'right': nodes[min2_idx]}
        new_node['freq'] = new_node['left']['freq'] + new_node['right']['freq']
        
        # Remove the two old nodes and add the new one
        nodes[min1_idx] = new_node
        nodes.pop(min2_idx)

    return nodes[0]

def encode(tree):
    #This function creates codes for the different characters in the text
    code_map = {}

    def build_codes(node, code):
        if 'sym' in node:
            code_map[node['sym']] = code
        else:
            #assignig 0 for left and 1 for right
            build_codes(node['left'], code + '0')
            build_codes(node['right'], code + '1')

    build_codes(tree, '')
    return code_map
    
def encode_text(text, code):
    #this function encodes the text based on the codes given
    encoded = ''
    for i in text:
        encoded += code[i]
    return encoded
        
def add_padding(encoded_text):
    #This function makes the encoded text a multiple of 8 by adding zeroes in the end and it also adds the information in the beginning
    zeroes = 8-len(encoded_text)%8
    encoded_text = encoded_text+('0' * zeroes)
    encoded_text = "{0:08b}".format(zeroes) + encoded_text
    return encoded_text

def bin_to_int(bin_txt):
    #this function converts the padded encoded text to integer
    int_txt = []
    for i in range(0,len(bin_txt),8):
        byte = bin_txt[i:i+8]
        int_txt.append(int(byte,2))
    return int_txt 

def remove_padding(text):
    #this function removes the padding while decompressing
    num_pad = int(text[:8],2)
    length = len(text)
    text = text[8:length-num_pad]
    return text

def decode(text,codes):
    #it decodes the coded text by looking it at the given 
    curr = ''
    decoded = ''
    for i in text:
        curr += i
        if curr in codes:
            if codes[curr] == "sp":
                decoded += " "
            else:
                decoded += codes[curr]
            curr = ''
    return decoded    

def compress(text):
    frequency = calc_frequency(text)
    sorted_freq = sort_dict_by_value(frequency)
    huff_tree = create_huff_tree(sorted_freq)
    codes = encode(huff_tree)
    encoded_text = encode_text(text,codes)
    padded_text = add_padding(encoded_text)
    int_txt = bin_to_int(padded_text)
    final_encoding = bytes(int_txt)
    return (final_encoding,codes)

def decompress(text,codes):
    text = remove_padding(text)
    
    text = decode(text,codes)
    print(text)
    return text




class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # the main container that holds all the frames
        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)
        container.place(x=200,y=40)

        self.frames = {}
        # adding frames to the dictionary
        for F in (Page1,Page2,Page3):

             frame = F(container,self)
             self.frames[F] = frame
        # frame.grid(row = 0, column = 0, sticky = "w")
        self.show_frame(Page1)

    def show_frame(self,page_name):
        #SHOWS A FRAME WITH THE GIVEN NAME
        for frame in self.frames.values():
            frame.grid_remove()
        frame = self.frames[page_name]
        frame.grid()


class Page1(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller

# title
        lbl=tk.Label(self, text="File Compressor", fg='black', font=("Helvetica", 16))
        lbl.grid(row=0,column=1)

# the options for compress (lbl1) decompress( lbl2)
        self.var1 = tk.BooleanVar()
        
        lbl1 = tk.Label(self,text = "compress",font =("Helvetica",12,"bold"))
        lbl1.grid(row=40)
        rButton1 = tk.Radiobutton(self,variable = self.var1,value=True,command=self.switch_pages)
        rButton1.grid(row=50)

        lbl2 = tk.Label(self,text = "decompress",font =("Helvetica",12,"bold"))
        lbl2.grid(row=40,column=4)
        rButton2 = tk.Radiobutton(self,variable = self.var1,value=False,command=self.switch_pages)
        rButton2.grid(row=50,column=4)
# main function which enables function switching
    def switch_pages(self):
        if not self.var1.get():
            self.controller.show_frame(Page3)
        else:
            self.controller.show_frame(Page2)

# compress frame
class Page2(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        self.filename = ''
        self.output = ''

        # title file compressor
        lbl=tk.Label(self, text="File Compressor", fg='black', font=("Helvetica", 16))
        lbl.grid(row=0,column=4)

# functions which enable file browsing and uploading
        my_str2=tk.StringVar()
        l21=tk.Label(self,textvariable=my_str2,fg='red')
        l21.grid(row=8,column=4)
        my_str2.set("file name here")
        # enables file browsing
        def browseFiles():
            
            self.filename = tk.filedialog.askopenfilename(initialdir = "/",title = "Select a File",filetypes = (("Text files","*.txt*"),("all files","*.*")))
            self.output = (self.filename.split("."))[0]+'.bin'
            if(self.filename):
                my_str2.set(self.filename)
                fob=open(self.filename,'r')
                # print(fob.read())
        button_explore = tk.Button(self,text = "Browse Files",command = browseFiles,fg='blue')
        button_explore.grid(row=5,column=4)

        # enables compression
        bts=Button(self, text="Compress",command=self.compress, fg='blue')
        bts.grid(row=15,column=4)

        # exits the program
        button_exit = tk.Button(self,text = "Exit",command = exit)  
        button_exit.grid(row=20,column=4)

        #  return option
        lbl2 = tk.Label(self,text = "return",font =("Helvetica",12,"bold"))
        lbl2.grid(row=70,column=4)
        self.var1 = tk.BooleanVar()
        ribButton2 = tk.Radiobutton(self,variable = self.var1,value=False,command=self.switch_pagess)
        ribButton2.grid(row=60,column=4)

        
 # switch frames
    def switch_pagess(self):
        if not self.var1.get():
            self.controller.show_frame(Page1)
        else:
            self.controller.show_frame(Page3)

    def compress(self):
        with open(self.filename, "r") as file, open(self.output, "wb") as out_path,open(self.filename[:-4]+"_key.txt","w") as key_file:
            text = file.read()
            text = text.rstrip()
            coded_text = compress(text)[0]
            codes = compress(text)[1]
            print(codes)
            for i in codes:
                if i == " ":
                    key_file.write("sp")
                else:
                    key_file.write(i)
                key_file.write(" ")
                key_file.write(codes[i])
                key_file.write(" ")
            out_path.write(coded_text)
        

class Page3(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        self.filename = ''
        self.output = ''
        self.key = ''
        # title file compressor
        lbl=tk.Label(self, text="File Decompressor", fg='black', font=("Helvetica", 16))
        lbl.grid(row=0,column=4)

        # enables file browsing and uploading of the compressed file and the key file
        my_str=tk.StringVar()
        l2=tk.Label(self,textvariable=my_str,fg='red')
        l2.grid(row=3,column=4)
        my_str.set("file here")
        my_str2=tk.StringVar()
        l21=tk.Label(self,textvariable=my_str2,fg='red')
        l21.grid(row=5,column=4)
        my_str2.set("key file here")
        def browseFiles():
            self.filename = tk.filedialog.askopenfilename(initialdir = "/",title = "Select a File",filetypes = (("Binary files","*.bin*"),("all files","*.*")))
            self.output = (self.filename.split("."))[0]+'_decompressed.txt'
            
            if(self.filename):
                my_str.set(self.filename)
                fob=open(self.filename,'r')
                # print(fob.read())
            self.key = tk.filedialog.askopenfilename(initialdir = "/",title = "Select a File",filetypes = (("Text files","*.txt*"),("all files","*.*")))
            if(self.key):
                my_str2.set(self.key)
                fobi=open(self.key,'r')
                # print(fobi.read())
        button_explore = tk.Button(self,text = "Browse Files",command = browseFiles,fg='blue')
        button_explore.grid(row=2,column=4)
        button_explore2= tk.Button(self,text = "Browse key Files",command = browseFiles,fg='red')
        button_explore2.grid(row=4,column=4)


        # enables decompression
        bts=Button(self, text="Decompress",command=self.decompress, fg='blue')
        bts.grid(row=8,column=4)

        # exits the program
        button_exit = tk.Button(self,text = "Exit",command = exit)  
        button_exit.grid(row=10,column=4)

       
       
#  return option re4turns to the main page
        lbl2 = tk.Label(self,text = "return",font =("Helvetica",12,"bold"))
        lbl2.grid(row=70,column=4)
        self.var1 = tk.BooleanVar()
        rButton2 = tk.Radiobutton(self,variable = self.var1,value=False,command=self.switch_pages3)
        rButton2.grid(row=60,column=4)

  # switch frames
    def switch_pages3(self):
        if not self.var1.get():
            self.controller.show_frame(Page1)
        else:
            self.controller.show_frame(Page2)
    def decompress(self):
        with open(self.filename, "rb") as file, open(self.output, "w") as out_path, open(self.key,"r") as keys:
            codes_dict = {}
            code = keys.read().split()
            # print(code)
            for i in range(0,len(code)-1,2):
                codes_dict[code[i+1]] = code[i]
            # print(codes_dict)

            bit_str = ''
            byte = file.read(1)
            while byte:
                # print(byte,ord(byte))
                byte = ord(byte)
                string = ((bin(byte))[2:]).rjust(8,"0")
                bit_str += string
                byte = file.read(1)
            
            decoded_text = decompress(bit_str,codes_dict)
            
            out_path.write(decoded_text)

app = MainApp()
app.title('File Compressor')
app.geometry("600x350")
app.mainloop()