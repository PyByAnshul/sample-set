import requests
from requests.exceptions import RequestException, JSONDecodeError
from globals import db
from globals import log as logging
# Cookies and headers
cookies = {
    'datr': '1yLPZyQdqsVWKhxfJ3etYblS',
    'ig_did': '64C6ABA3-0BF7-4AD2-ABCF-DB524BE4D625',
    'mid': 'Z88i1wAEAAEJXoE0dQXc9N55N-Sm',
    'ps_l': '1',
    'ps_n': '1',
    'ig_nrcb': '1',
    'csrftoken': 'Z8vIqzSNs2QfxrwftfemBNc5qvxP9M2g',
    'ds_user_id': '73261147875',
    'sessionid': '73261147875%3AV1ewSzZkLHLE1g%3A20%3AAYdPKhpI07sCrKsJWw7AE0E-RN5U_9DLp33osQnJ9g',
    'wd': '1920x451',
    'rur': 'EAG\\05473261147875\\0541773464030:01f7f5bdcf18de1bbed5040a9913e7fb2a4a31da041013dd73e383a6e46c44757faa5fb4',
}

headers = {
    'accept': '*/*',
    'accept-language': 'en-GB,en;q=0.9',
    'priority': 'u=1, i',
    'referer': 'https://www.instagram.com/bbcnews/reel/DHJmvTrNKpm/',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Brave";v="134"',
    'sec-ch-ua-full-version-list': '"Chromium";v="134.0.0.0", "Not:A-Brand";v="24.0.0.0", "Brave";v="134.0.0.0"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Linux"',
    'sec-ch-ua-platform-version': '"6.11.0"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    'x-asbd-id': '359341',
    'x-csrftoken': 'Z8vIqzSNs2QfxrwftfemBNc5qvxP9M2g',
    'x-ig-app-id': '936619743392459',
    'x-ig-www-claim': 'hmac.AR2YdKNfXyW0Qveoly0eo3v2o_Gy8J8azEsmjK7I9nsPN2IK',
    'x-requested-with': 'XMLHttpRequest',
    'x-web-session-id': '0efz8j:mqrt72:uoxvs0',
}

def main(video_id):
    if not video_id:
        logging.warning("No video_id provided")
        return

    url = f'https://www.instagram.com/api/v1/media/{video_id}/comments/'
    params = {
        'can_support_threading': 'true',
        'permalink_enabled': 'false',
    }

    try:
        logging.info(f"Fetching comments for video_id: {video_id}")
        response = requests.get(url, headers=headers, params=params, cookies=cookies)
        response.raise_for_status()  # Raises an error for non-2xx responses
        
        try:
            res_data = response.json()
            caption = res_data.get("caption", {}).get("text")
            if caption:
                db.post.find_one_and_update({'video_id': video_id}, {'$set': {'caption': caption}})
                logging.info(f"Caption updated for video_id: {video_id}")
            else:
                logging.warning(f"No caption found for video_id: {video_id}")
        except JSONDecodeError:
            logging.error(f"Failed to parse JSON response for video_id: {video_id}")
        
    except RequestException as e:
        logging.error(f"Request failed for video_id: {video_id} - {e}")
