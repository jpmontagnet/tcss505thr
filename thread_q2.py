# TCSS 505 - threading homework - question 2
# Student: JP Montagnet / jpmont

import argparse
import requests
import random
import threading
import time

"""
Goal:
Write a program that uses at least two threads to execute the same code
with the goal of improving the performance of the code.
First, execute the program with a single thread and time the result.
Next, execute the program with more than one thread and time the result,
showing an improvement in performance.

Solution:
The Sorting Hat, of Harry Potter fame, is a bottleneck.
Implemented additional Sorting Hats.
The roster of of students is split up evenly among the hats
via modulus of their respective index in the roster list.
Locking is used only for outputting the results.
Optionally, each student's name is searched for in Wikipedia
before the student is sorted. After all, the hats want to make
informed decisions! Okay, not really. Their "sorting" selections
here are, in fact, purely random. It is the long I/O delay of
the Wikipedia searches that makes multi-threading a win.
"""

g_houses_dflt = """
Gryffindor
Hufflepuff
Ravenclaw
Slytherin
""".strip().splitlines()

# Arbitrary subset of names from:
# harrypotter.neoseeker.com/wiki/List_of_students_that_go_to_Hogwarts
# ...plus a few other magical kids.
g_roster_dflt = """
Harry Potter
Hermione Granger
Ginny Weasley
Ron Weasley
Luna Lovegood
Draco Malfoy
Neville Longbottom
Millicent Bulstrode
Kevin Entwhistle
Anakin Skywalker
Tabitha Stephens
Sabrina Spellman
Constance Contraire
Loki Laufeyson
Ned Leeds
Billy Batson
""".strip().splitlines()

class Opts:
    houses_list = g_houses_dflt
    roster_file = None
    roster_list = g_roster_dflt
    num_threads = 1
    search_wiki = False

g_opts = Opts()

g_url = "https://en.wikipedia.org/w/api.php"

g_params = {
    "action": "query",
    "generator": "allpages",
    "gaplimit": 1,
    "prop": "description",
    "gapfilterredir": "nonredirects",
    "format": "json",
}

g_lock = threading.Lock()

def lock_acquire():
    global g_opts
    global g_lock
    if g_opts.num_threads == 1:
        return
    g_lock.acquire()

def lock_release():
    global g_opts
    global g_lock
    if g_opts.num_threads == 1:
        return
    g_lock.release()

def search_wiki(name: str):
    sess = requests.Session()
    params = g_params.copy()
    params["gapfrom"] = name
    resp = sess.get(url=g_url, params=params)
    data = resp.content
    if not data:
        return None  # "no resp content"
    data = resp.json()
    if not data:
        return None  # "not json"
    if "query" not in data:
        return None  # "no query"
    data = data["query"]
    if "pages" not in data:
        return None  # "no pages"
    data = list(data["pages"].values())[0]
    if "description" not in data:
        return None  # "no description"
    data = data["description"]
    return data

def sorting_hat(tid: int):
    global g_opts
    roster = [v for i, v in enumerate(g_opts.roster_list)
              if i % g_opts.num_threads == tid]
    for i, v in enumerate(roster):
        info = None
        if g_opts.search_wiki:
            info = search_wiki(v)
            if info is None:
                info = "(search was inconclusive)"
        house = random.choice(g_opts.houses_list)
        lock_acquire()
        if g_opts.search_wiki:
            print(f"{v}: {info}")
        print(f"{v} goes to {house}!")
        lock_release()

def assign_houses():
    global g_opts
    for opt in "num_threads search_wiki".split():
        print(f"Option {opt}: {getattr(g_opts, opt)}")
    print("---")
    threads = []
    for tid in range(g_opts.num_threads):
        thr = threading.Thread(target=sorting_hat, args=(tid,))
        threads.append(thr)
    start = time.perf_counter()
    for thr in threads:
        thr.start()
    for thr in threads:
        thr.join()
    finit = time.perf_counter()
    print("---")
    print(f"Sorting completed in {finit - start} secs")

def parse_opts():
    global g_opts
    parser = argparse.ArgumentParser(
        description="Fiddle with thread parallelization")
    parser.add_argument("--roster-file", type=str,
        help="File containing roster of students")
    parser.add_argument("--num-threads", type=int, default=Opts.num_threads,
        help="Number of threads")
    parser.add_argument("--search-wiki", action="store_true",
        help="Search online for info when sorting")
    args = parser.parse_args()

    if args.roster_file:
        with open(args.roster_file, "r") as r:
            g_opts.roster = r.readlines()
            g_opts.roster_file = args.roster

    g_opts.num_threads = args.num_threads
    g_opts.search_wiki = args.search_wiki

if __name__ == "__main__":
    parse_opts()
    assign_houses()

# END
