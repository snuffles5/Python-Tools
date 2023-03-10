# app_zm_cluster=aw1; app_zm_aid=XCPs8LKBSSCBLQnqjnrl3w; app_zm_haid=494; app_zm_cookie_enable=true; SESSION=82ca7b79-9238-46a4-a68c-05f0a0c5600a
import csv
import os
import string
import time
from datetime import datetime
import browser_cookie3
import opener as opener
import json
from bs4 import BeautifulSoup
import urllib.parse

import requests


class Zoom:
    def __init__(self, use_cookie_jar: bool, lti_scid: str = None):
        self.use_cookie_jar = use_cookie_jar

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
        if self.use_cookie_jar:
            pass
        else:
            self.csrf_token = input('Enter csrf_token\n')
            headers.update({'X-XSRF-TOKEN': self.csrf_token})
        return headers

    def set_cookies(self):
        if self.use_cookie_jar:
            chrome_cookies = '/Users/deni/Library/Application Support/Google/Chrome/Profile 3/Cookies'
            self.cookies = browser_cookie3.chrome(chrome_cookies)
            self.set_headers()
        else:
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
                if result.get('list'):  # todo handle multiple pages
                    current_page = result.get('list')
                    meeting_list += current_page
                    print(f"Got total {result.get('toIndex')    } recording")
                if result.get('toIndex') >= result.get('total'):
                    break
            page_num += 1
        return meeting_list

    def lti_reach(self):
        payload2 = {
            'oauth_version': '1.0',
            'oauth_nonce': '23c3128d99dd954fea331d743c916810',
            'oauth_timestamp': '1678439080',
            'oauth_consumer_key': 'pebX4IQLQNeD4SrOiZdvgQ',
            'user_id': '57896',
            'lis_person_sourcedid': '302528989',
            'roles': 'Learner',
            'context_id': '17578',
            'context_label': '%D7%90%D7%9C%D7%92%D7%95%D7%A8%D7%99%D7%AA%D7%9E%D7%99%D7%9D+1+-+%D7%96%D7%95%D7%9D+%28%D7%AA%D7%A9%D7%A4%D7%92_%D7%90_60172%29+-+%D7%91%D7%95%D7%98%D7%9E%D7%9F',
            'context_title': '%D7%90%D7%9C%D7%92%D7%95%D7%A8%D7%99%D7%AA%D7%9E%D7%99%D7%9D+1+-+%D7%96%D7%95%D7%9D',
            'resource_link_title': '%D7%96%D7%95%D7%9D',
            'resource_link_description': '',
            'resource_link_id': '23422',
            'context_type': 'CourseSection',
            'lis_course_section_sourcedid': '%D7%AA%D7%A9%D7%A4%D7%92_%D7%90_60172_1259',
            'lis_result_sourcedid': '{"data":{"instanceid":"23422","userid":"57896","typeid":"5","launchid":806633511},"hash":"131dcc0ca3e26cfcf023b5f258f12f79c46610087db5138cdb3f4af7013f8e9e"}',
            'lis_outcome_service_url': 'https%3A%2F%2Fmd.hit.ac.il%2Fmod%2Flti%2Fservice.php',
            'lis_person_name_given': '%D7%93%D7%A0%D7%99%D7%90%D7%9C',
            'lis_person_name_family': '%D7%A2%D7%99%D7%A0%D7%99+%D7%A7%D7%A0%D7%93%D7%99%D7%9C',
            'lis_person_name_full': '%D7%93%D7%A0%D7%99%D7%90%D7%9C+%D7%A2%D7%99%D7%A0%D7%99+%D7%A7%D7%A0%D7%93%D7%99%D7%9C',
            'ext_user_username': '302528989',
            'lis_person_contact_email_primary': 'daniel.eni%40gmail.com',
            'launch_presentation_locale': 'he',
            'ext_lms': 'moodle-2',
            'tool_consumer_info_product_family_code': 'moodle',
            'tool_consumer_info_version': '2020061508.01',
            'oauth_callback': 'about%3Ablank',
            'lti_version': 'LTI-1p0',
            "lti_message_type": "basic-lti-launch-request",
            "tool_consumer_instance_guid": "md.hit.ac.il",
            "tool_consumer_instance_name": "Moodle HIT",
            "tool_consumer_instance_description": "%D7%94%D7%9E%D7%9B%D7%95%D7%9F+%D7%94%D7%98%D7%9B%D7%A0%D7%95%D7%9C%D7%95%D7%92%D7%99+-+%D7%97%D7%95%D7%9C%D7%95%D7%9F",
            "custom_course_id_method_type": "0",
            "launch_presentation_document_target": "iframe",
            "launch_presentation_return_url": "https%3A%2F%2Fmd.hit.ac.il%2Fmod%2Flti%2Freturn.php%3Fcourse%3D17578%26launch_container%3D3%26instanceid%3D23422%26sesskey%3D1nMU6dCZfh",
            "oauth_signature_method": "HMAC-SHA1",
            "oauth_signature": "HCrso3VYQrCny1Fx%2FpYwsKfL7YE%3D"
        }
        url = f"{self.base_url}/lti/rich"
        headers = {
            'Host': 'applications.zoom.us',
            'Connection': 'close',
            'Content-Length': '2097',
            'Cache-Control': 'max-age=0',
            'sec-ch-ua': '\"Not A(Brand\";v=\"24\", \"Chromium\";v=\"110\"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '\"macOS\"',
            'Upgrade-Insecure-Requests': '1',
            'Origin': 'https://md.hit.ac.il',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.78 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Dest': 'iframe',
            'Referer': 'https://md.hit.ac.il/',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9'
        }
        cookies = {
            '_zm_mtk_guid': 'aaddf5b7a79649dea3092172811c723c',
            '_zm_visitor_guid': 'aaddf5b7a79649dea3092172811c723c'
        }
        # res = requests.post(url, headers=self.headers, cookies=self.cookies, data=payload2)
        # tokens = self.get_from_response_html_text(res.text, 'token')
        # return res
        res2 = requests.post(url, headers=headers, cookies=cookies, data=payload2)
        # X_XSRF_TOKEN = self.get_from_response_html_text()
        # x_zm = self.get_from_response_html_text(res2.text, 'x-zm')
        return res2 if 'X-XSRF-TOKEN' in res2.text else None


def write_to_csv(file_name, fields, rows):
    with open(f'{file_name}', 'w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(fields)
        csv_writer.writerows(rows)


if __name__ == '__main__':

    res = None
    tempzoom = None
    try:
        tempzoom = Zoom(True)
        res = tempzoom.lti_reach()
    except Exception as e:
        print(e)
    zoom = Zoom(bool(res), tempzoom.lti_scid if tempzoom else None )

    today_date = datetime.strftime(datetime.now(), '%Y-%m-%d')

    meeting_ls = zoom.get_meeting_list()
    if meeting_ls:
        zoom_rows = zoom.get_rows(meeting_ls)
        csv_fields = ['Topic', 'Date', 'Time Range', 'Total', 'Play URL']
        course_name = input('Enter Name of the course\n')
        write_to_csv(f"{datetime.now().date()}_{course_name}_ZRecs.csv", csv_fields, zoom_rows)
