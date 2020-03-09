import json
from collections import Counter
from urllib.request import urlopen

import numpy as np
from scipy.spatial import distance_matrix


def fetch_data(users_url, posts_url):
    """ Returns the dicts of users and posts based on provided urls. """
    with urlopen(users_url) as users_json:
        users = json.load(users_json)
    with urlopen(posts_url) as posts_json:
        posts = json.load(posts_json)

    return users, posts


def join(posts, users):
    """ Changes posts in place adding the entry 'user' based on a user's id. """
    pivoted_users = {user["id"]: user for user in users}
    for post in posts:
        post["user"] = pivoted_users[post["userId"]]


def count_posts(posts):
    """ Returns a list of strings of form: 
            *username* napisał(a) *count* postów. 
        Assumes users have been appended to posts (see the function join)."""
    no_posts = Counter(post["user"]["username"] for post in posts)
    posts_report = [
        "{} napisał(a) {} postów".format(username, count)
        for username, count in no_posts.items()
    ]

    return posts_report


def find_rep_titles(posts):
    """ Returns a list of repeated titles of posts. """
    no_titles = Counter(post["title"] for post in posts)
    repeated_titles = [title for title, count in no_titles.items() if count > 1]

    return repeated_titles


def find_closest_neighbors(users):
    """ Returns a dict of form:
            user id: id of the user living the closest """
    # Remarks:
    # - minimizing the distance on a sphere's surface is equivalent
    # to minimaling the Cartesian distance in 3d,
    # - there's also a function in the third-party geopy module that computes
    # the distance on a sphere using geographical coordinates explicitly.
    geo_coord = [
        (user["address"]["geo"]["lat"], user["address"]["geo"]["lng"]) for user in users
    ]  # extract geographical coordinates from the users dataset
    sph_coord = (
        np.pi / 180 * np.array(geo_coord, dtype=float)
    )  # conversion to spherical coordinates
    cart_coord = np.array(
        [
            np.sin(sph_coord[:, 0]) * np.cos(sph_coord[:, 1]),
            np.sin(sph_coord[:, 0]) * np.sin(sph_coord[:, 1]),
            np.cos(sph_coord[:, 0]),
        ]
    ).T  # convert sphercial coordinates to 3d Cartesian coordinates
    D = distance_matrix(cart_coord, cart_coord)
    np.fill_diagonal(
        D, 3
    )  # zeros on the diagonal are not the minima we're interested in
    closest_neighbors = {
        users[i]["id"]: users[np.argmin(D[i])]["id"] for i in range(len(users))
    }

    return closest_neighbors


if __name__ == "__main__":
    # fetch the datasets
    users, posts = fetch_data(
        "https://jsonplaceholder.typicode.com/users",
        "https://jsonplaceholder.typicode.com/posts",
    )

    # join the datasets
    join(posts, users)

    # count the posts written by each user
    posts_report = count_posts(posts)
    print("Raport postów:", *posts_report, sep="\n")
    print()

    # count the repeated titles
    repeated_titles = find_rep_titles(posts)
    print("Powtarzające się tytuły:", *repeated_titles, sep="\n")
    print()

    # find the closest neighbors
    closest_neighbors = find_closest_neighbors(users)
    print("Najbliżsi sąsiedzi:")
    for user_id1, user_id2 in closest_neighbors.items():
        print("User", user_id1, "mieszka najbliżej usera", user_id2)
    print()

