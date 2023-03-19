#GUI (Graphical User Interface)
#memanggil module-module 
import tkinter as tk
from tkinter import ttk
import pandas as pd
import numpy as np
from pandas import DataFrame
import sklearn
import matplotlib.pyplot as plt

#membuat window GUI
window = tk.Tk()
window.configure(bg="steel blue") #mengubah warna background GUI
window.geometry("800x1000") #mengubah size tampilan ketika di run
window.resizable(width=False, height=False)
window.title("Exponential Smoothing") #memberi judul pada bar

#memberi label pada GUI
labelJudul=tk.Label(window, text="Menghitung Nilai Peramalan Menggunakan Single Exponential Smoothing",font=('helvetica',12,'bold'))
labelJudul.pack(padx=2,pady=2,fill="x",expand=True)

#membuat frame 
input_frame=ttk.Frame(window)
input_frame.pack(padx=2,pady=0,fill="x",expand=True)

#Input File Excel
labelData=ttk.Label(input_frame, text="Masukkan Data Excel",font=('helvetica',10,'bold'))
labelData.pack(padx=10,pady=10,fill="x",expand=True)

##Syntax input file
from tkinter import filedialog
def getExcel():
    global df
    data = filedialog.askopenfilename()
    read_file = pd.read_excel (data)
    df = DataFrame(read_file)

##Membuat Button untuk input file      
buttonData=ttk.Button(input_frame, text="Pilih File", command=getExcel)
buttonData.pack(padx=10,pady=10,fill="y",expand=True)
     
#Label Hasil 
label3=ttk.Label(input_frame, text="Hasil", font=('helvetica',10,'bold'))
label3.pack(padx=10,fill="x",expand=True)
##Hasil 
hasil_label3 = ttk.Label(input_frame,text="0")
hasil_label3.pack(padx=10,fill="x",expand=True)

#Label Forecast 
label4=ttk.Label(input_frame, text="Forecasting",font=('helvetica',10,'bold'))
label4.pack(padx=10,fill="x",expand=True)
##Hasil Forecast 
hasil_label4 = ttk.Label(input_frame,text="0")
hasil_label4.pack(padx=10,fill="x",expand=True)

#Label Nilai MSE
label5=ttk.Label(input_frame, text="Nilai MSE",font=('helvetica',10,'bold'))
label5.pack(padx=10,fill="x",expand=True)
##Nilai MSE
hasil_label5 = ttk.Label(input_frame,text="0")
hasil_label5.pack(padx=10,fill="x",expand=True)

#Label Plot
label6=ttk.Label(input_frame, text="Plot Holt-Winters",font=('helvetica',10,'bold'))
label6.pack(padx=10,fill="x",expand=True)
##Plot
hasil_label6 = ttk.Label(input_frame,text="0")
hasil_label6.pack(padx=10,fill="x",expand=True)

#Rumus Single Exponential Smoothing (Metode Peramalan)
def hitung():
    global df
    #Membagi data menjadi Data Train dan Data Testing
    df_train = df.iloc[:-12]
    df_test = df.iloc[-12:]
    
    #Hasil Model Peramalan
    from statsmodels.tsa.api import SimpleExpSmoothing
    single_exponen = SimpleExpSmoothing(df_train).fit(smoothing_level=0.05, optimized=False)
    hasil_label3.configure(text=(single_exponen.summary()))

    #Forecasting untuk 12 periode ke depan
    forecasting = single_exponen.forecast(12).rename(r'$\alpha=0.05')
    hasil_label4.configure(text=(forecasting))

    #MSE
    from sklearn.metrics import mean_squared_error
    mse=mean_squared_error(df_test,forecasting)
    hasil_label5.configure(text=(mse))

    #plot
    fig = plt.figure(figsize=(5,4), dpi=80)
    ax1 = fig.add_subplot()
    ax1.plot(df_train, color='blue')
    ax1.plot(df_test, color='orange')
    ax1.plot(forecasting, color='red')
    ax1.set_xlabel('Data ke-')
    ax1.set_ylabel('Jumlah Penumpang')
    ax1.set_title('Holt Winters Single Exponential Smoothing')
    ax1.grid(True)
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
    canvas = FigureCanvasTkAgg(fig, hasil_label6 ) 
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

#Membuat Button Hitung untuk menampilkan hasil dari perhitungan    
buttonHitung=ttk.Button(input_frame, text="Hitung",command=hitung)
buttonHitung.pack(padx=10,pady=10,fill="x",expand=True)

#Mainloop untuk menjalankan GUI     
window.mainloop()
