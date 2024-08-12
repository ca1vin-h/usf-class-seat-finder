import requests
import requests
from bs4 import BeautifulSoup
import json

#Discord webhook URL
webhook_url = ''

semester = '202408'
subject = 'PHY'
course_num = '2049'

valid_CRNs = ''

# requests data from url with headers
# returns the data in json format
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


'''
with open(semester +'_'+ subject +'_'+ course_num + '.json', 'w') as f:
    json.dump(requestData(semester, subject, course_num), f)
'''

#try/catch loop to catch http errors gracefully
try:
    response = requestData(semester, subject, course_num)
    tampa_sections = [section for section in response['sections'] if section['CAMPUS'] == "Tampa"]
except (requests.exceptions.RequestException, KeyError) as e:
    tampa_sections = []
    print(f"An error occurred: {e}")
    exit()

for section in tampa_sections:
    try: 
        if(int(section['SEATS_REMAIN']) > 0):
            valid_CRNs = valid_CRNs + ' ' + section['CRN']
            pass
    #catch error if value is not an int
    except ValueError:
        pass
    

# create message for discord webhook
if valid_CRNs == '':
    print("No courses found")
    exit()
data = {
    "content": "Sections found in Tampa:" + valid_CRNs,
    "username": semester +'_'+ subject +'_'+ course_num  # Optional: Set the name of the bot
}

try:
    response = requests.post(webhook_url, json=data)
    if response.status_code == 204:
        print("Message sent successfully!")
    else:
        print(f"Failed to send message: {response.status_code}")
    pass
except (requests.exceptions.RequestException, KeyError) as e:
    print(f"An error occurred: {e}")
    pass
    
