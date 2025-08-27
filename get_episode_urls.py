import feedparser
import re

FEED_URL = "https://laveradio.com/feed/laveradio.xml"
MAX_EPISODE_NUMBER = 550  # Adjust as needed


def extract_episode_number(title: str) -> int | None:
    """
    Extracts the first sequence of digits from a string.

    Args:
        title: The episode title string (e.g., "Lave Radio Episode 450").

    Returns:
        The extracted episode number as an integer, or None if not found.
    """
    match = re.search(r'\d+', title)
    if match:
        return int(match.group(0))
    return None


def extract_episode_number_from_old_url(url: str) -> float | None:
    """
    Extracts the episode number from a Lave Radio MP3 URL.

    The number is expected to be between "-ep" and ".mp3".
    It can be an integer or a decimal (e.g., 500.5).

    Args:
        url: The URL of the MP3 file (e.g., ".../laveradio-ep545.mp3").

    Returns:
        The episode number as a float, or None if not found.
    """
    # Regex to find numbers (including decimals) between '-ep' and '.mp3'
    match = re.search(r'-ep(\d+(\.\d+)?)\.mp3', url)
    if match:
        # group(1) captures the full number string, e.g., "545" or "500.5"
        return float(match.group(1))
    return None


def get_lave_radio_episode_map(url: str) -> dict[int, str]:
    """
    Reads the Lave Radio RSS feed and creates a map of episode numbers to
    their enclosure URLs.

    Args:
        url: The URL of the RSS feed.

    Returns:
        A dictionary where the key is the episode number (int) and the
        value is the enclosure URL (str).
    """
    print(f"Fetching and parsing feed from {url}...")
    feed = feedparser.parse(url)
    episode_map = {}

    if feed.bozo:
        print(f"Warning: feedparser reported an error: {feed.bozo_exception}")

    for entry in feed.entries:
        title = entry.get('title', '')

        # Identify main Lave Radio episodes by their title format
        if title.startswith("Lave Radio Episode") or title.startswith("Episode "):
            episode_number = extract_episode_number(title)

            # Ensure we have an episode number and an enclosure URL
            if episode_number and 'enclosures' in entry and len(entry.enclosures) > 0:
                enclosure_url = entry.enclosures[0].get('href')
                if enclosure_url:
                    episode_map[episode_number] = enclosure_url
                else:
                    print(f"Warning: Found episode '{title}' but it has no enclosure URL.")
            else:
                print(f"Warning: Could not fully process entry: '{title}'")

    print("Parsing complete.")
    return episode_map


def old_url_to_new_url(old_url: str, episode_map: dict[int, str]) -> str | None:
    """
    Converts an old Lave Radio MP3 URL to the new URL using the episode map.

    Args:
        old_url: The old MP3 URL (e.g., ".../laveradio-ep545.mp3").
        episode_map: A dictionary mapping episode numbers to new URLs.

    Returns:
        The new URL if found, otherwise None.
    """
    episode_number = extract_episode_number_from_old_url(old_url)
    if episode_number is not None:
        return episode_map.get(int(episode_number))
    return None


def all_old_urls_to_new_urls(episode_map: dict[int, str]) -> None:
    for i in range(1, MAX_EPISODE_NUMBER + 1):
        old_url = f"https://laveradio.com/podcasts/Lave_Radio/laveradio-ep{i}.mp3"
        new_url = old_url_to_new_url(old_url, episode_map)
        print(f"Old URL: {old_url} -> New URL: {new_url}")



if __name__ == "__main__":
    lave_episodes = get_lave_radio_episode_map(FEED_URL)
    if lave_episodes:
        print("\n--- Lave Radio Episode Map [Episode # -> URL] ---")
        # # Print each episode's number and URL, sorted by episode number
        # for episode_num, url in sorted(lave_episodes.items()):
        #     print(f"Episode {episode_num}: {url}")
        # print(f"\nFound {len(lave_episodes)} episodes.")
        all_old_urls_to_new_urls(lave_episodes)
    else:
        print("Could not find any Lave Radio episodes in the feed.")


