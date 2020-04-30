# Crowdcast

Find out which bars and restaurants have small crowds and short lines in the era of social distancing.

[View Crowdcast Demo App](https://elated-benz-92515b.netlify.app)

_Note: The app is currently populated with static data and assets. During the hack:now event, it was wired up to an API powered by Flask, Google Places API and Google Photo API_

## hack:now Submission

Crowdcast was a our submission for Hack:now, the all-online 36-hour global hackathon that ran from April 24-26. This event was hosted by the team from Cal Hacks, the world's largest collegiate hackathon with ~2000 attendees held annually at UC Berkeley and run by the student group Hack the Bay in partnership with CITRIS Foundary.

*Recognized as one of the "Top 30 Teams of hack:now", by making it to the highly competitive second round of judging.*

## What It Does

We created an app called Crowdcast that takes your current location, searches for nearby bars, and detects how busy each venue is in real-time using computer vision. In particular, it can track how many people are currently at a given establishment, and it can also track how many people are waiting in line outside (as well as how long the wait time would be). Why head to a bar with your friends without knowing how packed it will be? Crowdcast searches all nearby bars and provides you with real-time knowledge if the bar you intended to go to is actually a feasible option.

## How It's Built

### Frontend

The frontend is a svelte powered single page application, that fetches data from the backend API, and displays a list of venues along with a map.

- Svelte
- Mapbox API
- SCSS
- CSS Custom Properties
- Bespoke style architecture (No CSS framework)


### Backend

The back-end was built with a Flask API, which in itself calls the Google Places API and Google Photo API to get information about nearby venues. It also retrieves information from our computer vision component built on OpenCV from some open source examples, which exposes a REST endpoint to provide the back-end with information about the current capacity and wait times for each venue.

- Python
- Flask
- Google Places API
- Google Photos API
- OpenCV


## Built By

James Patrick Gibson - [@negativespace.io](https://twitter.com/negativespaceio)

Thomas Gautier - [tng26](https://github.com/tng26)

Kevin Gaan – [kevingaan](https://github.com/kevingaan)
