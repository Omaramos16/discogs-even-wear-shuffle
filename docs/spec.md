# Project Spec (Still early ideas)

### The "Equal Opportunity" Logic
1. **Fetch:** Get all albums from the Google Sheet. Frequency TBD, maybe daily? Store last fetch in sheets (hidden) page
2. **Filter:** Find the minimum value in the `Played` column.
3. **Select:** Filter for all albums where `Played == min_value`.
4. **Randomize:** Pick one album from that filtered list.
5. **Update:** If User plays: `Played += 1`. If User skips: `Skipped += 1`
   - What counts as a "Play"? The user clicking on whatever launches it on Spotify.
   - What counts as a "Skip"? The user click the random button TWICE. (The first one might just be an accident or to "wake up" the widget, maybe just a freebie?)

### Data Structure (Google Sheet)
- **Discogs_ID**: Unique key.
- **Artist/Album/Info**: For visibility.
- **Played**: How many times you've listened.
- **Skipped**: How many times you rejected the suggestion.
- **Spotify_Link**: The URI to launch the app.

### Hardware/Software Target
- **Device:** Android (will be developing using my Pixel 10 Pro, but will try testing environments).
- **Widget:** TBD, maybe Jetpack Glance (2x2 layout).