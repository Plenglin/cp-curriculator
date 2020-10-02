from collections import namedtuple

CourseGroup = namedtuple('CourseGroup', 'units courses')
Curriculum = namedtuple('CourseGroup', 'name root_group')
Subject = namedtuple('Subject', 'name code href')
Course = namedtuple('Course', 'subject number name')

