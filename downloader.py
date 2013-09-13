from util import get_courses, get_course_info, write_to_file
import sys

building = sys.argv[1]
courses = get_courses(building)
info = [get_course_info(c) for c in courses]

rename = {'valley lsb': 'vlsb'}

if building in rename:
    building = rename[building]

write_to_file(info, building)
