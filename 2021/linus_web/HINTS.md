# Hint

Agent,

Did you check the webapp for any LFI vulnerabilities? One common place to check would be the JavaScript to see what POST request interaction the webapp might be doing.
You already know the webapp doesn't do a lot, but I wonder what pipeline it passes uploaded videos through, maybe it transcodes them using some common tool to normalise formats? Not sure.

If you can get LFI, I wonder what files might be worth looking at, we know this is some sort of WSGI/python server they're using, maybe they're using common file names like wsgi.py or similar?
Investigate and find out, let me know once you've gained access to the system.

Good luck.
