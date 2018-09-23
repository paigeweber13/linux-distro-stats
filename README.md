# Basic Info
## Current status: very WIP.
The goal of this project is to visualize data about people's impressions of
various linux distributions using data gathered from distrowatch.org. This
website will get the data on load from distrowatch and cache it for 24 hours.
There will be no database on the backend (for now).

## Todo before version 0.1
 - [x] backend functions that get reviews, ratings, and popularity
 - [ ] decide on key words to find in reviews
 - [ ] backend function to find list of words in reviews and track the number
   of occurances of each word
 - [ ] create draft of site layout
 - [ ] visualize data with javascript
 - [ ] cache found data, refresh cache every 24 hours

## Future work:
 * At some point, I would like to build this tool in Pharos, just for the
   exercise.
 * store weekly popularity in a database every week and use that to create
   popularity metrics over arbitrary periods of time

