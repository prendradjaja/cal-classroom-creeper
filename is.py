import sys
import code
import csv
from util import read_from_file, get_all_rooms, get_course_attr, get_readable_attrs, print_columns

if len(sys.argv) == 2:
    building = sys.argv[1]
else:
    building = input().strip()

courses = read_from_file(building)

rooms = get_all_rooms(courses)

code.interact(local = locals())
