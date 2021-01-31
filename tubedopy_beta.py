from pytube import YouTube as yt
from pytube.contrib.playlist import Playlist as pl
import pytube
import os 
import googleapiclient.discovery
from urllib.parse import parse_qs, urlparse

'''
    Autor: Mithzuka (Daniel Velazquez)
    Nombre: TubeDoPy
    Version: Beta (0.1) 
    Fecha salida: 31/01/2021

    Actualmente el programa esta hecho para descargar unicamente audio en la mejor calidad
    posible y de YouTube solamente.
    Para poder usar bien este programa necesitas las 
    siguientes librerias:
                          - pip install pytube
                          - pip3 install --upgrade google-api-python-client
                            (En este link explica el uso y como conseguir la clave: 
                            https://stackoverflow.com/questions/62345198/extract-individual-links-from-a-single-youtube-playlist-link-using-python)

    Cualquier duda o comentario favor de mandarlo a mi correo git
    


    Recuerda: Si te gusta la app y quieres que siga mejorandola no olvides donar. 
              Si te gusta lo que descargas apoyalos comprando su contenido oficial.
'''



class tubedopy():

    def __init__(self):
        
        self.path = os.path.expanduser('~').replace('\\', '/')
        self.path += '/Music/TubeDoPy'

        while True:
            try:
                os.chdir(self.path)
                break
            except FileNotFoundError:
                os.mkdir(self.path)
        
    def comprobar_url(self, url=None):

        self.url = url

        if '&list' in url:
            try:
                self.plist = pl(self.url)
                return True
            except:
                return 'Error: Url no valido'
        else:
            try:
                self.list = yt(self.url)
                return True
            except pytube.exceptions.RegexMatchError:
                return 'Error: URL no valido'
    
    def download_aud(self, ref_url=None):

        try:
            self.ref_url = ref_url
            stream = yt(self.ref_url)
            self.audio = stream.streams.order_by('abr').last()
            self.audio.download()
        except:
            return 'Error: URL no valido'

    def convert_aud(self, aud_ext=None):

        self.aud_ext = yt(aud_ext)
        self.act_ext = ''
        self.new_ext = self.aud_ext.title
        self.new_ext += '.mp3'

        for entry in os.scandir():
            if not entry.name.startswith('.') and entry.is_file():
                if self.aud_ext.title in entry.name:
                    self.act_ext = entry.name
                    break

        os.replace(self.act_ext, self.new_ext)

    def get_linkpl(self, ref_purl=None):

        #extract playlist id from url
        url = ref_purl
        query = parse_qs(urlparse(url).query, keep_blank_values=True)
        playlist_id = query["list"][0]

        print(f'get all playlist items links from {playlist_id}')
        youtube = googleapiclient.discovery.build("youtube", "v3", developerKey = "YOUR_API_KEY")

        request = youtube.playlistItems().list(
            part = "snippet",
            playlistId = playlist_id,
            maxResults = 50
        )
        response = request.execute()

        playlist_items = []
        while request is not None:
            response = request.execute()
            playlist_items += response["items"]
            request = youtube.playlistItems().list_next(request, response)

        pl_list = [ 
            f'https://www.youtube.com/watch?v={t["snippet"]["resourceId"]["videoId"]}&list={playlist_id}&t=0s'
            for t in playlist_items
        ]
        return pl_list

        
            
    def get_name(self, link_vid=None):

        self.link_vid = link_vid
        title = yt(self.link_vid)
        return title.title 