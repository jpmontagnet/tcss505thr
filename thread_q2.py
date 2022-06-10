# TCSS 505 - threading homework - question 1
# Student: JP Montagnet / jpmont

import argparse
import requests
import random
import threading
import time

"""
Write a program that uses at least two threads to execute the same code
with the goal of improving the performance of the code.
First, execute the program with a single thread and time the result.
Next, execute the program with more than one thread and time the result,
showing an improvement in performance.
"""

g_houses_dflt = """
Gryffindor
Hufflepuff
Ravenclaw
Slytherin
""".strip().splitlines()

# Arbitrary subset of names from:
# harrypotter.neoseeker.com/wiki/List_of_students_that_go_to_Hogwarts
# ...plus a few others.
g_roster_dflt = """
Harry Potter
Hermione Granger
Fred Weasley
George Weasley
Ginny Weasley
Ron Weasley
Percy Weasley
Cedric Diggory
Oliver Wood
Luna Lovegood
Draco Malfoy
Neville Longbottom
Ernie MacMillan
Millicent Bulstrode
Vincent Crabbe
Victoria Frobisher
Cormac McLaggen
Mandy Brocklehurst
Stephen Cornfoot
Kevin Entwhistle
Morag McDougal
Padma Patil
Orla Quirke
Justin Finch-Fletchley
Anakin Skywalker
Tabitha Stephens
Sabrina Spellman
Constance Contraire
Quentin Beck
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
    params["gspfrom"] = name
    # TODO
    return f"All about {name}"

def sorting_hat(tid: int):
    global g_opts
    roster = [v for i, v in enumerate(g_opts.roster_list)
              if i % g_opts.num_threads == tid]
    for i, v in enumerate(roster):
        info = None
        if g_opts.search_wiki:
            info = search_wiki(v)
            if info is None:
                info = "Search came up empty"
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
