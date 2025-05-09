# PlexTrailers
Python Script for getting movie/tv trailers for Plex Server Owners

Donations are most welcome for future updates at the link below.

https://www.paypal.com/ncp/payment/FFLG36H78KMHJ

This script is designed to automate the process of downloading YouTube videos from a webpage that contains a list of trailer links, including both direct and embedded YouTube links. Here's a breakdown of the key steps it performs:

Install Missing Packages: It checks if necessary Python packages (selenium, beautifulsoup4, requests) are installed and installs them if they are missing.

Verify Tools:

It verifies the installation of yt-dlp (a tool for downloading videos), ChromeDriver (needed for Selenium to control the browser), and FFmpeg (used for video conversion and processing). If any of these tools are missing, it installs them by downloading and setting them up.

Web Scraping with Selenium:

The script opens a webpage (https://www.themoviebox.net/s/trailer-round-up) and waits for a link containing "trailer-round-up" in its URL to appear.

Once the link is found, it navigates to that page and scrolls down for up to 5 minutes to load all the content.

Extract YouTube Links:

It uses BeautifulSoup and regular expressions to extract all YouTube video links (normal YouTube links and iframe embed links) from the page.

It also handles embedded video links that use the youtube-nocookie.com domain for privacy-conscious embeds.

Download YouTube Videos:

After collecting all YouTube links, it uses yt-dlp to download videos in 1080p quality (best video/audio) and saves them to a predefined directory (C:\Videos).

The script also ensures that video metadata (e.g., description) is embedded and thumbnails are included.

Error Handling and Logging:

It includes error handling to ensure the script doesn't crash if something goes wrong (like missing links or failed downloads) and logs the process along the way.

After the operation, it closes the browser to clean up resources.

The goal of the script is to automate the downloading of YouTube videos from a specific page of trailers, ensuring all required tools are installed and configured properly.
