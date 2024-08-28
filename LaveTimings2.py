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

    for entry in feed.entries:
        title_ = entry['title']
        duration = get_duration(entry)
        total_duration = total_duration + duration
        if title_.startswith("Lave Radio Episode") or title_.startswith("Episode "):
            total_laveradio_duration = total_laveradio_duration + duration
            total_laveradio_count = total_laveradio_count + 1
        elif "Interview" in title_:
            total_interview_duration = total_interview_duration + duration
            total_interview_count = total_interview_count + 1
        elif "Conclave" in title_:
            total_conclave_duration = total_conclave_duration + duration
            total_conclave_count = total_conclave_count + 1
        elif title_.startswith("Retro Lave Episode"):
            total_retro_duration = total_retro_duration + duration
            total_retro_count = total_retro_count + 1
        elif "EGX" in title_:
            total_egx_duration = total_egx_duration + duration
            total_egx_count = total_egx_count + 1
        elif title_.startswith("Remote Outpost Games"):
            total_rog_duration = total_rog_duration + duration
            total_rog_count = total_rog_count + 1
        elif "RPG" in title_:
            total_rpg_duration = total_rpg_duration + duration
            total_rpg_count = total_rpg_count + 1
        else:
            print(f"Unexpected Title: {title_}")
            total_others_duration = total_others_duration + duration
            total_others_count = total_others_count + 1

    print("")
    print("")
    hh, mm, ss = total_duration_to_hhmmss(total_duration)
    print(f"Grand Total: {number_of_items} Shows: {hh} Hours {mm} Hours {ss} Seconds")
    hhlr, mmlr, sslr = total_duration_to_hhmmss(total_laveradio_duration)
    print(f"{total_laveradio_count} Lave Radio Episodes: {hhlr} Hours {mmlr} Minutes {sslr} Seconds")
    hhi, mmi, ssi = total_duration_to_hhmmss(total_interview_duration)
    print(f"{total_interview_count} Interviews: {hhi} Hours {mmi} Minutes {ssi} Seconds")
    hhc, mmc, ssc = total_duration_to_hhmmss(total_conclave_duration)
    print(f"{total_conclave_count} Conclave Episodes: {hhc} Hours {mmc} Minutes {ssc} Seconds")
    hhr, mmr, ssr = total_duration_to_hhmmss(total_retro_duration)
    print(f"{total_retro_count} Retro Lave Episodes: {hhr} Hours {mmr} Minutes {ssr} Seconds")
    hhegx, mmegx, ssegx = total_duration_to_hhmmss(total_egx_duration)
    print(f"{total_egx_count} EGX Episodes: {hhegx} Hours {mmegx} Minutes {ssegx} Seconds")
    hhrog, mmrog, ssrog = total_duration_to_hhmmss(total_rog_duration)
    print(f"{total_rog_count} Remote Outpost Games Episodes: {hhrog} Hours {mmrog} Minutes {ssrog} Seconds")
    hhrpg, mmrpg, ssrpg = total_duration_to_hhmmss(total_egx_duration)
    print(f"{total_rpg_count} RPG Episodes: {hhrpg} Hours {mmrpg} Minutes {ssrpg} Seconds")
    hho, mmo, sso = total_duration_to_hhmmss(total_others_duration)
    print(f"{total_others_count} Other Episodes: {hho} Hours {mmo} Minutes {sso} Seconds")


parse_lave_radio()
