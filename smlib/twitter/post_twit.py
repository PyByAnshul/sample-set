import requests
import json
from globals import log as logging
from smlib.twitter.utils import headers,cookies

false = False
null = None
true = True

def main(summary):
    """
    Create and post a tweet using the provided summary.

    Args:
        summary (str): The text of the tweet.
    """
    try:
        # Construct the payload for the tweet
        data = json.dumps(
            {
                "variables": {
                    "tweet_text": f"{summary}",
                    "dark_request": False,
                    "media": {"media_entities": [], "possibly_sensitive": False},
                    "semantic_annotation_ids": [],
                    "conversation_control": {"mode": "ByInvitation"},
                    "disallowed_reply_options": None,
                },
                "features": {
                    "premium_content_api_read_enabled": False,
                    "communities_web_enable_tweet_community_results_fetch": True,
                    "c9s_tweet_anatomy_moderator_badge_enabled": True,
                    "responsive_web_grok_analyze_button_fetch_trends_enabled": False,
                    "responsive_web_grok_analyze_post_followups_enabled": True,
                    "responsive_web_jetfuel_frame": False,
                    "responsive_web_grok_share_attachment_enabled": True,
                    "responsive_web_edit_tweet_api_enabled": True,
                    "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
                    "view_counts_everywhere_api_enabled": True,
                    "longform_notetweets_consumption_enabled": True,
                    "responsive_web_twitter_article_tweet_consumption_enabled": True,
                    "tweet_awards_web_tipping_enabled": False,
                    "responsive_web_grok_analysis_button_from_backend": True,
                    "creator_subscriptions_quote_tweet_preview_enabled": False,
                    "longform_notetweets_rich_text_read_enabled": True,
                    "longform_notetweets_inline_media_enabled": True,
                    "profile_label_improvements_pcf_label_in_post_enabled": True,
                    "rweb_tipjar_consumption_enabled": True,
                    "responsive_web_graphql_exclude_directive_enabled": True,
                    "verified_phone_label_enabled": True,
                    "articles_preview_enabled": True,
                    "rweb_video_timestamps_enabled": True,
                    "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                    "freedom_of_speech_not_reach_fetch_enabled": True,
                    "standardized_nudges_misinfo": True,
                    "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
                    "responsive_web_grok_image_annotation_enabled": False,
                    "responsive_web_graphql_timeline_navigation_enabled": True,
                    "responsive_web_enhance_cards_enabled": False,
                },
                "queryId": "UYy4T67XpYXgWKOafKXB_A",
            }
        )

        # API endpoint and request
        response = requests.post(
            "https://x.com/i/api/graphql/UYy4T67XpYXgWKOafKXB_A/CreateTweet",
            headers=headers,
            cookies=cookies,
            data=data,
        )

        # Log response status
        logging.info(f"Tweet post response status: {response.status_code}")
        response.raise_for_status()  # Raise an exception for HTTP errors

    except requests.exceptions.RequestException as e:
        # Handle HTTP and request exceptions
        logging.error(f"HTTP request failed: {e}")

    except Exception as e:
        # Handle unexpected errors
        logging.error(f"An unexpected error occurred: {e}")
