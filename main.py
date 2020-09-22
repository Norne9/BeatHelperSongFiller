import cloudscraper
import time
import json

BEAT_HELPER_URL = "http://51.15.122.220:12380/download"
DELAY_SONG = 3.0
DELAY_END = 5.0 * 60.0


def main():
    scraper = cloudscraper.create_scraper()
    while True:
        hashes = json.loads(scraper.get(BEAT_HELPER_URL).text)
        for s_hash in hashes:
            print(f"Processing {s_hash}...")
            url = f"https://beatsaver.com/api/search/text/0?q={s_hash}&?automapper=1"

            try:
                data = json.loads(scraper.get(url).text)
                doc = data["docs"][0]
                song = {
                    "Key": doc["key"],
                    "Hash": doc["hash"].upper(),
                    "SongName": doc["name"],
                    "Uploader": doc["uploader"]["username"],
                }
            except Exception as e:
                print(f"Failed to parse: {e}")
                continue

            try:
                print(json.dumps(song))
                if scraper.post(BEAT_HELPER_URL, json=song).status_code != 202:
                    raise Exception("Wrong status code!")
            except Exception as e:
                print(f"Failed to send: {e}")
                continue

            print(f"Processed {song['SongName']}.")
            time.sleep(DELAY_SONG)

        print("Waiting...")
        time.sleep(DELAY_END)


if __name__ == '__main__':
    main()
