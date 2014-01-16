from django.db import models
from django.db import connection

class Dashboard(object):
    def getTotalInvoiced(self, userId):
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT round(sum(amount),2) total_invoiced
            FROM devtracker.time_tracking_invoice_amounts t
            where user_id = %d
            and sent_date is not null
            """ % (userId)
        )

        row = cursor.fetchone()

        try:
            return row[0]
        except:
            return "0.00"

    def getTotalPaid(self,userId):
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT round(ifnull(sum(amount),0.00),2) total_paid
            FROM devtracker.time_tracking_invoice_amounts t
            where user_id = %d
            and paid_date is not null
            """ % (userId)
        )

        row = cursor.fetchone()

        try:
            return row[0]
        except:
            return "0.00"