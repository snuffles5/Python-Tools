import os
from time import sleep
from dotenv import dotenv_values
import requests


class Tomp3_youtube:
    def __init__(self):
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
        download_response = requests.get(download_url)
        open(file_name, "wb").write(download_response.content)

    def download_youtube_files(self, urls, type: str, bitrate: str, folder):
        i = 1
        if type == 'mp4':
            bitrate = 'auto'
        for url in urls:  # TODO async
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
        self.config = dotenv_values('.env')
        self.api_key = self.config['YOUTUBE_API_KEY']
        self.set_headers()

    def set_headers(self):
        self.headers = {
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
        for file in os.listdir(folder):
            # Checking if the file is present in the list
            # if file in files_to_rename:
            # construct current name using file name and path
            print(f'file {file}')
            for idx, name in enumerate(list_of_names):
                if name in file:
                    old_name = os.path.join(folder, file)
                    # get file name without extension
                    extension = os.path.splitext(file)[1]
                    new_name = f'{idx + 1} - {name}'
                    # Adding the new name with extension
                    new_base = f'{new_name}_new{extension}'
                    print(f'new_base {new_base}')
                    # construct full file path
                    new_name = os.path.join(folder, new_base)
                    # Renaming the file
                    os.rename(old_name, new_name)


if __name__ == '__main__':
    config = dotenv_values('.env')
    tomp3 = Tomp3_youtube()
    files = Files()

    type = 'mp4'
    bitrate = '256'
    folder = config['FOLDER']
    youtube_links = ['https://youtu.be/dZk3ilr9rqA']
    files.print_all_files(config['PRINT_ALL_FILES'])