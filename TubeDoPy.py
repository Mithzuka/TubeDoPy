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

    if not tdp.comprobar_url(url_box.get()) == True:
        label_info['text'] = 'Ingresa una URL valida'        
    elif '&list=' in url_box.get():
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
                        
            label_info['text'] = f'Descargando {link}'
            tdp.download_aud(ref_url=link)
            tdp.convert_aud(aud_ext=link)
            label_info['text'] = f'Descargado {tdp.get_name(link_vid=link)}'

        self.verification += 1        
        
        label_info['text'] = f'La lista {self.verification} de 2 se ha descargado.'
                

    def refers(self):

        t = td(name='lista 1', target=self.down_convert, args=(self.lista_1,))
        d = td(name='lista 2', target=self.down_convert, args=(self.lista_2,))

        t.start()
        d.start()

        t.join()
        d.join()


def s_down():

    link = url_box.get()
    label_info['text'] =  'Iniciando descarga'
    tdp.download_aud(link)
    tdp.convert_aud(link)
    label_info['text'] = f'({tdp.get_name(link)}) Descargado con exito.'
    




# Ventana
root = tk.Tk()
root.geometry('800x600')
frame = tk.Frame(root)
frame.pack

# Cuadro para ingresar url
url_box = tk.Entry(root, width = 65)
url_box.pack()

# Etiqueta url
label_url = tk.Label(root, font = 'Helvetica 20', text = 'Ingresa Url')
label_url.pack()

# Etiqueta informativa
label_info = tk.Label(root, font = '20')
label_info.pack(pady=20)

# Boton Descarga
dload_button = tk.Button(
    root, text = 'Descarga!', command = lambda: td(target=comprobar).start()
)
dload_button.pack(pady=20)

# Imagen Donacion
try:
    img_paypal = tk.PhotoImage(file=path_imgDonate)    
except:
    img_paypal = None

# Boton Donacion
donate_button = tk.Button(root, image=img_paypal, text='Donar', command= lambda: os.system("start \"\" https://www.paypal.com/donate/?hosted_button_id=Q5C7GNUUAKBSJ"))
donate_button.pack(pady=20)

# Creador
label_name = tk.Label(root, font=1, text='Created by: Mitzuka')
label_name.pack(side=tk.BOTTOM)

# Version
label_ver = tk.Label(root, font=1, text='Beta Version')
label_ver.pack(side=tk.BOTTOM)

root.title('TubeDoPy')
root.mainloop()