
# USF Class Seat Finder

The USF Class Seat Finder script allows you to monitor the availability of seats for a specific course at the University of South Florida (USF). The script scrapes the USF Staff Schedule Search form and notifies you via a Discord webhook when a seat becomes available.

## Features

-   **Monitor course availability**: Automatically checks if a course has available seats.
-   **Customizable search criteria**: Specify semester, subject, course number, campus, and other preferences.
-   **Discord notifications**: Get real-time updates via a Discord webhook when seats are available.

## Prerequisites

Before using the script, make sure you have the following installed:

-   Python 3.x
-   Required Python packages:
    -   `requests`
    -   `beautifulsoup4`
    -   `pytz`

You can install the required packages using pip:

`pip install requests beautifulsoup4 pytz` 

## Usage

The script requires several arguments to run. These arguments allow you to specify the course information and the notification webhook.

### Required Arguments

-   **`-webhook`**: Your Discord webhook URL where notifications will be sent.
-   **`-semester`**: The semester identifier (e.g., `202408` for Fall 2024).
-   **`-subject`**: The subject code (e.g., `ECO` for Economics).
-   **`-course_num`**: The course number (e.g., `3203` for Intermediate Macroeconomics).

### Optional Arguments

-   **`-campus`**: The campus name (e.g., `Tampa`). Default is `None`.
-   **`-allow_online`**: Whether to allow online courses (`T` for True, `F` for False). Default is `None`.
-   **`-require_online`**: Whether to require the course to be online (`T` for True, `F` for False). Default is `None`.
-   **`-crn`**: A list of CRNs (Course Reference Numbers) to search for specific sections (e.g., `91412 91413 91414`). Default is an empty list.

### Example Command


`python usf_seat_finder.py -webhook "https://discord.com/api/webhooks/..." -semester "202408" -subject "ECO" -course_num "3203" -campus "Tampa" -allow_online "T" -require_online "F" -crn 91412 91413` 

This command checks for available seats in the course ECO 3203 for the Fall 2024 semester on the Tampa campus. It allows online courses but does not require them. It also checks specific sections with the provided CRNs.

## Notes

-   The script is designed to be run periodically (e.g., using a cron job) to continually check for seat availability.
-   Ensure that the webhook URL is correctly configured to receive notifications.
