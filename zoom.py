import csv
import string
import time
from datetime import datetime
import urllib.parse
import requests

class Zoom:
    def __init__(self, lti_scid: str = None):
        self.base_url = 'https://applications.zoom.us'
        self.lti_scid = lti_scid if lti_scid else input(f"Enter lti_scid\n")
        self.csrf_token = None
        self.session_id = None
        self.cookies = None
        self.set_cookies()
        self.headers = self.set_headers()

    def set_headers(self):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': '*/*',
            'User-Agent': 'Snuffles v1.1'
        }
        self.csrf_token = input('Enter csrf_token\n')
        headers.update({'X-XSRF-TOKEN': self.csrf_token})
        return headers

    def set_cookies(self):
        self.session_id = input('Enter session_id\n')
        self.cookies = {'app_zm_cluster': 'aw1', 'app_zm_haid': '494', 'app_zm_cookie_enable': 'true',
                       'SESSION': self.session_id}

    def get_recording_files(self, meeting_id: string):
        url = f'{self.base_url}/api/v1/lti/rich/recording/file?meetingId={meeting_id}&lti_scid={self.lti_scid}'
        return requests.get(url, headers=self.headers, cookies=self.cookies)

    # end_time example : 2023-02-26
    def get_recording_list_of_course(self, end_time, page_number):
        url = f'{self.base_url}/api/v1/lti/rich/recording/COURSE?startTime=&endTime={end_time}&keyWord=&searchType=1&status=&page={page_number}&total=0&lti_scid={self.lti_scid}'
        return requests.get(url, headers=self.headers, cookies=self.cookies)

    def get_rows(self, meeting_list: list):
        rows = []
        print(f"{len(meeting_list)} items in the list")
        for meeting in meeting_list:
            recording_files_res = self.get_recording_files(urllib.parse.quote(meeting.get('meetingId')))
            result = recording_files_res.json().get('result')
            if result:
                recording_files = result.get('recordingFiles')
                for file in recording_files:
                    if file.get('fileType') == 'MP4':
                        #    convert datetime strings to datetime objects
                        start_date = datetime.strptime(file.get('recordingStart'), '%Y-%m-%d %H:%M:%S')
                        end_date = datetime.strptime(file.get('recordingEnd'), '%Y-%m-%d %H:%M:%S')
                        # calculate time difference
                        time_diff = end_date - start_date
                        url = file.get('playUrl')
                        topic = meeting.get('topic')
                        # recording_date = file.get('recordingStart').split(' ')[0]
                        recording_date = f"{start_date.date().__str__()} ({start_date.strftime('%A')})"
                        time_range = f"{file.get('recordingStart').split(' ')[1]} - {file.get('recordingEnd').split(' ')[1]}"
                        row = [topic, recording_date, time_range, time_diff.__str__(), url]
                        rows.append(row)
                        print(f"Got {len(rows)} rows")
                        # break
            else:
                print(f"No recording file {recording_files_res.text if recording_files_res.text else ''}")
            time.sleep(0.2)
        return rows

    def get_meeting_list(self, page_num: int = 1):
        meeting_list = []
        while True:
            try:
                response = self.get_recording_list_of_course(today_date, page_num)
                result = response.json().get('result')
                if not result:
                    break
            except Exception as e:
                print(f"An error occurred. {e}")
                break

            if result:
                if result.get('list'):
                    current_page = result.get('list')
                    meeting_list += current_page
                    print(f"Got total {result.get('toIndex')    } recording")
                if result.get('toIndex') >= result.get('total'):
                    break
            page_num += 1
        return meeting_list

def write_to_csv(file_name, fields, rows):
    with open(f'{file_name}', 'w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(fields)
        csv_writer.writerows(rows)


if __name__ == '__main__':
    zoom = Zoom()
    today_date = datetime.strftime(datetime.now(), '%Y-%m-%d')
    meeting_ls = zoom.get_meeting_list()
    if meeting_ls:
        zoom_rows = zoom.get_rows(meeting_ls)
        csv_fields = ['Topic', 'Date', 'Time Range', 'Total', 'Play URL']
        course_name = input('Enter Name of the course\n')
        write_to_csv(f"{datetime.now().date()}_{course_name}_ZRecs.csv", csv_fields, zoom_rows)
