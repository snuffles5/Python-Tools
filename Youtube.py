import json
import os
import urllib
from time import sleep

from dotenv import dotenv_values

import requests

class Tomp3_youtube:
    def __init__(self):
        # self.url = 'https://tomp3.cc/api/ajax/search'
        self.set_headers()

    def set_headers(self):
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': '*/*',
            'User-Agent': 'Snuffles v1.1'
        }

    def search(self, youtube_link: str, type: str):
        # youtube_link.replace('https://www.youtube.com/watch?v=','')
        body = {
            'query': youtube_link,
            'vt': type
        }
        return requests.post(f'https://tomp3.cc/api/ajax/search', data=body,
                            headers=self.headers)

    def convert(self, vid: str, k: str):
        body = {
            'vid': vid,
            'k': k
        }
        return requests.post(f'https://tomp3.cc/api/ajax/convert', data=body,
                                    headers=self.headers)

    def download_file(self, download_url: str, file_name: str):
        download_response =  requests.get(download_url)
        open(file_name, "wb").write(download_response.content)

    def download_youtube_files(self, urls, type: str, bitrate: str, folder):
        i = 1
        if type == 'mp4':
            bitrate = 'auto'
        for url in urls: #TODO async
            search_res = self.search(url, type)
            vid = search_res.json()['vid']
            requested_object = search_res.json()['links'][type][bitrate]
            k = requested_object['k']
            convert_res = self.convert(vid, k)
            file_name = f'{convert_res.json()["title"]}.{type}'
            download_url = convert_res.json()['dlink']
            print(f'{i}) downloading {file_name}...')
            self.download_file(download_url, f'{folder}/{file_name}')
            i += 1

class Youtube:
    ENDPOINT = 'https://www.googleapis.com/youtube/v3'

    def __init__(self):
        # self.url = 'https://tomp3.cc/api/ajax/search'
        self.config = dotenv_values('.env')
        self.api_key = self.config['YOUTUBE_API_KEY']
        self.set_headers()

    def set_headers(self):
        self.headers = {
            # 'Content-Type': 'application/json',
            'Accept': '*/*',
            'User-Agent': 'Snuffles v1.1'
        }

    def get_playlist_links(self, playlist_id: str):
        url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&playlistId={playlist_id}&key={self.api_key}"
        video_ids = []
        video_links = []
        while True:
            response = requests.get(url)
            videos = response.json()
            for video in videos['items']:
                video_id = video['contentDetails']['videoId']
                video_ids.append(video_id)
                video_link = f"https://www.youtube.com/watch?v={video_id}"
                video_links.append(video_link)
            if 'nextPageToken' in videos:
                url = f"{url}&pageToken={videos['nextPageToken']}"
                sleep(0.5)
            else:
                break
        return video_links


class Files:
    def print_all_files(self, folder: str):
        files = []
        for file in os.listdir(folder):
            files.append(file)
        files.sort()
        for file in files:
            print(file)

    def rename_files(self, folder: str, list_of_names):
        # /Users/deni/Downloads/sara-songs
        for file in os.listdir(folder):
            # Checking if the file is present in the list
            # if file in files_to_rename:
            # construct current name using file name and path
            print(f'file {file}')
            for idx, name in enumerate(list_of_names):
                # print(f'name {name}')

                if name in file:
                    old_name = os.path.join(folder, file)
                    # get file name without extension
                    extension = os.path.splitext(file)[1]
                    # print(f'extension {extension}')
                    # only_name = os.path.splitext(file)[0]
                    # print(f'only_name {only_name}')
                    new_name = f'{idx + 1} - {name}'
                    # print(f'new_name {new_name}')

                    # Adding the new name with extension
                    new_base = f'{new_name}_new{extension}'
                    print(f'new_base {new_base}')
            # construct full file path
                    new_name = os.path.join(folder, new_base)

            # Renaming the file
                    os.rename(old_name, new_name)


    # def rename_file(self, src_folder_path: str, dst_folder_path: str):
            # /Users/deni/Downloads/sara-songs
            # os.rename(src_folder_path, dst_folder_path, *, src_dir_fd=None, dst_dir_fd=None)



