#!/usr/bin/env python3
"""Shadow of minsar's asf_search_args.py — identical search, but downloads with resume+retry."""
import os, netrc, time, requests
import asf_search as asf
from minsar.cli.asf_search_args import create_parser, _filter_results_by_exclude_season


def download_resume(url, dest, session, retries=5):
    if os.path.exists(dest):
        head = session.head(url)
        expected = int(head.headers.get("Content-Length", 0))
        if expected and os.path.getsize(dest) == expected:
            print(f"  Skip (complete): {os.path.basename(dest)}", flush=True)
            return

    for attempt in range(retries):
        try:
            existing = os.path.getsize(dest) if os.path.exists(dest) else 0
            headers = {"Range": f"bytes={existing}-"} if existing else {}
            with session.get(url, headers=headers, stream=True) as resp:
                if resp.status_code == 416:
                    print(f"  Skip (complete): confirmed by server", flush=True)
                    return
                resp.raise_for_status()
                with open(dest, "ab" if existing else "wb") as f:
                    for chunk in resp.iter_content(chunk_size=1024 * 1024):
                        f.write(chunk)
            return
        except (requests.exceptions.ChunkedEncodingError, requests.exceptions.ConnectionError):
            if attempt == retries - 1:
                raise
            wait = 2 ** attempt
            print(f"  Connection dropped, retrying in {wait}s ({attempt+1}/{retries-1})...", flush=True)
            time.sleep(wait)


def main():
    inps = create_parser()

    print("Searching for data...\n")
    results = asf.search(
        platform=inps.platform,
        processingLevel=inps.processing_level,
        start=inps.start_date,
        end=inps.end_date,
        intersectsWith=inps.intersectsWith,
        flightDirection=inps.flightDirection,
        beamMode=inps.beam_mode,
        relativeOrbit=inps.relative_orbit,
        relativeBurstID=inps.burst_id,
        polarization=inps.polarization,
        dataset=inps.dataset,
    )

    result_list, excluded_count = _filter_results_by_exclude_season(results, inps.exclude_season_bounds)
    print(f"Found {len(results)} results.")
    if inps.exclude_season_bounds:
        print(f"After --exclude-season={inps.exclude_season}: {len(result_list)} results (excluded {excluded_count}).")

    for r in result_list:
        if inps.print:
            print(', '.join(str(v) for k, v in r.properties.items() if k not in ['centerLat', 'centerLon']))

    if not inps.download:
        return

    os.makedirs(inps.dir, exist_ok=True)
    auth = netrc.netrc(os.environ.get("NETRC"))
    username, _, password = auth.authenticators("urs.earthdata.nasa.gov")
    session = asf.ASFSession().auth_with_creds(username, password)

    print(f"Downloading {len(result_list)} results to {inps.dir} ...")
    for i, r in enumerate(result_list, 1):
        fname = r.properties["fileName"]
        fpath = os.path.join(inps.dir, fname)
        print(f"[{i}/{len(result_list)}] {fname}", flush=True)
        download_resume(r.properties["url"], fpath, session)
    print("Done")


if __name__ == "__main__":
    main()
