import sys
import csv
from util import read_from_file, get_all_rooms, get_course_attr, get_readable_attrs, print_columns

if len(sys.argv) == 4:
    room, building, day = sys.argv[1:]
    day = day.upper()
else:
    room, building = sys.argv[1:]
    day = ''

courses = read_from_file(building)

rooms = get_all_rooms(courses)

in_room = sorted([c for c in courses if get_course_attr(c, 'room') == room and day in get_course_attr(c, 'days')])
in_room = [get_readable_attrs(c) for c in in_room]

if in_room:
    print_columns(in_room)
elif room in rooms:
    print('No courses')
else:
    print('Invalid room')
