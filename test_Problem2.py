import unittest

from Problem2 import (
    fetch_data,
    join,
    count_posts,
    find_rep_titles,
    find_closest_neighbors,
)


class Problem2TestCase(unittest.TestCase):
    def setUp(self):
        self.users, self.posts = fetch_data(
            "https://jsonplaceholder.typicode.com/users",
            "https://jsonplaceholder.typicode.com/posts",
        )

    def test_join(self):
        join(self.posts, self.users)
        self.assertIn("user", self.posts[0])
        self.assertIs(self.posts[0]["user"], self.users[0])
        self.assertIn("user", self.posts[-1])
        self.assertIs(self.posts[-1]["user"], self.users[-1])

    def test_count_posts(self):
        join(self.posts, self.users)
        posts_report = count_posts(self.posts)
        for line in posts_report:
            line = line.split()
            self.assertEqual(line[2], "10", msg=line[0])

    def test_find_rep_titles(self):
        repeated_titles = find_rep_titles(self.posts)
        self.assertEqual(repeated_titles, [])

    def test_find_closest_neighbor(self):
        closest_neighbors = find_closest_neighbors(self.users)
        self.assertEqual(closest_neighbors[1], 5)
        self.assertEqual(closest_neighbors[4], 9)
        self.assertEqual(closest_neighbors[8], 7)
        self.assertEqual(closest_neighbors[10], 5)


if __name__ == "__main__":
    unittest.main()