if __name__ == '__main__':
    tomp3 = Tomp3_youtube()
    type = 'mp4'
    bitrate = '256'
    folder = '/Users/deni/Downloads'
    # youtube_links = ['https://www.youtube.com/watch?v=AKi-yPiiAlQ', 'https://www.youtube.com/watch?v=AYEVjMFURC4', 'https://www.youtube.com/watch?v=Y0KxZz5k-RE', 'https://www.youtube.com/watch?v=COrqhqIcEuI', 'https://www.youtube.com/watch?v=ua2hB0SxKyM', 'https://www.youtube.com/watch?v=HpQtd-QD3Q4', 'https://www.youtube.com/watch?v=sKO2LLqL58I', 'https://www.youtube.com/watch?v=EU0cm1uil_M', 'https://www.youtube.com/watch?v=1qKXCP6bywQ', 'https://www.youtube.com/watch?v=GBGQO7gRTaI', 'https://www.youtube.com/watch?v=gP6PS-poyMg', 'https://www.youtube.com/watch?v=JqhuSUqkuBs', 'https://www.youtube.com/watch?v=PuEYOUJ7SuA', 'https://www.youtube.com/watch?v=8LcXXijE8yQ', 'https://www.youtube.com/watch?v=FKkT2vQ37CY', 'https://www.youtube.com/watch?v=hUK21JN8JX8', 'https://www.youtube.com/watch?v=8fR44uYsARo', 'https://www.youtube.com/watch?v=FHeTKM5i4CQ', 'https://www.youtube.com/watch?v=0Il2etmS7mA', 'https://www.youtube.com/watch?v=DgvmC-F5jsE', 'https://www.youtube.com/watch?v=Y5bbt872LA0', 'https://www.youtube.com/watch?v=MEJ5jgCaDhE', 'https://www.youtube.com/watch?v=_Rg9dgmRyrI', 'https://www.youtube.com/watch?v=lt0Go3f1F60', 'https://www.youtube.com/watch?v=3ivSCrzPYd4', 'https://www.youtube.com/watch?v=aaJbbzIR2xY', 'https://www.youtube.com/watch?v=vv7XTuK9Qd8', 'https://www.youtube.com/watch?v=guYz5MrJ_Ks', 'https://www.youtube.com/watch?v=gFr_nzUFsK0', 'https://www.youtube.com/watch?v=b4MOk9Rn9sc']
    # tomp3.download_youtube_files(youtube_links, type, bitrate)
    youtube_links = ['https://youtu.be/dZk3ilr9rqA']
    # tomp3.download_youtube_files(youtube_links, type, bitrate, folder)
    # names = ['בוא לריו' ,'הללויה' ,'ארץ-אילנית' ,'כאן נולדתי' ,'ארץ הצבר' ,'ברקים ורעמים' ,'חסקה / בוא אלינו לים' ,'אדוני ראש העיר' ,'קום והתהלך בארץ' ,'לעולם בעקבות השמש' ,'אלף כבאים' ,'אני ואתה' ,'הופה היי' ,'ארץ ישראל שלי' ,'אנשים טובים באמצע הדרך' ,'ברוש' ,'תתארו לכם' ,'איך שיר נולד' ,'ושוב נצאה אל הדרך' ,'גברת עם סלים' ,'עוד לא תמו כל פלאייך' ,'שלום לך ארץ נהדרת' ,'חורף' ,'אין לי ארץ אחרת' ,'חורשת האקליפטוס' ,'הדגל שלי' ,'גלשן' ,'נולדתי לשלום' ,'יש לי ציפור קטנה בלב' ,'בשנה הבאה' ,'שני חברים יצאו לדרך' ,'אצלנו בחצר']
    files = Files()
    files.print_all_files('/Users/deni/Documents/Study/Bsc/Year B/Probability/הרצאות אלעד עטיא')
    # files.rename_files(folder, names)

    # youtube = Youtube()
    # playlist_id = 'PLRgBdNZyw4h8a1tKxthKIPOMmuWltPbgF'
    # video_ids = youtube.get_playlist_links(playlist_id)
    # print(video_id


