import urllib.request
import urllib.parse
import csv
from bs4 import BeautifulSoup

def print_error(msg):
    VISIBLE_ERROR = '##### Error: '
    print(VISIBLE_ERROR + msg)

def grab_soup(building):
    """Given a building name, return a Soup object of search results, containing
    all courses found in that building."""
    url = 'http://osoc.berkeley.edu/OSOC/osoc'
    values = {'p_term':'FL', 'p_bldg':building, 'p_print_flag':'Y'}
    data = bytes(urllib.parse.urlencode(values),'utf-8') # or bytearray?
    req = urllib.request.Request(url, data)
    response = urllib.request.urlopen(req)
    html = response.read()
    return BeautifulSoup(html)

def any_classes_found(soup):
    """Given a Soup object of search results, print an error message if no
    classes were found."""
    if 'No classes match' in soup.text:
        print_error('no classes found')

def get_courses(building):
    """
    tag objects."""
    soup = grab_soup(building)
    any_classes_found(soup)
    total = int(soup.find_all('font')[-2].text.strip().split()[1])
    rows = soup.find_all('tr')
    num_cols = lambda row: str(row).count('<td')
    first_col = lambda row: str(row.font.text.strip())
    courses = [row for row in rows if num_cols(row) == 11 and first_col(row) != 'ControlNumber']
    if total != len(courses): # Sanity check
        print_error('found {0} courses (should be {1})'.format(len(courses), total))
    return courses

def scrape_course_data(course):
    """Given a course as a soup tag object, return a list of strings containing
    the course data."""
    cols = course.find_all('td')[1:]
    return [col.text.strip().replace('\xa0',' ') for col in cols]

def get_course_info(course):
    """Given a course as soup tag object, return a list of just the relevant
    information, with days and time processed."""
    data = scrape_course_data(course)
    rawdays, rawtime = data[3].split()
    days = fix_days(rawdays)
    start, end = fix_times(rawtime)
    room = data[4].split()[0]
    title = data[5]
    ccn = data[0]
    return [start, room, rawtime, days, rawdays, ccn, title]

ATTRIBUTES = {'start':   0,
              'room':    1,
              'rawtime': 2,
              'days':    3,
              'rawdays': 4,
              'ccn':     5,
              'title':   6}
def get_course_attr(course, attr):
    return course[ATTRIBUTES[attr]]

def get_readable_attrs(course):
    return course[2:]

def fix_days(days):
    """Convert OSOC's day format to a queriable format.
    
    >>> fix_days('MTWTF')
    'MTWHF'
    >>> fix_days('TuTh')
    'TH'
    """
    days = days.replace('Tu','T')
    days = days.replace('Th','H')
    if days.count('T') == 2:
        a, b = days.split('T',1)
        b = b.replace('T','H')
        days = 'T'.join([a, b])
    return days

def fix_times(times):
    """Convert OSOC's time format to a list of the format [start, end], (where
    "start" and "end" are minutes past midnight) which is useful for sorting.
    The numbers "start" and "end" are given as four-digit strings.
    
    >>> fix_times('1-4P')
    ['0780', '0960']
    """
    start, end = times.split('-')
    end, ampm = end[:-1], end[-1]
    if len(start) in (1, 2): start = [int(start), 0]
    else: start = [int(start[:-2]), int(start[-2:])]
    if len(end) in (1, 2): end = [int(end), 0]
    else: end = [int(end[:-2]), int(end[-2:])]
    if end[0] == 12 and ampm == 'A':
        end[0] = 24
        start[0] += 12
    elif not(end[0] == 12 and ampm == 'P' or ampm == 'A'):
        end[0] += 12
        if start[0] <= end[0]-12:
            start[0] += 12
    return [str(x[0]*60 + x[1]).zfill(4) for x in [start, end]]

def time_range(times):
    """Given a start and end time as either the input or output of fix_times,
    return a range object corresponding to that time range."""
    if type(times) == list:
        start, end = [int(t) for t in times]
        return range(start, end)
    return time_range(fix_times(times))

def time_set(times):
    """Given a start and end time as either the input or output of fix_times,
    return a set corresponding to that time range."""
    return set(time_range(times))

def write_to_file(lst, filename):
    """Writes a list to an output file."""
    with open('buildings/' + filename + '.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, lineterminator='\n')
        writer.writerows(lst)

def read_from_file(building):
    """Given the name of a building, return the data in that csv file."""
    with open('buildings/' + building + '.csv', 'r') as csvfile:
        courses = list(csv.reader(csvfile))
    return courses

def get_all_rooms(courses):
    """Given a list of courses in a building, return the sorted list of all the
    rooms in that building."""
    return sorted(set([get_course_attr(c, 'room') for c in courses]))

def find_courses(courses, room, day):
    pass

def print_trunc(s):
    """Print a string, truncated if necessary to keep it on one 80-char line."""
    if len(s) > 80:
        print(s[:77] + '..\\', end='')
    elif len(s) == 80:
        print(s, end='')
    else:
        print(s)

def print_columns(matrix):
    """Given a 2-dimensional list of strings, print in columns."""
    widths = [0]*len(matrix[0])
    for row in matrix:
        for i, elem in enumerate(row):
            widths[i] = max(widths[i], len(elem))
    for row in matrix:
        line = ''
        for i, elem in enumerate(row[:-1]):
            line += elem.ljust(widths[i] + 2)
        line += row[-1]
        print_trunc(line)
