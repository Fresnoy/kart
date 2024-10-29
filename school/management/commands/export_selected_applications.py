import pandas as pd

from django.core.management.base import BaseCommand

from django.db.models import Q

from django.contrib.auth.models import User
from school.models import AdminStudentApplication, StudentApplication, StudentApplicationSetup, Promotion
from people.models import Artist, FresnoyProfile


class Command(BaseCommand):
    help = "Export selected candidature to CSV"

    def add_arguments(self, parser):
        # Args
        parser.add_argument("--campaign_id", type=int, help="Export candidature's campaign Id")

    def handle(self, *args, **options):
        # set param vars
        campaign_id = options["campaign_id"]

        # get the current campaign
        campaign = StudentApplicationSetup.objects.filter(Q(id=campaign_id) | Q(is_current_setup=True)).first()
        # get select or waitlisted applications
        admins_sa = AdminStudentApplication.objects.filter(application__campaign=campaign).filter(
            Q(wait_listed=True) | Q(selected=True)
        )

        # create csv header with all models rows
        profile_rows = [
            "application__artist__user__profile__" + field.name for field in FresnoyProfile._meta.get_fields()
        ]
        user_rows = ["application__artist__user__" + field.name for field in User._meta.get_fields()]
        artist_rows = ["application__artist__" + field.name for field in Artist._meta.get_fields()]
        promo_rows = ["application__campaign__promotion__" + field.name for field in Promotion._meta.get_fields()] 
        campaign_rows = ["application__campaign__" + field.name for field in StudentApplicationSetup._meta.get_fields()] 
        app_rows = ["application__" + field.name for field in StudentApplication._meta.get_fields()]
        admin_app_rows = [field.name for field in AdminStudentApplication._meta.get_fields()]
        # concat them
        all_rows = admin_app_rows + campaign_rows + promo_rows + app_rows + artist_rows + profile_rows + user_rows
        # add header in top of CSV
        csv_head = pd.DataFrame([all_rows]).to_csv(index=False, header=False)

        # Query values with all headers cols. Have to drop duplicates i don't know why
        csv_data = (
            pd.DataFrame(data=admins_sa.values_list(*all_rows, named=True), columns=all_rows)
            .drop_duplicates('id')
            .to_csv(index=False, header=False)
        )
        # open / write csv
        f = open("applications.csv", 'w', encoding='utf-8')
        f.write(csv_head)
        f.write(csv_data)
        f.close()

        print('Data written to applications.csv')
