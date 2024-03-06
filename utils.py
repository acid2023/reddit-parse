from datetime import datetime, timedelta
from tabulate import tabulate

from praw.models import Comment, Submission, Redditor  # type: ignore


def get_cut_timestamp(days_period: int) -> int:
    current_time = datetime.utcnow()
    days_ago = current_time - timedelta(days=days_period)
    return int(days_ago.timestamp())


def get_top_authors_counts(instances_list: list[Submission | Comment], key: str) -> dict[str, int]:
    def substitute_athor_name(author: Redditor | str) -> str:
        if isinstance(author, Redditor):
            return author.name
        else:
            return author

    counts_dict: dict[str, int] = {}

    for instance in instances_list:
        redditor = getattr(instance, key)
        author = substitute_athor_name(redditor)
        if author is None:
            continue
        if author in counts_dict:
            counts_dict[author] += 1
        else:
            counts_dict[author] = 1
    sorted_counts_dict = dict(sorted(counts_dict.items(), key=lambda item: item[1], reverse=True))
    return sorted_counts_dict


def print_fancy_top(count_dict: dict[str, int], top_num: int) -> None:
    total_lines = len(count_dict)
    if top_num > total_lines:
        top_num = total_lines

    table_data = [[key, value] for key, value in count_dict.items()][:top_num]
    print(tabulate(table_data, headers=['Name', 'Count'], tablefmt="fancy_grid"))
