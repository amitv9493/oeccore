import csv

from .models import Course

from oeccore.settings import BASE_DIR

def readfile():
    """
    inserting a large csv data into models 
    """
    fields = []
    rows = []
    with open(BASE_DIR /'coursesflynew.csv', "r") as file:
        csvreader = csv.reader(file)
        fields = next(csvreader)

        for row in csvreader:
            rows.append(row)

        obj = [Course(
        university_id=int(i[0]),
        course_name=i[1],
        course_levels_id=int(i[2]),
        documents_required_id=int(i[4]),
        course_requirements_id=int(i[5]),
        Active=int(i[6]),

        ) for i in rows]

    msg =Course.objects.bulk_create(objs=obj)
    print('done')
