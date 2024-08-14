
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

-   **`-webhook`** (str): Your Discord webhook URL where notifications will be sent.
-   **`-semester`** (str): The semester identifier (e.g., `202408` for Fall 2024).
-   **`-subject`** (str): The subject code (e.g., `ECO`).
-   **`-course_num`** (str): The course number (e.g., `3203`).

### Optional Arguments

-   **`-campus`** (str): The campus name (e.g., `Tampa`). Default is `None`.
-   **`-allow_online`** (str): Whether to allow online courses (`T` for True, `F` for False). Default is `None`.
-   **`-require_online`** (str): Whether to require the course to be online (`T` for True, `F` for False). Default is `None`.
-   **`-crn`** (list of str): A list of CRNs (Course Reference Numbers) to search for specific sections (e.g., `91412 91413 91414`). Default is an empty list.

### Examples


This command checks for available seats in the course ECO 3203 for the Fall 2024 semester on the Tampa campus. It allows online courses but does not require them. It also checks specific sections with the provided CRNs.

Basic Search:

`python class_seat_finder.py -webhook https://discord.com/api/webhooks/your_webhook -semester 202408 -subject ECO -course_num 3203`

Search with Campus and Online Requirement:

`python class_seat_finder.py -webhook https://discord.com/api/webhooks/your_webhook -semester 202408 -subject ECO -course_num 3203 -campus Tampa -require_online T`

Search for Specific CRNs:

`python class_seat_finder.py -webhook https://discord.com/api/webhooks/your_webhook -semester 202408 -subject ECO -course_num 3203 -crn 91412 91413`

## Example Output

### Open Sections Found!

**Semester:** 202408  
**Subject:** ENC  
**Course Number:** 1101  
**Current Time:** 2024-08-13 19:27:49 EDT-0400

#### Available Sections

- **CRN:** 89191  
  **Seats Available:** 20  
  **Section Number:** 709  
  **Professor:** Staff  
  **Campus:** Off-campus - Tampa  
  **Online:** True

- **CRN:** 89192  
  **Seats Available:** 20  
  **Section Number:** 710  
  **Professor:** Staff  
  **Campus:** Off-campus - Tampa  
  **Online:** True

- **CRN:** 89193  
  **Seats Available:** 20  
  **Section Number:** 711  
  **Professor:** Staff  
  **Campus:** Off-campus - Tampa  
  **Online:** True

- **CRN:** 89194  
  **Seats Available:** 20  
  **Section Number:** 712  
  **Professor:** Staff  
  **Campus:** Off-campus - Tampa  
  **Online:** True

- **CRN:** 91968  
  **Seats Available:** 20  
  **Section Number:** 525  
  **Professor:** Staff  
  **Campus:** Off-campus - Sarasota-Manatee  
  **Online:** True

- **CRN:** 91743  
  **Seats Available:** 1  
  **Section Number:** 521  
  **Professor:** Angelique Hobbs Medvesky  
  **Campus:** Sarasota-Manatee  
  **Online:** False

- **CRN:** 89238  
  **Seats Available:** 1  
  **Section Number:** 009  
  **Professor:** Nicholas Giordano Guilfoile  
  **Campus:** Tampa  
  **Online:** False

- **CRN:** 89251  
  **Seats Available:** 1  
  **Section Number:** 020  
  **Professor:** Katrina Lynn Sandefer  
  **Campus:** Tampa  
  **Online:** False

- **CRN:** 93100  
  **Seats Available:** 1  
  **Section Number:** 047  
  **Professor:** Olajide Abdulrahman Omojarabi  
  **Campus:** Tampa  
  **Online:** False

- **CRN:** 89288  
  **Seats Available:** 19  
  **Section Number:** 053  
  **Professor:** Staff  
  **Campus:** Tampa  
  **Online:** False

- **CRN:** 89293  
  **Seats Available:** 1  
  **Section Number:** 057  
  **Professor:** Elizabeth Pottinger  
  **Campus:** Tampa  
  **Online:** False

- **CRN:** 89294  
  **Seats Available:** 18  
  **Section Number:** 058  
  **Professor:** Staff  
  **Campus:** Tampa  
  **Online:** False

- **CRN:** 89296  
  **Seats Available:** 5  
  **Section Number:** 060  
  **Professor:** Estrella Garcia-Calvo  
  **Campus:** Tampa  
  **Online:** False

- **CRN:** 89304  
  **Seats Available:** 1  
  **Section Number:** 066  
  **Professor:** Isabella Susan Rabadi  
  **Campus:** Tampa  
  **Online:** False

- **CRN:** 89307  
  **Seats Available:** 2  
  **Section Number:** 069  
  **Professor:** William Hal Walker  
  **Campus:** Tampa  
  **Online:** False

- **CRN:** 89308  
  **Seats Available:** 4  
  **Section Number:** 070  
  **Professor:** Anthony Joseph Borruso  
  **Campus:** Tampa  
  **Online:** False

**More sections found! Consider narrowing down your search.**

## Notes

-   The script is designed to be run periodically (e.g., using a cron job) to continually check for seat availability.
-   Ensure you replace <webhook_url> with your actual Discord webhook URL.
-   The semester identifier must be in the format YYYYMM.
