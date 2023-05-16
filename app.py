
def enquirydata():
    from django.utils import timezone
    from datetime import timedelta
    from enquiry.models import enquiry
    import random
    import names
    for i in range(100):
        name = names.get_full_name()
        x = enquiry.objects.create(
            student_name = name,
            student_phone= '9999999999',
            student_email = 'abc@abc.com',
            student_address = '123 Main st',
            current_education_id = 1,
            country_interested_id=1,
            university_interested_id = 1,
            level_applying_for_id = 1,
            course_interested_id = 55,
            intake_interested_id = 2,
            assigned_users_id =1,
            enquiry_status_id =1,
            added_by_id = 1,
            date_created = timezone.now() - timedelta(days=random.randint(0, 100))
        )

