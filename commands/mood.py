from discord_client import client
from discord.ext.commands import Context
import csv
import random
from typing import Dict, Set


class TrackInfo:
    def __init__(self, title: str, artist: str):
        self.title = title
        self.artist = artist

    def getSearchQuery(self):
        return f"{self.title} {self.artist}"


categorizedTrackIds: Dict[str, Set[str]] = dict()
trackInfoDict: Dict[str, TrackInfo] = dict()

# Read labeled csv file.
with open("labelled_scraped.csv", encoding="utf-8", newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Load track info.
        trackInfoDict[row["spotify_id"]] = TrackInfo(
            row["title"], row["artist"]
        )

        # Categorize.
        if row["label"] in categorizedTrackIds:
            categorizedTrackIds[row["label"]].add(row["spotify_id"])
        else:
            categorizedTrackIds[row["label"]] = set([row["spotify_id"]])


def playlistToStr(spotifyIds: Set[str]) -> str:
    return "\n".join(map(lambda x: f"spotify:track:{x}", spotifyIds))


@client.command()
async def mood(ctx: Context, *args: str):
    try:
        message = "".join(
            [
                "Please copy-paste the following text ",
                "into your Spotify client.",
                "```\n",
                playlistToStr(random.sample(categorizedTrackIds[args[0]], 20)),
                "\n```",
            ]
        )
        await ctx.message.channel.send(message)
    except Exception as e:
        print(e)
        await ctx.message.channel.send("No tracks.")
