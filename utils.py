from tabulate import tabulate

from praw.models import Comment, Submission  # type: ignore

from praw_utils import substitute_athor_name


def get_top_authors_counts(instances_list: list[Submission | Comment], key: str) -> dict[str, int]:

    counts_dict: dict[str, int] = {}

    for instance in instances_list:
        redditor = getattr(instance, key, None)
        author = substitute_athor_name(redditor)
        if author is None:
            continue
        if author in counts_dict:
            counts_dict[author] += 1
        else:
            counts_dict[author] = 1
    sorted_counts_dict = dict(sorted(counts_dict.items(), key=lambda item: item[1], reverse=True))
    return sorted_counts_dict


def get_fancy_top_table(count_dict: dict[str, int], top_num: int, header: str) -> str:
    total_lines = len(count_dict)
    if top_num > total_lines:
        top_num = total_lines

    table_data = [[key, value] for key, value in count_dict.items()][:top_num]
    return tabulate(table_data, headers=[header, 'Count'], tablefmt="fancy_grid")
