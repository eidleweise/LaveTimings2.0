import feedparser
import re
import sys

FEED_URL = "https://laveradio.com/feed/laveradio.xml"

def extract_episode_number(title: str) -> int | None:
    """
    Extracts the first sequence of digits from an episode title.

    Args:
        title: The episode title string (e.g., "Lave Radio Episode 450").

    Returns:
        The extracted episode number as an integer, or None if not found.
    """
    match = re.search(r'\d+', title)
    if match:
        return int(match.group(0))
    return None

def get_and_print_latest_episode(url: str):
    """
    Fetches the latest episode from an RSS feed and prints its details.
    """
    print(f"Fetching feed from {url}...")
    feed = feedparser.parse(url)

    # Check for parsing errors or an empty feed
    if feed.bozo:
        print(f"Error: Could not parse feed. Reason: {feed.bozo_exception}", file=sys.stderr)
        return
    if not feed.entries:
        print("Error: Feed contains no entries.", file=sys.stderr)
        return

    # feedparser orders entries from newest to oldest, so the first is the latest
    latest_episode = feed.entries[0]

    title = latest_episode.get('title', 'N/A')
    episode_number = extract_episode_number(title)

    # Safely get the enclosure URL
    enclosure_url = None
    if 'enclosures' in latest_episode and len(latest_episode.enclosures) > 0:
        enclosure_url = latest_episode.enclosures[0].get('href')

    print("\n--- Most Recent Lave Radio Episode ---")
    print(f"  Episode Number: {episode_number or 'Not found'}")
    print(f"  Title:          {title}")
    print(f"  Download URL:   {enclosure_url or 'Not found'}")

if __name__ == "__main__":
    get_and_print_latest_episode(FEED_URL)