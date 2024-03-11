from datetime import datetime, timedelta

from praw import Reddit  # type: ignore
from praw.models import Comment, MoreComments, Submission, Redditor  # type: ignore

import reddit_API_secret as SECRET
from measure_time import measure_time


@measure_time
def reddit_authorization() -> Reddit:
    reddit = Reddit(
        client_id=SECRET.client_id,
        client_secret=SECRET.SECRET,
        user_agent='acid2023',)
    return reddit


@measure_time
def getting_comments_from_submission(submission: Submission, cycles=3, recucurrent=False, flat=False, pure_flat=False) -> list[Comment]:
    def get_comments_from_more_comments(some_comment: Comment | MoreComments) -> list[Comment | MoreComments]:
        if isinstance(some_comment, Comment):
            return [some_comment]
        else:
            more_comments = some_comment.comments()
            comments_list: list[Comment | MoreComments] = []
            for comment in more_comments:
                comments_list += get_comments_from_more_comments(comment)
            return comments_list

    def substitute_more_comments(comments_list: list[Comment | MoreComments]) -> list[Comment | MoreComments]:
        new_comments_list = []
        for comment in comments_list:
            if isinstance(comment, MoreComments):
                comments = comment.comments()
            else:
                comments = [comment]
            new_comments_list += comments
        return new_comments_list

    if pure_flat:
        return submission.comments.list()

    if flat:
        submission_comments_list = submission.comments.list()
    else:
        submission_comments_list = submission.comments

    if not recucurrent:
        comments_list = submission_comments_list
        for _ in range(cycles):
            comments = substitute_more_comments(comments_list)
            if comments == comments_list:
                break
            comments_list = comments
        return comments_list

    else:

        comments_list = []

        for comment in submission_comments_list:
            comments_list += get_comments_from_more_comments(comment)

        return comments_list


def substitute_athor_name(author: Redditor | str) -> str:
    if isinstance(author, Redditor):
        return author.name
    else:
        return author


@measure_time
def retrieveing_submissions(reddit: Reddit, subreddit_name: str) -> list[Submission]:
    subreddit = reddit.subreddit(subreddit_name)
    submissions = subreddit.new(limit=10000)
    return submissions


@measure_time
def select_submissions(submissions: list[Submission], days_ago=3) -> tuple[list[Submission], int]:
    def get_cut_timestamp(days_period: int) -> int:
        current_time = datetime.utcnow()
        days_ago = current_time - timedelta(days=days_period)
        return int(days_ago.timestamp())

    query_timestamp = get_cut_timestamp(days_ago)
    query_submissions = []
    num_count = 0
    for submission in submissions:
        if submission.created_utc >= query_timestamp:
            query_submissions.append(submission)
            num_count += submission.num_comments

    return (query_submissions, num_count)
