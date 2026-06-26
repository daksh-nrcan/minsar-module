#!/usr/bin/env python3
import os, netrc, time, requests
import asf_search as asf

wkt = "POLYGON((-113.3 54.4, -112.7 54.4, -112.7 53.9, -113.3 53.9, -113.3 54.4))"

results = asf.search(
    platform=asf.PLATFORM.SENTINEL1,
    processingLevel=asf.PRODUCT_TYPE.SLC,
    beamMode=asf.BEAMMODE.IW,
    flightDirection=asf.FLIGHT_DIRECTION.ASCENDING,
    relativeOrbit=49,
    start="2026-01-01",
    end="2026-05-14",
    intersectsWith=wkt,
    maxResults=20000,
)

print(f"Found {len(results)} scenes", flush=True)

out_dir = os.environ.get("SCRATCHDIR", ".")
os.makedirs(out_dir, exist_ok=True)

auth = netrc.netrc(os.environ.get("NETRC"))
username, _, password = auth.authenticators("urs.earthdata.nasa.gov")
session = asf.ASFSession().auth_with_creds(username, password)

def download_resume(url, dest, session, retries=5):
    # Before downloading, check if we already have the complete file.
    # HEAD request fetches only headers (no body), so it's cheap.
    # Content-Length is the total file size the server would send.
    if os.path.exists(dest):
        head = session.head(url)
        expected = int(head.headers.get("Content-Length", 0))
        if expected and os.path.getsize(dest) == expected:
            print(f"  Skip (complete): already at {expected:,} bytes", flush=True)
            return

    # retries=5 means up to 5 total attempts (not 5 extra retries)
    for attempt in range(retries):
        try:
            # Re-check size at the top of each attempt — if a previous attempt
            # downloaded some data before dropping, we resume from there
            existing = os.path.getsize(dest) if os.path.exists(dest) else 0

            # HTTP Range header tells the server "start sending from byte N"
            # so we skip what we already downloaded instead of restarting
            headers = {"Range": f"bytes={existing}-"} if existing else {}

            with session.get(url, headers=headers, stream=True) as resp:
                # 416 = server has nothing beyond what we already have = complete
                if resp.status_code == 416:
                    print(f"  Skip (complete): confirmed by server", flush=True)
                    return
                resp.raise_for_status()
                # "ab" = append-binary: new bytes get added after the existing ones
                # "wb" = write-binary: fresh file from scratch
                with open(dest, "ab" if existing else "wb") as f:
                    for chunk in resp.iter_content(chunk_size=1024 * 1024):
                        f.write(chunk)
            return  # success — exit the retry loop
        except (requests.exceptions.ChunkedEncodingError, requests.exceptions.ConnectionError):
            if attempt == retries - 1:
                raise  # last attempt failed — re-raise and let it crash
            # Exponential backoff: wait 1s, 2s, 4s, 8s between attempts
            wait = 2 ** attempt
            print(f"  Connection dropped, retrying in {wait}s ({attempt+1}/{retries-1})...", flush=True)
            time.sleep(wait)

for i, r in enumerate(results, 1):
    fname = r.properties["fileName"]
    fpath = os.path.join(out_dir, fname)
    print(f"[{i}/{len(results)}] Downloading: {fname}", flush=True)
    download_resume(r.properties["url"], fpath, session)
    print(f"  Done: {fname}", flush=True)
