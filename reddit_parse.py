from praw.models import MoreComments  # type: ignore

from praw_utils import reddit_authorization, retrieveing_submissions, getting_comments_from_submission, select_submissions
from utils import get_top_authors_counts, get_fancy_top_table


def main() -> None:

    print('Starting script...')

    print('\nConnecting to Reddit ...')
    time_elapsed, reddit = reddit_authorization()
    print('\nConnected! Time elapsed: ', f'{time_elapsed:.6f}')

    subreddit_name = 'news'
    print(f'Selecting submissions from subreddit: "{subreddit_name}"')
    time_elapsed, submissions = retrieveing_submissions(reddit, subreddit_name)
    new_posts = list(submissions)
    total_posts = len(new_posts)
    print(f'\nNew submissions from subreddit "{subreddit_name}" retrieved!')
    print(f'\nTotal submissions retrieved: {total_posts}, \nElapsed time is {time_elapsed:.6f} seconds.')

    days_ago = 3
    time_elapsed, (submissions, num_count) = select_submissions(new_posts, days_ago=days_ago)
    total = len(submissions)

    print(f'\nSelected {total} out of {total_posts} submissions that are {days_ago} days old or less.',
          f'\nTime elapsed {time_elapsed:.6f} seconds.')

    print(f'\nTotal number of comments in all submissions as per praw Submission.num_comments property: {num_count}')

    print('\nParsing submissions for comments...')
    print(' ')

    query_comments_list = []
    time_elapsed = 0
    total_dropped = 0

    for idx, submission in enumerate(submissions):
        submission_comments_list = []
        time_elapsed_for_query, submission_comments_list = getting_comments_from_submission(submission, pure_flat=True, flat=True)
        time_elapsed += time_elapsed_for_query
        more_comments_droped_list = [comment for comment in submission_comments_list if not isinstance(comment, MoreComments)]
        number_droped = len(submission_comments_list) - len(more_comments_droped_list)
        total_dropped += number_droped
        query_comments_list += more_comments_droped_list
        print(f'Retrieved {len(more_comments_droped_list):<4}\tcomments from submission {idx+1} / {total:<3}',
              f'\tMoreComments instances dropped: {number_droped:<3}',
              f'\ttime elapsed {time_elapsed_for_query:.6f}{"":<3}',
              f'\ttotal comments\t {len(query_comments_list):>4}')

    print(f'\nAll submissions parsed, total time elapsed {time_elapsed:.6f} seconds.')

    print(f'\nTotal comments retrieved: {len(query_comments_list)}, total comments dropped: {total_dropped}')

    top_authors = get_top_authors_counts(submissions, 'author')
    top_commenters = get_top_authors_counts(query_comments_list, 'author')

    top_num = 10
    print(f'\n\n Top {top_num} authors and top {top_num} commenters in all submissions for last {days_ago} days:\n')

    left_table = get_fancy_top_table(top_authors, top_num, header=f'Top {top_num} authors')

    right_table = get_fancy_top_table(top_commenters, top_num, header=f'Top {top_num} commenters')

    left_lines = left_table.split('\n')
    right_lines = right_table.split('\n')

    combined_lines = [f"{left_line}\t{right_line}" for left_line, right_line in zip(left_lines, right_lines)]

    for line in combined_lines:
        print(line)


if __name__ == '__main__':
    main()
