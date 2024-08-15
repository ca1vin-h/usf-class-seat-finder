import argparse
import requests
from bs4 import BeautifulSoup
import pytz
from datetime import datetime

#initialize the parser
parser = argparse.ArgumentParser(description='Process course information.')

#required arguments
parser.add_argument('-webhook', required=True, help='Your discord webhook')
parser.add_argument('-semester', required=True, help='The semester identifier (e.g., 202408)')
parser.add_argument('-subject', required=True, help='The subject code (e.g., ECO)')
parser.add_argument('-course_num', required=True, help='The course number (e.g., 3203)')

#optional arguments
parser.add_argument('-campus', help='The campus name (e.g., Tampa)', default=None)
parser.add_argument('-allow_online', choices=['T', 'F'], help='Allow online courses (T/F)', default=None)
parser.add_argument('-require_online', choices=['T', 'F'], help='Require online courses (T/F)', default=None)
parser.add_argument('-test', action='store_true', help='Run in test mode')

#optional argument for multiple sections
parser.add_argument('-crn', nargs='*', help='List of crns to search for (e.g., 91412 91413 91414)', default=[])

# Parse the arguments
args = parser.parse_args()

webhook_url = args.webhook
semester = args.semester
subject = args.subject
course_num = args.course_num
campus = args.campus
allow_online = args.allow_online
require_online = args.require_online
selected_crns = args.crn
test_mode = args.test

print(f"Webhook: {webhook_url}")
print(f"Semester: {semester}")
print(f"CRNs: {subject}")
print(f"Course Number: {course_num}")
if campus:
    print(f"Campus: {campus}")
if allow_online:
    print(f"Allow Online: {allow_online}")
if require_online:
    print(f"Require Online: {require_online}")
if selected_crns:
    print(f"Sections: {', '.join(selected_crns)}")
print(f"Test Mode: {args.test}")


def requestData(P_SEMESTER, P_SUBJ, P_NUM):

    url = "http://usfweb.usf.edu/DSS/StaffScheduleSearch/StaffSearch/Results"
    data = {"P_SEMESTER": P_SEMESTER, "P_SUBJ": P_SUBJ, "P_NUM": P_NUM}

    # make the request using the above headers
    response = requests.post(url, data=data)

    # use beautiful soup to parse the html response from the staff search
    soup = BeautifulSoup(response.text, 'html.parser')

    # Replace all occurrences of '\u00a0' with ' ' in the BeautifulSoup object's strings (CRS SUBJ#)
    for string in soup.strings:
        if '\u00a0' in string:
            string.replace_with(string.replace('\u00a0', ' '))

    # replace br tags with space to help split classes that have different meeting times on different days
    for br_tag in soup.find_all('br'):
        br_tag.replace_with(' ')

    table = soup.find('table', id='results')

    # create the json object
    row_data = {}
    row_data["semester"] = P_SEMESTER
    row_data["subject"] = P_SUBJ
    row_data["number"] = P_NUM
    row_data["sections"] = []

    for row in table.find_all('tr')[1:]:
        # Store the rest of the data under the "sections" key
        sections = {}
        headers = [header.get_text().strip().replace('\n', ' ').replace(' ', '_').replace("#", "")
                   for header in table.find_all('th')]
        for i, cell in enumerate(row.find_all(['td'])):
            # print(cell.get_text().strip().replace('\xa0', ' '))
            sections[headers[i]] = cell.get_text().strip().replace('\xa0', ' ').replace("#", "")

        # Remove keys
        '''
        del_keys = ["SUBJ_CRS#"]
        for key in del_keys:
            if key in sections:
                del sections[key]
        '''

        # split schedules for classes that have multiple meet times
        sections['DAYS'] = sections['DAYS'].split(' ')
        sections['TIME'] = sections['TIME'].split(' ')
        sections['BLDG'] = sections['BLDG'].split(' ')
        sections['ROOM'] = sections['ROOM'].split(' ')

        # check if course is what was requested
        if not sections['SUBJ_CRS'] == P_SUBJ + ' ' + P_NUM:
            continue

        # remove dual enrollment only classes
        if "DUAL ENROLLMENT".lower() in sections['TITLE'].lower():
            continue
        


        if sections['DAYS'] == ['']:
            sections['DAYS'] = "ONLINE"
        else:
            #make date/time easier to use 
            dayDict = {'M': [], 'T': [], 'W': [], 'R': [], 'F': [], 'S': []}
            for day, time in zip(sections['DAYS'], sections['TIME']):
                for key in dayDict:
                    if key.upper() in day.upper():
                        dayDict[key].append(time)
            sections['DAYS'] = dayDict
        del sections['TIME']
        row_data["sections"].append(sections)
    return row_data

