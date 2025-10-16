# -*- encoding: utf-8 -*-
from django.core.management.base import BaseCommand

from school.utils import candidature_close, send_candidature_not_finalized_to_candidats_after_date_end
from school.models import StudentApplication, StudentApplicationSetup

from datetime import datetime, date, timedelta

# Can us with crontab
# example : run every day at 15h00
# 00 15 * * * . /path/to/activate && /path/to/manage.py application_end_date_reminder --automatic_reminder
# '.' mean bash


class Command(BaseCommand):
    help = "Sends an email to candidates who have not completed their application after the end date"

    def add_arguments(self, parser):
        # Args
        parser.add_argument("--novalidation", action="store_true", help="No validation required")
        parser.add_argument(
            "--automatic_reminder",
            action="store_true",
            help="Send email one week after the end date for current campaign",
        )

    def handle(self, *args, **options):
        # set auto for cronjob
        automatic_reminder = options["automatic_reminder"]
        # no validation for cron
        novalidation = True if automatic_reminder else options["novalidation"]

        if automatic_reminder:
            print("{}".format(datetime.now()))

        # is the campaign open
        candidatures_close = candidature_close()
        if not candidatures_close:
            print("Campaign is open")
            return False

        # get the current campaign
        campaign = StudentApplicationSetup.objects.filter(is_current_setup=True).first()
        if not campaign:
            print("Campaign not found")
            return False

        # is one of the automatic send day (compare dates with != no 'is not') without hours
        if automatic_reminder and (campaign.candidature_date_end.date() + timedelta(days=7)) != date.today():
            print(
                "{} : Ce n'est pas le jour ({}), aucun email de relance de candidature n'a été envoyé".format(
                    date.today(), str(campaign.candidature_date_end.date()) + " + 7 jours"
                )
            )
            return False

        all_applications = StudentApplication.objects.filter(campaign=campaign).count()
        # Candidat who havn't send application
        query_applications_started__emails = StudentApplication.objects.filter(
            campaign=campaign,
            application_completed=False,
        ).values_list("artist__user__email", flat=True)
        # convert QuerySet to list
        list_emails = list(query_applications_started__emails)
        # question
        str_question = "Vous allez envoyer un email à {} candidats " "(pour {} candidatures au total)? (y/n)".format(
            len(list_emails), all_applications
        )
        # ask or not
        confirm = "y" if novalidation else None
        if not confirm:
            confirm = input(str_question).lower().strip()

        if confirm != "y":
            print("Aucun email n'a été envoyé")
            return
        #
        mail_sent = send_candidature_not_finalized_to_candidats_after_date_end(self, campaign, list_emails)
        if mail_sent:
            print("{} Emails envoyés : {}".format(len(list_emails), list_emails))
        else:
            print("Erreur email ")
