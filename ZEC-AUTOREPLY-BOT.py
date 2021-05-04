#!/usr/bin/env python3
from urllib.parse import quote_plus
import os
import praw

QUESTIONS = ["how does", "how is", "how will",  "when does", "when is", "when will", "why does", "why is", "why wont", "why won't", "what is", "who is", "what are"]
REPLY_TEMPLATE = "[Great question, This is what I've found for you](https://lmgtfy.app/#gsc.tab=0&gsc.q={})"


def main():
    reddit = praw.Reddit(
        user_agent="LMGTFY (by u/ZEC-AUTOREPLY)",
        client_id=os.environ.get('ZEC_ARB_ID'),
        client_secret=os.environ.get('ZEC_ARB_SECRET'),
        username=os.environ.get('ZEC_ARB_USER'),
        password=os.environ.get('ZEC_ARB_PASS')
    )

    subreddit = reddit.subreddit("zec")
    for submission in subreddit.stream.submissions():
            process_submission(submission)
    

def process_submission(submission):
    # Ignore titles with more than 10 words as they probably are not simple questions.
    if len(submission.title.split()) > 10:
        return

    normalized_title = submission.title.lower()
    for question_phrase in QUESTIONS:
        if question_phrase in normalized_title:
            url_title = quote_plus(submission.title)
            reply_text = REPLY_TEMPLATE.format(url_title)
            print(f"Replying to: {submission.title}")
            print(reply_text)
            submission.reply(reply_text)
            # A reply has been made so do not attempt to match other phrases.
            break


if __name__ == "__main__":
    main()
