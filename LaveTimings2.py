import feedparser


def get_duration(item):
    title_ = item['title']
    # print(title_)
    duration_str = item['itunes_duration']
    # print(title_ + " : " + duration_str)
    splits = len(duration_str.split(':'))
    duration_in_seconds = 0
    if splits == 3:
        hours, minutes, seconds = duration_str.split(':')
        duration_in_seconds = int(hours) * 3600 + int(minutes) * 60 + int(seconds)
    elif splits == 2:
        minutes, seconds = duration_str.split(':')
        duration_in_seconds = int(minutes) * 60 + int(seconds)
    return duration_in_seconds

def total_duration_to_hhmmss(total):
    # Extract hours, minutes, and seconds
    hours = total // 3600
    minutes = (total % 3600) // 60
    seconds = total % 60
    return hours, minutes, seconds


def get_file_size(item):
    """
    Extracts the file size (length) in bytes from an RSS feed entry.
    The length is typically found in the 'enclosures' section of the entry.
    """
    try:
        # The length is a string representing bytes, so convert to integer.
        return int(item['enclosures'][0]['length'])
    except (KeyError, IndexError, ValueError):
        # Handle cases where 'enclosures' key is missing, the list is empty,
        # or the length value is not a valid integer.
        print(f"Warning: Could not find file length for entry: {item.get('title', 'Unknown Entry')}")
        return 0


def format_file_size(size_in_bytes):
    """
    Converts a file size in bytes to a human-readable string in MB or GB.
    """
    if size_in_bytes == 0:
        return "0 MB"
    # 1 Gigabyte = 1024 * 1024 * 1024 bytes
    gb_size = size_in_bytes / (1024**3)
    if gb_size >= 1:
        return f"{gb_size:.2f} GB"
    # 1 Megabyte = 1024 * 1024 bytes
    mb_size = size_in_bytes / (1024**2)
    return f"{mb_size:.2f} MB"




def parse_lave_radio():
    feed = feedparser.parse("https://laveradio.com/feed/laveradio.xml")
    number_of_items = len(feed.entries)
    total_duration = 0
    total_laveradio_duration = 0
    total_conclave_duration = 0
    total_retro_duration = 0
    total_egx_duration = 0
    total_rog_duration = 0
    total_rpg_duration = 0
    total_interview_duration = 0
    total_others_duration = 0

    total_laveradio_count = 0
    total_conclave_count = 0
    total_retro_count = 0
    total_egx_count = 0
    total_rog_count = 0
    total_rpg_count = 0
    total_interview_count = 0
    total_others_count = 0

    total_filesize = 0
    total_laveradio_filesize = 0
    total_conclave_filesize = 0
    total_retro_filesize = 0
    total_egx_filesize = 0
    total_rog_filesize = 0
    total_rpg_filesize = 0
    total_interview_filesize = 0
    total_others_filesize = 0

    for entry in feed.entries:
        title_ = entry['title']
        duration = get_duration(entry)
        filesize = get_file_size(entry)
        total_duration = total_duration + duration
        total_filesize = total_filesize + filesize
        if title_.startswith("Lave Radio Episode") or title_.startswith("Episode "):
            total_laveradio_duration = total_laveradio_duration + duration
            total_laveradio_filesize = total_laveradio_filesize + filesize
            total_laveradio_count = total_laveradio_count + 1
        elif "Interview" in title_:
            total_interview_duration = total_interview_duration + duration
            total_interview_filesize = total_interview_filesize + filesize
            total_interview_count = total_interview_count + 1
        elif "Conclave" in title_:
            total_conclave_duration = total_conclave_duration + duration
            total_conclave_filesize = total_conclave_filesize + filesize
            total_conclave_count = total_conclave_count + 1
        elif title_.startswith("Retro Lave Episode"):
            total_retro_duration = total_retro_duration + duration
            total_retro_filesize = total_retro_filesize + filesize
            total_retro_count = total_retro_count + 1
        elif "EGX" in title_:
            total_egx_duration = total_egx_duration + duration
            total_egx_filesize = total_egx_filesize + filesize
            total_egx_count = total_egx_count + 1
        elif title_.startswith("Remote Outpost Games"):
            total_rog_duration = total_rog_duration + duration
            total_rog_filesize = total_rog_filesize + filesize
            total_rog_count = total_rog_count + 1
        elif "RPG" in title_:
            total_rpg_duration = total_rpg_duration + duration
            total_rpg_filesize = total_rpg_filesize + filesize
            total_rpg_count = total_rpg_count + 1
        else:
            print(f"Unexpected Title: {title_}")
            total_others_duration = total_others_duration + duration
            total_others_filesize = total_others_filesize + filesize
            total_others_count = total_others_count + 1

    print("")
    print("")
    hh, mm, ss = total_duration_to_hhmmss(total_duration)
    print(f"Grand Total: {number_of_items} Shows: {hh} Hours {mm} Minutes {ss} Seconds ({format_file_size(total_filesize)})")
    hhlr, mmlr, sslr = total_duration_to_hhmmss(total_laveradio_duration)
    print(f"{total_laveradio_count} Lave Radio Episodes: {hhlr} Hours {mmlr} Minutes {sslr} Seconds ({format_file_size(total_laveradio_filesize)})")
    hhi, mmi, ssi = total_duration_to_hhmmss(total_interview_duration)
    print(f"{total_interview_count} Interviews: {hhi} Hours {mmi} Minutes {ssi} Seconds ({format_file_size(total_interview_filesize)})")
    hhc, mmc, ssc = total_duration_to_hhmmss(total_conclave_duration)
    print(f"{total_conclave_count} Conclave Episodes: {hhc} Hours {mmc} Minutes {ssc} Seconds ({format_file_size(total_conclave_filesize)})")
    hhr, mmr, ssr = total_duration_to_hhmmss(total_retro_duration)
    print(f"{total_retro_count} Retro Lave Episodes: {hhr} Hours {mmr} Minutes {ssr} Seconds ({format_file_size(total_retro_filesize)})")
    hhegx, mmegx, ssegx = total_duration_to_hhmmss(total_egx_duration)
    print(f"{total_egx_count} EGX Episodes: {hhegx} Hours {mmegx} Minutes {ssegx} Seconds ({format_file_size(total_egx_filesize)})")
    hhrog, mmrog, ssrog = total_duration_to_hhmmss(total_rog_duration)
    print(f"{total_rog_count} Remote Outpost Games Episodes: {hhrog} Hours {mmrog} Minutes {ssrog} Seconds ({format_file_size(total_rog_filesize)})")
    hhrpg, mmrpg, ssrpg = total_duration_to_hhmmss(total_rpg_duration)
    print(f"{total_rpg_count} RPG Episodes: {hhrpg} Hours {mmrpg} Minutes {ssrpg} Seconds ({format_file_size(total_rpg_filesize)})")
    hho, mmo, sso = total_duration_to_hhmmss(total_others_duration)
    print(f"{total_others_count} Other Episodes: {hho} Hours {mmo} Minutes {sso} Seconds ({format_file_size(total_others_filesize)})")


parse_lave_radio()
