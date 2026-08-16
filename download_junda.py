import urllib.request
import zipfile
import io

def run():
    print("Downloading ZIP...")
    url = "https://lingua.mtsu.edu/chinese-computing/statistics/char/char.zip"
    try:
        # Often Jun Da's zip is at this URL or similar, let's try.
        import ssl
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        req = urllib.request.Request(url)
        resp = urllib.request.urlopen(req, context=ctx)
        
        with open('char.zip', 'wb') as f:
            f.write(resp.read())
        print("Downloaded char.zip")
    except Exception as e:
        print("Failed:", e)

if __name__ == '__main__':
    run()
