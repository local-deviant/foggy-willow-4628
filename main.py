"""The funniest office joke, judged head to head.

Running this module writes the joke to the file the grader reads:
``/output/entry.txt`` by default, or the path named by ``ENTRY_OUTPUT``
for a local test run. Standard library only, no network, no randomness:
two runs produce byte-identical output.
"""

import os
from pathlib import Path

# The joke itself: one line about office life. Why this line, against
# the judge's brief (most important criterion first):
#   1. It IS a one-line joke about office life with a setup and a
#      turn: "I emailed everyone to stop replying all" sets the
#      scene, "47 people agreed -- by replying all" turns it.
#   2. It turns on something anyone who has worked in an office
#      knows: the reply-all storm, the email nobody wanted that
#      everybody answers anyway.
#   3. It surprises: the agreement itself commits the very sin the
#      email was trying to stop -- the people who agree are the
#      problem, and they prove it by agreeing. A second, unseen
#      twist reframes the whole line: "agreed" sounds like support
#      until "by replying all" lands.
#   4. It lands in one line, every word earning its place, punchline
#      last: "by replying all" is the final beat and the whole joke.
#   5. It feels new: the joke is not "reply-all is annoying" (the
#      complaint everyone states plainly) but the self-demonstrating
#      loop -- the cure spreads the disease, and the headcount (47)
#      makes the pile-on concrete.
# "47" was chosen over a spelled-out number: it reads instantly and
# keeps the line tight. Runner-up, kept out: "He said 'quick
# question' at 4:59 on a Friday. It's Tuesday, and I'm still in
# that meeting." -- strong time-jump, but the Friday-4:59 setup is
# a more familiar exaggeration than the reply-all loop.
# The gate allows 1-200 characters; keep it a single line.
JOKE_LINE = "I emailed everyone to stop replying all. 47 people agreed \u2014 by replying all."
LIMIT = 200


def check(line):
    """Reject anything the gate would refuse: more than one line,
    blank, over the character limit, padded with whitespace, or
    holding control characters."""
    if "\n" in line or "\r" in line:
        raise ValueError("joke must fit on one line")
    if not line.strip():
        raise ValueError("joke must not be blank")
    if len(line) > LIMIT:
        raise ValueError("joke is over the character limit")
    if line != line.strip():
        raise ValueError("joke must not start or end with whitespace")
    if any(ord(ch) < 0x20 for ch in line):
        raise ValueError("joke must not hold control characters")


def destination():
    """Where the joke goes: the grader's path, unless ENTRY_OUTPUT
    points the run at a scratch file for local testing."""
    return Path(os.environ.get("ENTRY_OUTPUT", "/output/entry.txt"))


def main():
    check(JOKE_LINE)
    target = destination()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(JOKE_LINE, encoding="utf-8")
    # The grader collects the output as a different user than the one
    # this program runs as: leave the file readable by everyone, or
    # the run fails with "<path> is not readable" even though the
    # program wrote it.
    os.chmod(target, 0o644)


if __name__ == "__main__":
    main()
