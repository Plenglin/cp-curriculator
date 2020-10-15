from collections import namedtuple

CourseGroup = namedtuple('CourseGroup', 'units courses')
"""
A group of courses. Units is how many units you need to take in that group,
and courses is a list of valid courses that can potentially satisfy that 
group.
"""

Curriculum = namedtuple('CourseGroup', 'name root_group')
Subject = namedtuple('Subject', 'name code href')
Course = namedtuple('Course', 'subject number name')

