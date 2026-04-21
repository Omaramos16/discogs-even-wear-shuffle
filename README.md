# Discogs "Even Wear" Shuffle

A "bring-your-own-backend" Android widget using the Google Sheets and Discogs APIs to give your physical media library "even wear." 

While Discogs provides a "Random Item" feature, it lacks memory—often suggesting the same albums repeatedly while others gather dust. This project acts as a state-aware shuffle that only repeats albums once your entire collection has been played. It also tracks skips to help you identify albums that never get a fair chance. User-owned, serverless, and open-source.

This project allows collectors to treat their library like a rotation rather than a dice roll. By using Google Sheets as a user-controlled database, every album is assigned a "played" and "skipped" counter. The algorithm ensures a "Fair Shuffle": it only selects from albums tied for the lowest "played" count. In other words, an album won't be suggested again until every other record in your collection has been given an equal chance.

Designed specifically for Android, this project provides a clean home-screen widget that displays album art and offers one-touch launching into Spotify or your preferred streaming service.

## Key Features
* "Even Wear" Algorithm: True exhaustion-based shuffling—no album repeats until the full rotation is complete.
* Collection Management Metrics: Tracks how many times you decide to dismiss a selection to help identify "shelf-warmers".
* User-Owned Data: No third-party servers. Your data lives in your own Google Sheet, which you can modify manually if needed.
* Android Integration: A low-profile (1x1 or 2x2) widget for instant library interaction.
* Automatic Linking: Bypasses search bars by matching your physical Discogs entry to a digital streaming link (Spotify) instantly.

## (Planned) Tech Stack
* **Client:** Android (Jetpack Glance Widget, Kotlin)
* **Backend / Database:** Google Sheets API & Google Apps Script (REST endpoint)
* **Sync Engine:** Python (for initial Discogs API ingestion)

## Status
**Phase 1:** Infrastructure, Spec, and Data Syncing.




