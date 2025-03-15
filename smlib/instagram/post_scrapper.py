import requests
import json
from globals import db
from globals import log as logging
from smlib.instagram.comments_section_scrapper import main as comment_main
from concurrent.futures import ThreadPoolExecutor
import traceback

false = False
true = True
null = None

cookies = {
    "datr": "1yLPZyQdqsVWKhxfJ3etYblS",
    "ig_did": "64C6ABA3-0BF7-4AD2-ABCF-DB524BE4D625",
    "mid": "Z88i1wAEAAEJXoE0dQXc9N55N-Sm",
    "ps_l": "1",
    "ps_n": "1",
    "ig_nrcb": "1",
    "csrftoken": "Z8vIqzSNs2QfxrwftfemBNc5qvxP9M2g",
    "ds_user_id": "73261147875",
    "sessionid": "73261147875%3AV1ewSzZkLHLE1g%3A20%3AAYdPKhpI07sCrKsJWw7AE0E-RN5U_9DLp33osQnJ9g",
}

headers = {
    "accept": "*/*",
    "content-type": "application/x-www-form-urlencoded",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
}


data = {
    "av": "17841473316257643",
    "__d": "www",
    "__user": "0",
    "__a": "1",
    "__req": "16",
    "__hs": "20161.HYP:instagram_web_pkg.2.1...1",
    "dpr": "1",
    "__ccg": "GOOD",
    "__rev": "1020884751",
    "__s": "nhz7a2:1zkp03:pey3uj",
    "__hsi": "7481501639145956526",
    "__dyn": "7xeUjG1mxu1syUbFp41twpUnwgU7SbzEdF8aUco2qwJxS0DU2wx609vCwjE1EE2Cw8G11wBz81s8hwGxu786a3a1YwBgao6C0Mo2swtUd8-U2zxe2GewGw9a361qw8Xxm16wUwtE1wEbUGdG1QwTU9UaQ0Lo6-3u2WE5B08-269wr86C1mwPwUQp1yUb8jK5V8aUuwm8jxK2K0P8KmUhw",
    "__csr": "hsgwhgjjgJNYInlYghkDFbFTPOjRIFVqLZb-AiapeDLFzqALxlQl4yvl9t2i9agDV2C_JeW88UyVVAQh7pVEHKUCh26u8DByVtoLDArh8C8Xu8zEG7QUSdUtzRBz9ut2pp8Odz4pad_Az8-tudyaBBy4m2-ayEO446Uyby8S8goCglw04Mug0M0E1aEWlo2vw9V1Eg3q3nww4Dgx5g1d87S5UVwxiw5Jw6Nw1wW0D436l0dN6Bwzze08Sgqwzqx2xhDp9E1po47wm-0zcM3JFa9x65k26444Umw1XEE05DS0tO0aFw",
    "__hsdp": "",
    "__hblp": "",
    "__comet_req": "7",
    "fb_dtsg": "NAcMYzNHrFDvoFrFUhAzzXtOWONzv1cWzlDr2Ce3qkXYQPGOk_DuAVA:17843708194158284:1741920441",
    "jazoest": "26432",
    "lsd": "uwxjHqSt9pyPpkJQZl4xAp",
    "__spin_r": "1020884751",
    "__spin_b": "trunk",
    "__spin_t": "1741922842",
    "fb_api_caller_class": "RelayModern",
    "fb_api_req_friendly_name": "PolarisProfilePostsTabContentQuery_connection",
    "variables": '{"after":"3586777480276842763_16278726","before":null,"data":{"count":12,"include_reel_media_seen_timestamp":true,"include_relationship_info":true,"latest_besties_reel_media":true,"latest_reel_media":true},"first":12,"last":null,"username":"bbcnews","__relay_internal__pv__PolarisIsLoggedInrelayprovider":true,"__relay_internal__pv__PolarisShareSheetV3relayprovider":true}',
    "server_timestamps": "true",
    "doc_id": "28584433827869438",
}


def main():
    try:
        while True:
            logging.info("Sending request to Instagram API")
            response = requests.post(
                "https://www.instagram.com/graphql/query",
                headers=headers,
                cookies=cookies,
                data=data,
            )

            if response.status_code == 200:
                res_data = response.json()
                logging.info("Data received successfully")

                video_data = []
                try:
                    for video in res_data["extensions"][
                        "all_video_dash_prefetch_representations"
                    ]:
                        for rep in video["representations"]:
                            video_data.append(
                                {
                                    "video_id": video["video_id"],
                                    "base_url": rep["base_url"],
                                    "bandwidth": rep["bandwidth"],
                                    "width": rep["width"],
                                    "height": rep["height"],
                                    "representation_id": rep["representation_id"],
                                }
                            )
                            db.post.find_one_and_update(
                                {"post_id": video["video_id"]},
                                {
                                    "$set": {
                                        "video_id": video["video_id"],
                                        "base_url": rep["base_url"],
                                        "bandwidth": rep["bandwidth"],
                                        "width": rep["width"],
                                        "height": rep["height"],
                                        "representation_id": rep["representation_id"],
                                    }
                                },
                                upsert=True,
                            )
                    logging.info(f"{len(video_data)} videos processed")

                except KeyError as e:
                    logging.error(f"Key error while processing video data: {e}")
                except Exception as e:
                    traceback.print_exc()
                    logging.error(f"Unexpected error processing video data: {e}")

                with ThreadPoolExecutor(max_workers=2) as executor:
                    futures = [
                        executor.submit(comment_main, video.get("video_id"))
                        for video in video_data
                        if video.get("video_id")
                    ]

                    for future in futures:
                        try:
                            future.result()
                        except Exception as e:
                            logging.error(f"Error processing video comments: {e}")

                edge = res_data["data"][
                    "xdt_api__v1__feed__user_timeline_graphql_connection"
                ]["page_info"]
                if edge["has_next_page"]:
                    node_id = edge["end_cursor"]
                else:
                    logging.info("All pages scraped successfully")
                    break

                data["variables"] = json.dumps(
                    {
                        "after": f"{node_id}",
                        "before": null,
                        "data": {
                            "count": 12,
                            "include_reel_media_seen_timestamp": true,
                            "include_relationship_info": true,
                            "latest_besties_reel_media": true,
                            "latest_reel_media": true,
                        },
                        "first": 12,
                        "last": null,
                        "username": "bbcnews",
                        "__relay_internal__pv__PolarisIsLoggedInrelayprovider": true,
                        "__relay_internal__pv__PolarisShareSheetV3relayprovider": true,
                    }
                )

            else:
                logging.warning(
                    f"Failed to fetch data: Status code {response.status_code}"
                )
                break

    except requests.RequestException as e:
        logging.error(f"Request failed: {e}")
    except json.JSONDecodeError as e:
        logging.error(f"Failed to parse JSON response: {e}")
    except Exception as e:
        logging.critical(f"Critical error: {e}", exc_info=True)


if __name__ == "__main__":
    main()