#try/catch loop to catch http errors gracefully
try:
    response = requestData(semester, subject, course_num)
except (requests.exceptions.RequestException, KeyError) as e:
    tampa_sections = []
    print(f"A Staff Search error occurred: {e}")
    exit()
    
returned_sections = [section for section in response['sections']]
ok_sections = []
#print(returned_sections)

#iterate through sections available for course
for section in returned_sections:
    #check there are seats open
    if not test_mode:
        try: 
            if not (int(section['SEATS_REMAIN']) > 0):
                #print(str(section) + str(section['SEATS_REMAIN']))
                continue
        #catch error if value is not an int
        except ValueError:
            print("Value error detected! Please message the creator of this script with the course you attempted to search!")
            continue
    
    #check if sections selected are available
    if selected_crns:
        if section['CRN'] in selected_crns:
            ok_sections.append(section)
            continue
        else:
            continue
    
    #check if online classes allowed
    if allow_online:
        if allow_online == 'T':
            if section['DAYS'] == 'ONLINE':
                ok_sections.append(section)
                continue
        elif section['DAYS'] == 'ONLINE':
            continue
    
    #check if online classes required
    if require_online:
        if require_online == 'T':
            if section['DAYS'] == 'ONLINE':
                ok_sections.append(section)
                continue
            else:
                continue
    
    #check for campus
    if campus:
        if section['CAMPUS'] == campus:
            ok_sections.append(section)
            continue
        else:
            continue
        
    #default case for courses not filtered out
    ok_sections.append(section)
    
#check if no seats found
if ok_sections == []:
    print("No seats found")
    exit()


#create discord message string
course_info = 'Semester: ' + semester + '\nSubject: ' + subject + '\nCourse Number: ' + course_num + '\nCurrent Time: '+ datetime.now(pytz.timezone('US/Eastern')).strftime('%Y-%m-%d %H:%M:%S %Z%z')
sections_found = ''
for section in ok_sections:
    sections_found = sections_found + 'CRN: ' + section['CRN'] + '\n'
    sections_found = sections_found + 'Seats Available: ' + section['SEATS_REMAIN'] + '\n'
    sections_found = sections_found + 'Section Number: ' + section['SEC'] + '\n'
    sections_found = sections_found + 'Professor: ' + section['INSTRUCTOR'] + '\n'
    sections_found = sections_found + 'Campus: ' + section['CAMPUS'] + '\n'
    if section['DAYS'] == 'ONLINE':
        sections_found = sections_found + 'Online: True\n\n'
    else: 
        sections_found = sections_found + 'Online: False\n\n'

if not test_mode:
    discord_message = "Open sections found!\n" + course_info + '\n\n' + sections_found
else:
    discord_message = "Testing the script!\n" + course_info + '\n\n' + sections_found

#discord max message limit is 2000 characters, if the message is larger than 2000 characters a message will be displayed and the string length will be reduced
if len(discord_message) > 2000:
    discord_message = discord_message[:1900] + '...\nMore sections found! Consider narrowing down your search.'

data = {
    "content": discord_message,
    "username": "usf course seat finder bot"
}
try:
    response = requests.post(webhook_url, json=data)
    if response.status_code == 204:
        print("Message sent successfully!")
    else:
        print(f"Failed to send message: {response.status_code}")
    pass
except (requests.exceptions.RequestException, KeyError) as e:
    print(f"A Discord error occurred: {e}")
    pass



exit()
for sec in ok_sections:
    print(sec)
    print()
    print()
