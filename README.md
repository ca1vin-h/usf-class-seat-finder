
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

`python class_seat_finder.py -webhook <webhook_url> -semester <semester_id> -subject <subject_code> -course_num <course_number> [-campus <campus_name>] [-allow_online <T/F>] [-require_online <T/F>] [-crn <crn_list>]`

### Required Arguments

-   **`-webhook`** (str): Your Discord webhook URL. This URL is used to send notifications when seats are available.
-   **`-semester`** (str): The semester identifier (e.g., `202408` for Fall 2024). The format should be YYYYMM.
-   **`-subject`** (str): The subject code (e.g., `ECO`). This represents the department of the course.
-   **`-course_num`** (str): The course number (e.g., `3203`). This identifies the specific course.

### Optional Arguments

-   **`-campus`** (str): The campus name (e.g., `Tampa`). If provided, the search will be restricted to this campus. Default is `None`.
-   **`-allow_online`** (str): Allow online courses (`T` or `F`). If set to `T`, online courses will be included in the search results. If `F`, online courses will be excluded. Default is `None`.
-   **`-require_online`** (str): Require online courses (`T` or `F`). If set to `T`, only online courses will be included. Default is `None`.
-   **`-crn`** (list of str): List of CRNs to search for (e.g., `91412 91413 91414`). If specified, the script will check availability for these specific CRNs. Default is an empty list.

## Examples

### Basic Search:

`python class_seat_finder.py -webhook https://discord.com/api/webhooks/your_webhook -semester 202408 -subject ECO -course_num 3203`

### Search with Campus and Online Requirement:

`python class_seat_finder.py -webhook https://discord.com/api/webhooks/your_webhook -semester 202408 -subject ECO -course_num 3203 -campus Tampa -require_online T`

### Search for Specific CRNs:

`python class_seat_finder.py -webhook https://discord.com/api/webhooks/your_webhook -semester 202408 -subject ECO -course_num 3203 -crn 91412 91413`

## Example Output

Open Sections Found!

**Semester:** 202408  
**Subject:** ENC  
**Course Number:** 1101  
**Current Time:** 2024-08-13 19:27:49 EDT-0400

- **CRN:** 89191  
  **Seats Available:** 20  
  **Section Number:** 709  
  **Professor:** Staff  
  **Campus:** Off-campus - Tampa  
  **Online:** True

- **CRN:** 91743  
  **Seats Available:** 1  
  **Section Number:** 521  
  **Professor:** Angelique Hobbs Medvesky  
  **Campus:** Sarasota-Manatee  
  **Online:** False


## Notes

-   The script is designed to be run periodically (e.g., using a cron job) to continually check for seat availability.
-   Ensure you replace <webhook_url> with your actual Discord webhook URL.
-   The semester identifier must be in the format YYYYMM.
