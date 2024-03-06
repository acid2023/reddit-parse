from praw import Reddit  # type: ignore
from praw.models import Comment, MoreComments, Submission  # type: ignore

import reddit_API_secret as SECRET


def reddit_authorization() -> Reddit:
    reddit = Reddit(
        client_id=SECRET.client_id,
        client_secret=SECRET.SECRET,
        user_agent='acid2023',)
    return reddit


def getting_comments_from_submission(submission: Submission) -> list[Comment]:
    def get_comments_from_more_comments(some_comment: Comment | MoreComments) -> list[Comment | MoreComments]:
        if isinstance(some_comment, Comment):
            return [some_comment]
        else:
            more_comments = some_comment.comments()
            comments_list: list[Comment | MoreComments] = []
            for comment in more_comments:
                comments_list += get_comments_from_more_comments(comment)
            return comments_list

    submission_comments = submission.comments
    comments_list = []

    for comment in submission_comments:
        comments_list += get_comments_from_more_comments(comment)

    return comments_list
