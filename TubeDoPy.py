import tkinter as tk
from tubedopy_beta import tubedopy
from threading import Thread as td
from multiprocessing import Pool
import os


tdp = tubedopy()
path_imgDonate = os.path.expanduser('~').replace('\\', '/')
path_imgDonate += '/TubeDoPy/donate.gif'


def comprobar():
    '''
        Al activar el boton de descarga entra aqui y comprueba si
        la URL viene de una lista o es un link individual.
    '''


    if '&list=' in url_box.get():
        threadsPool()
    else:
        tdp.comprobar_url(url_box.get())
        s_down()

    
    


class threadsPool():

    '''
        La clase empieza obteniendo el contenido de la caja de texto
        posteriormente trae las URL'S en una lista la cual se divide
        en dos listas y se llaman a dos hilos a descargar las canciones.
    '''

    def __init__(self):

        self.verification = 0

        self.enlaces = tdp.get_linkpl(url_box.get())

        self.start_download()

    def start_download(self):
        
        self.lista_1 = self.enlaces[0:int(len(self.enlaces)/2)]
        self.lista_2 = self.enlaces[int(len(self.enlaces)/2):]
        
        self.refers()

    def down_convert(self, listas):


        for link in listas:
                        
            label_comp['text'] = f'Descargando {link}'
            tdp.download_aud(ref_url=link)
            tdp.convert_aud(aud_ext=link)
            label_comp['text'] = f'Descargado {tdp.get_name(link_vid=link)}'

        self.verification += 1        
        
        label_comp['text'] = f'La lista {self.verification} de 2 se ha descargado.'
                

    def refers(self):

        t = td(name='lista 1', target=self.down_convert, args=(self.lista_1,))
        d = td(name='lista 2', target=self.down_convert, args=(self.lista_2,))

        t.start()
        d.start()

        t.join()
        d.join()


def s_down():

    link = url_box.get()
    label_comp['text'] =  'Iniciando descarga'
    tdp.download_aud(link)
    tdp.convert_aud(link)
    label_comp['text'] = f'({tdp.get_name(link)}) Descargado con exito.'
    




# Ventana
root = tk.Tk()
root.geometry('800x600')
frame = tk.Frame(root)
frame.pack

# Cuadro para ingresar url
url_box = tk.Entry(root, width = 65)
url_box.pack()


label_url = tk.Label(root, font = 'Helvetica 20', text = 'Ingresa Url')
label_url.pack()

label_comp = tk.Label(root, font = '20')
label_comp.pack(pady=20)

label_name = tk.Label(root, font=1, text='Created by: Mitzuka')
label_name.pack(side=tk.BOTTOM)

label_ver = tk.Label(root, font=1, text='Beta Version')
label_ver.pack(side=tk.BOTTOM)

dload_button = tk.Button(
    root, text = 'Descarga!', command = lambda: td(target=comprobar).start()
)
dload_button.pack(pady=20)

img_paypal = tk.PhotoImage(file=path_imgDonate)

def ars():
    labelprueba.config(text='You clicked the button... :D')


donate_button = tk.Button(root, image=img_paypal, command=ars)
donate_button.pack(pady=20)

labelprueba = tk.Label(root, text='')
labelprueba.pack(pady=20)

root.title('TubeDoPy')
root.mainloop()