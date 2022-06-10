# TCSS 505 Threading homework
# Student: JP Montagnet / jpmont

Worked in this alone.
The main issue encountered was simply coming up with a viable scenario.
For both problems, the solution provided is contrived.

For #1, not much to say, other than it was interesting to demonstrate
how quickly (or not) that a race condition could be triggered.
Calling to a no-op function was about the bare minimum of work
between successive reads, necessary to trigger.
Various other in-line processing (no function call) were insufficient,
at least within the time limits that I imposed on my attempts.

The "Sorting Hat" for #2 was more fun though. ;-)
For #2, I had hoped that filesystem ops would incur enough I/O time
that multiple threads would win; this was not the case.
Switching to network I/O -- a search of Wikipedia -- was sufficient.

No questions, within the scope of this assignment.
Learned a few new things in the course of reading.