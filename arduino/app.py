import os, sys
from tkinter.constants import DISABLED, END, LEFT, NORMAL
import numpy as np
import tkinter as tk
from tkinter import ttk, IntVar, StringVar
from tkinter import filedialog

from numpy.lib.function_base import insert

import arduino


class ArdApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title('ArdApp')
        
        self.filepath = StringVar(value='./')
        self.filename = StringVar(value='arduino')
        self.fnames = ['arduino', 'shake', 'swing']
        self.participants_name = StringVar(value='entry your name')
        
        self.ard = self.connect_arduino()
        self.ard_state = StringVar(value='Ready' if self.ard else 'No Arduino')
        self.ard_datalist = StringVar(value=[''])
        self.ard_data_cnt = 0
        self.ard_runtime = StringVar()
        
        self.__create_widgets()
        
    def connect_arduino(self):
        try:
            ard = arduino.Arduino()
        except:
            ard = None
        return ard
    
    def __create_widgets(self):
        self.main_frame = self.__init_main_frame()
        self.main_frame.grid(row=0, column=0)
        
    def __init_main_frame(self):
        frame = tk.Frame(self, relief='raised')
        fileinfo_frame = self.__file_info_frame(frame)
        partinfo_frame = self.__prticipants_info_frame(frame)
        ardinfo_frame = self.__arduino_info_frame(frame)
        
        partinfo_frame.grid(row=0, column=0)
        fileinfo_frame.grid(row=1, column=0)
        ardinfo_frame.grid(row=0, rowspan=2, column=1)
        
        
        return frame
    
    def __file_info_frame(self, root):
        def   __dirdialog():
            dirs = os.path.abspath(os.path.dirname(__file__))
            dirpath = filedialog.askdirectory(initialdir=dirs)
            self.filepath.set(dirpath)
        
        frame = tk.LabelFrame(root, text='File Info')
        
        path_frame = tk.Frame(frame)
        path_frame.pack()
          
        path_label = tk.Label(path_frame, text='File Path')
        path_label.pack(side=LEFT)
        path_entry = tk.Entry(path_frame, textvariable=self.filepath, width=25)
        path_entry.pack(side=LEFT)
        path_btn = tk.Button(path_frame, text='ref', command=__dirdialog)
        path_btn.pack(side=LEFT)
        
        file_frame = tk.Frame(frame)
        file_frame.pack()
        
        file_label = tk.Label(file_frame, text='File Name')
        file_label.pack(side=LEFT)
        file_entry = ttk.Combobox(file_frame, textvariable=self.filename,
                                  values=self.fnames, width=25)
        
        def set_btn_clicked(): # TODO 個々の処理後で生地にする
            fname = self.filename.get()
            i = self.datalist.curselection()[0]
            data = list(map(eval, self.ard_datalist.get()[1:-1].split(', ')))
            data[i] = fname
            self.ard_datalist.set(data)
            
        file_entry.pack(side=LEFT)
        self.file_btn = tk.Button(file_frame, text='set', state=DISABLED, command=set_btn_clicked)
        self.file_btn.pack(side=LEFT)
        return frame
    
    def __prticipants_info_frame(self, root):
        frame = tk.LabelFrame(root, text='Participants Info')
        
        name_frame = tk.Frame(frame, )
        name_frame.pack()
        name_label = tk.Label(name_frame, text='Name')
        name_label.pack(side=LEFT)
        name_entry = tk.Entry(name_frame, textvariable=self.participants_name, width=25)
        name_entry.pack(side=LEFT)
        return frame
    
    def __arduino_info_frame(self, root):
        frame = tk.LabelFrame(root, text='Arduino Info')
        
        state_frame = tk.Frame(frame, )
        state_frame.pack()
        state_label = tk.Label(state_frame, text='State: ')
        state_label.pack(side=LEFT)
        ard_state = tk.Label(state_frame, textvariable=self.ard_state)
        ard_state.pack(side=LEFT)
        
        def show_data(event):
            if self.datalist.size() == 0:
                return False
            i = self.datalist.curselection()
            if len(i) == 0: # gui の runtime いじったときの謎挙動の回避
                return False
            self.file_btn['state'] = NORMAL
            i = i[0]
            data = np.array(self.ard.raw[i])
            data_len_val['text'] = len(data)
            data_ave_val['text'] = np.mean(data, axis=0)[1]
            data_std_val['text'] = np.std(data, axis=0)[1]
            val_list.delete(0, END)
            for i, d in enumerate(data):
                val_list.insert(END, f'{i:10},{d[0]:10},{d[1]:5}')
            return True
        
        data_frame = tk.LabelFrame(frame, text='Datas')
        data_frame.pack()
        self.datalist = tk.Listbox(data_frame, listvariable=self.ard_datalist,)
        self.datalist.bind('<<ListboxSelect>>', show_data)
        self.datalist.delete(0)
        self.datalist.pack(side=LEFT)
        
        datainfo_frame = tk.Frame(data_frame)
        datainfo_frame.pack(side=LEFT)
        data_len_label = tk.Label(datainfo_frame, text='n:')
        data_len_label.grid(row=0, column=0)
        data_len_val = tk.Label(datainfo_frame, text='None')
        data_len_val.grid(row=0, column=1)
        data_ave_label = tk.Label(datainfo_frame, text='ave:')
        data_ave_label.grid(row=1, column=0)
        data_ave_val = tk.Label(datainfo_frame, text='None')
        data_ave_val.grid(row=1, column=1)
        data_std_lebel = tk.Label(datainfo_frame, text='std:',)
        data_std_lebel.grid(row=2, column=0)
        data_std_val = tk.Label(datainfo_frame, text='None')
        data_std_val.grid(row=2, column=1)
        val_list = tk.Listbox(datainfo_frame, listvariable=StringVar(value=[f'{"idx":10},{"time":10},{"val":5}']))
        val_list.grid(row=3, column=0, columnspan=2)
        
        
        
        def start_btn_clicked():
            def inner():
                if self.ard_state.get() == 'Run':
                    return False
                print(self.ard_runtime.get())
                if self.ard_runtime.get().isdigit():
                    runtime = int(self.ard_runtime.get())
                    self.ard_state.set('Run')
                    self.ard.start()
                    self.after(runtime*1000, stop_btn_clicked())
                    return True
            return inner
        
        def stop_btn_clicked():
            def inner():
                if self.ard_state.get() == 'Ready':
                    return False
                self.ard_state.set('Ready')
                self.ard.stop()
                self.ard_data_cnt += 1
                self.datalist.insert(END, self.filename.get())
                return True
            return inner
        
        def save_btn_clicked():
            def inner():
                if self.ard_data_cnt < 1:
                    return False
                try:
                    n = int(self.datalist.curselection()[0])
                except Exception as e:
                    print(e)
                    return False
                path = self.filepath.get()
                fname = self.filename.get()
                return self.ard.save(n, path, fname)
            return inner
        
        ctrl_frame = tk.LabelFrame(frame, text='Controller')
        ctrl_frame.pack()
        
        runtime_label = tk.Label(ctrl_frame, text='RunTime')
        runtime_label.pack()
        runtime_entry = tk.Entry(ctrl_frame, textvariable=self.ard_runtime, width=5)
        runtime_entry.pack()
        start_btn = tk.Button(ctrl_frame, text='Start', command=start_btn_clicked())
        start_btn.pack(side=LEFT)
        stop_btn = tk.Button(ctrl_frame, text='Stop', command=stop_btn_clicked())
        stop_btn.pack(side=LEFT)
        save_btn = tk.Button(ctrl_frame, text='Save', command=save_btn_clicked())
        save_btn.pack(side=LEFT)

        return frame
              
        

def main():
    ArdApp().mainloop()
    
if __name__ == '__main__':
    main()
