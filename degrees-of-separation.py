"""
A tiny script to find the shortest path between two Wikipedia articles.
"""

import argparse
import requests
from bs4 import BeautifulSoup
from collections import deque


def main() -> None:
    parser = argparse.ArgumentParser(description="Process two links.")
    parser.add_argument("link1", type=str, help="The first link")
    parser.add_argument("link2", type=str, help="The second link")
    parser.add_argument("--max_depth", type=int, default=5, help="Maximum search depth")

    args = parser.parse_args()

    print(f"Link 1: {args.link1}")
    print(f"Link 2: {args.link2}")

    try:
        r = requests.get(args.link1)
        r.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching {args.link1}: {e}")
        return

    try:
        r = requests.get(args.link2)
        r.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching {args.link2}: {e}")
        return

    visited = set()

    def neighbors(link: str) -> "set[str]":
        try:
            print(f"Fetching {link}")
            r = requests.get(link)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "html.parser")

            links = set()
            for a in soup.find_all("a", href=True):
                if a["href"].startswith("/wiki/"):
                    links.add(f'https://en.wikipedia.org{a["href"]}')

            return links
        except requests.RequestException as e:
            print(f"Error fetching {link}: {e}")
            return set()

    def bfs(start: str, target: str) -> int:
        queue = deque([(start, 0)])
        visited.add(start)

        while queue:
            current_link, depth = queue.popleft()
            print(f"Checking {current_link} at depth {depth}")

            if depth > args.max_depth:
                return 0

            if current_link == target:
                return depth

            for neighbor in neighbors(current_link):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, depth + 1))

        return 0

    if depth := bfs(args.link1, args.link2):
        print("Found a path", depth)
    else:
        print("No path found")


if __name__ == "__main__":
    main()
