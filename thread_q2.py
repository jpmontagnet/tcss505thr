# TCSS 505 - threading homework - question 1
# Student: JP Montagnet / jpmont

import argparse
import os.path
import random
import shutil
import threading
import time
import tempfile

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
    out_basedir = "."
    keep_outdir = False

g_opts = Opts()

def sorting_hat(tid: int):
    global g_opts
    roster = [v for i, v in enumerate(g_opts.roster_list)
              if i % g_opts.num_threads == tid]
    for i, v in enumerate(roster):
        filename = os.path.join(g_opts.out_basedir, f"{tid}_{i}")
        house = random.choice(g_opts.houses_list)
        with open(filename, "w") as f:
            print(f"{v} goes to {house}!", file=f)

def assign_houses():
    global g_opts
    print(f"Option num-threads = {g_opts.num_threads}")
    print(f"Option out-basedir = {g_opts.out_basedir}")
    print(f"Option keep-outdir = {g_opts.keep_outdir}")
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
    if not g_opts.keep_outdir:
        shutil.rmtree(path=g_opts.out_basedir)

def parse_opts():
    global g_opts
    parser = argparse.ArgumentParser(
        description="Fiddle with thread parallelization")
    parser.add_argument("--roster-file", type=str,
        help="File containing roster of students")
    parser.add_argument("--num-threads", type=int, default=Opts.num_threads,
        help="Number of threads")
    parser.add_argument("--out-basedir", type=str, default=".",
        help="Base output dir")
    parser.add_argument("--keep_outdir", action="store_true",
        help="Keep temporary output dir and its contents")
    args = parser.parse_args()
    if args.roster_file:
        with open(args.roster_file, "r") as r:
            g_opts.roster = r.readlines()
            g_opts.roster_file = args.roster
    g_opts.num_threads = args.num_threads
    g_opts.out_basedir = tempfile.mkdtemp(dir=args.out_basedir, prefix="hogwarts_")
    tempfile.tempdir = g_opts.out_basedir
    g_opts.keep_outdir = args.keep_outdir

if __name__ == "__main__":
    parse_opts()
    assign_houses()

# END
