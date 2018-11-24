# Basic Info
## Current status: very WIP.
The goal of this project is to visualize data about people's impressions of
various linux distributions using data gathered from distrowatch.org. This
website will get the data on load from distrowatch and cache it for 24 hours.
There will be no database on the backend (for now).

## Todo before version 0.1
 - [x] backend functions that get reviews, ratings, and popularity
 - [x] decide on key words to find in reviews (needs review, but an initial
   list has been created)
 - [x] backend function to find list of words in reviews and track the number
   of occurances of each word
 - [ ] create draft of site layout
 - [ ] visualize data with javascript
 - [ ] cache found data, refresh cache every 24 hours

## Reasoning behind keywords
### What is the 'ideal' operating system?
 * easy - 'it just works' like a mac. This means features like automatic
   hardware recognition, automatic driver loading, detecting display
   connection/disconnection, etc.
 * reliable - always behaves as expected. You don't boot up your computer and
   not have your wireless card show up in network-manager, for instance.
 * fast - slim. OS (including default desktop environment) doesn't hog ram or
   cpu.
 * customizable - does not restrict the user's choice of software,
   out-of-the-box behavior can be changed as much as the user wants

This program will search for words that indicate the presence of this desirable
trait as well as search for words that indicate the precense of the opposite,
undesirable behavior. For instance, when building a metric for ease-of-use, the
software will search for words like "works" and "trivial" that increase the
score as well as searching for words like "hard" or "hassle" that would
decrease the score. The exact words used by this software can be found in
keywords.json

## Future work:
 * At some point, I would like to build this tool in
   [Pharo](https://pharo.org/), just for the exercise.
 * store weekly popularity in a database every week and use that to create
   popularity metrics over arbitrary periods of time

