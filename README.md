Working with reddit is based on module PRAW (Python Reddit API Wrapper)
Official site for this module is https://praw.readthedocs.io/

In order to start working with this module you shall get authorization from reddit - SECRET key and client_id key
Details of registration and obtaining these can be found on https://www.reddit.com/r/redditdev/comments/hasnnc/where_do_i_find_the_reddit_client_id_and_secret/

In my script this dta is specified in reddit_APY_secret.py which is not on the repo
Content is provided in file called reddit_API_.py - just rename it (add secret at the end of filename, but bobviously efore extension) and enter your personal data

Once these strings are avaialable - we can connect to reddit

Important nore!!! - there is request limit in reddit API (600 request in 10 minutes or so) and when it is exceeded there is great chance that you wiull get HTTP error 429, you can check the status requesting .auth.limits property of Reddit instance. It would return data in format:
{'remaining': int or None, 'reset_timestamp': timastamp or None, 'used': int or None} - once remaining is zero it would start making errors.

There is some ambiguity in the way praw and reddit deal with this requests limit - some times it is None and nothing happens at all, for some opertaions one request may generate multiple entries for some each entry is of requerst (i will elaborate on this later)

Getting the necessary subredeit (section ) is straightforward - Reddit.subreddit(subreddit_name) - this would return Subreddit instance
from subreddit to submissions (or threads within the subreddit) is almost straightforward as well - there several methods available< all with limit keyword - IMPORTANT!!! the resulting submissions are limited to 1000!!!! if limit=None and this is limitation of praw and reddit!!!
I am using .new(limit=None) to get submissions, for other variants see the Subreddit description https://praw.readthedocs.io/en/stable/code_overview/models/subreddit.html#

Once all possible submission within subreddit of interest are pulled, I compare there creation data (.created_utc property as timestamp) with requested date and generate list of submissions meeting the criterion.

For each submission (Submission class) I explore the its comments - Submission.comments result in instance of CommentForest, which can be expanded by .list() method to List of comments that are either Comment instances or MoreComments instances (which is effectively another forest of comments / replies)

To explore comments treee for each submission there are two ways possible:
    - flattening list of comments by Submission.comments.list() method and ignore potential MoreComments subtrees, or
    - recurrently unfold each  MoreComments instance to list of comments (some of these again may be MoreComments instances) by using .comment property/method for MoreComments insance if necessary.

The second method is quite time consuming, but result in additional comments (circa several times more). Also it is possible to increase level of exploration by combining .list() and recurrency. 

Thus in my function getting_comments_from_submission I am using combintaion:
    - if keyword 'recurrent' is True - fully recurrent exploration of comments
    - if 'recurrent' is false - I generate list of comments for each submission (by .comments.list() metghod) and several time make substitution of each instance of MoreComments to CommentForest. 
    By default 3 cycles but any way up to the point no more new comments appear. From my experiments 3 cycles is enough to get to the same level as full recurrent.

I also made some experiments checking time it takes for execution and number of comments revealed for different combinations of reccurent and flat methods. Also I used pure_flat method - that is just once return .comments.list() results. For that purpose I used decorator function - @measure_time/

My results for subreddit - news, number of submissions explored 10:
    - non recurrent, non flat - 611 comments for 23.6 seconds
    - non recurrent, flat - 3202 comments for 412.6 seconds
    - recurrent, non flat (we start from normal commsnts list) - 711 comments for 33.6 seconds
    - recurrent, flat - 3302 comments for 253.2 seconds
    - pure flat (just once .comments.list()) - 2185 comments for 21.6 seconds. 

For homework assignment I am using pure_flat as the fastest method - though it doesn'produce all the comments, it is sufficient enough fore all homework assignment purposes. Once list of comments is produced, all comemnts that are of MoreComments instance are dropped as they have no author

For instance when I run script for 'news' subreddit for pure_flat configuration - I retrieved 11 145 comments for 95 seconds (1634 MoreComments subtrees were dropped), with just flat configuration (non recurrent, 3 cycles of expanding) I retrieved 17 474 comments for 1640 seconds (dropped 160 MoreComments).

It worth noting that Submisision instance does have property .num_commnets that gives the count of all comments in it, but it is always differ from what I get by exploring comment trees (any way) as some other comments are included in this count - for example deleted, banned, private and so forth.

    
Once i have list of all comments and list of submissions getting top authors is straightforward.

Both Submission instances and Comments istances have property field - .author that returns Redditor class instnace with field .name for author's name.

If author is None I ignored the comment without further investigations.

I make dicts that counts apearance of individual author (as key) and put its counts as value. Then dicts ate sortted on value fields and results are printed out with help of tabulate module.


