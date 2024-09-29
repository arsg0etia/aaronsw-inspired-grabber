import subprocess
import urllib.request
import random
import sys

class NoBlocks(Exception):
    pass

def getblocks():
    try:
        response = urllib.request.urlopen("http://{?REDACTED?}/grab")
        r = response.read().decode('utf-8')  # Decode bytes to string
        if '<html' in r.lower():
            raise NoBlocks
        return r.split()
    except Exception as e:
        print(f"Error fetching blocks: {e}")
        raise NoBlocks

if len(sys.argv) > 1:
    prefix = ['--socks5', sys.argv[1]]
else:
    prefix = []  # You could specify an interface here if necessary

def line(x):
    return ['curl'] + prefix + [
        '-H', f"Cookie: TENACIOUS={str(random.random())[3:]}",
        '-o', f'pdfs/{x}.pdf',
        f"http://www.jstor.org/stable/pdfplus/{x}.pdf?acceptTC=true"
    ]

while True:
    try:
        blocks = getblocks()
        for block in blocks:
            print(block)
            # Using subprocess.run() instead of Popen().wait()
            subprocess.run(line(block), check=True)
    except NoBlocks:
        print("No blocks available, retrying...")
    except KeyboardInterrupt:
        print("Interrupted by user, exiting.")
        break
    except Exception as e:
        print(f"An error occurred: {e}")
