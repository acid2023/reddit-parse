from praw_utils import reddit_authorization, getting_comments_from_submission
from utils import get_top_authors_counts, get_cut_timestamp, print_fancy_top

reddit = reddit_authorization()
rate_limit = reddit.auth.limits

subreddit_name = 'news'
print('Connecting to reddit...')
subreddit = reddit.subreddit(subreddit_name)
print('Connected to reddit!')
submissions = subreddit.new(limit=10000)
print(f'Retrieving new submissions from subreddit "{subreddit_name}"...')
new_posts = list(submissions)
print('New submissions retrieved!')
print('Total new posts: ', len(new_posts))

submissions = []
days_ago = 3

query_timestamp = get_cut_timestamp(days_ago)

print(f'Selecting submissions that {days_ago} days old or less ...')
for post in new_posts:
    if post.created_utc >= query_timestamp:
        submissions.append(post)
print('Submissions selected!')

total = len(submissions)
print(f'Total {total} submissions selected.')

print('Parsing submissions for comments...')
query_comments_list = []
for idx, submission in enumerate(submissions):
    submission_comments_list = []
    submission_comments_list = getting_comments_from_submission(submission)
    query_comments_list += submission_comments_list
    print(f'Retrieved {len(submission_comments_list):<4}\tcomments from submission {idx+1} / {total:<3},',
          f'\t total comments\t {len(query_comments_list):>6}')

print('All submissions parsed')
print('Total comments retrieved: ', len(query_comments_list))

top_authors = get_top_authors_counts(submissions, 'author')
top_commenters = get_top_authors_counts(query_comments_list, 'author')

top_num = 10
print(f'\n\n Top {top_num} authors for last {days_ago} days:\n')
print_fancy_top(top_authors, top_num)

print(f'\n\n Top {top_num} comentators in all submissions for last {days_ago} days:\n')
print_fancy_top(top_commenters, top_num)
