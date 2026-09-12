# obe-to-dun

The MaamiMade free recipe page: how to make Nigerian stew, with the book sold underneath.

Live at https://thetoyosibello.github.io/obe-to-dun/

## Build

    python3 page.py     # index.html, copies img/ and fonts/ in
    python3 pins.py     # pins/*.jpg, the 1000x1500 Pinterest creatives

Both are self contained. `page.py` carries the four settings at the top (site URL, buy
link, email form action, price) and asserts that no em or en dash reaches the prose.
`pins.py` renders through Chrome headless so the type matches the book exactly.

## What is deliberately not here

The page teaches the method, the fry theory, the UK substitutions and every failure mode.
The signature pepper ratio, the tomato rule, the assorted protein playbook and the storage
method are the book.
