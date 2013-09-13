import sys
import csv
from util import read_from_file, get_all_rooms, get_course_attr, get_readable_attrs, print_columns, time_set

times, building, day = sys.argv[1:]
day = day.upper()

search_times = time_set(times)

courses = read_from_file(building)

rooms = get_all_rooms(courses)

whole_day = set(range(0, 1440))

results = []

for room in rooms:
    courses_in_room = [c for c in courses if get_course_attr(c, 'room') == room and day in get_course_attr(c, 'days')]
    busy_times = set()
    for course in courses_in_room:
        busy_times |= time_set(get_course_attr(course, 'rawtime'))
    available_times = whole_day - busy_times
    if search_times <= available_times:
        results.append(room)

print('Found {0} results'.format(len(results)))
results = sorted(results, key=lambda x: x.rjust(99)) # Sort, putting shorter room numbers first
for item in results:
    print(item)
