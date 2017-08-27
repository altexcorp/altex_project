# -*- coding: utf-8 -*

from datetime import date
from openerp import api, models

class ReportCustomerTimeSheet(models.AbstractModel):

    _name = 'report.altex_project.customer_timesheet'

    def get_timesheet(self, doc):
        """
         Get the time sheet depending the data selected by the user
        """
        AnalyticLineObj = self.env['account.analytic.line']

        domain = [('account_id', '=', doc.project_id.analytic_account_id.id),
                  ('user_id', '=', doc.user_id.id),
                  ('date', '>=', doc.from_date),
                  ('date', '<=', doc.to_date)]

        data = {}
        task_list = []
        # Creation du dictionnaire
        activity_ids = AnalyticLineObj.search(domain)
        sorter_activities = activity_ids.sorted(key=lambda r: r.date)

        for activity in sorter_activities:
            if activity.task_id.name not in task_list:
                task_list.append(activity.task_id.name)
            if activity.date in data:
                data[activity.date]['activities'].append(activity.name)
                data[activity.date]['durations'].append(activity.unit_amount)
                data[activity.date]['task'].append(activity.task_id.name)
            else:
                data.update({activity.date: {'activities': [activity.name], #
                                             'task': [activity.task_id.name],
                                             'date': activity.date,
                                             'durations':[activity.unit_amount],
                                             }})
        print 'gjklmlkjhgf',data
        res = []
        for key in sorted(data):
            res.append(data[key])
        print "res",res
        return res

    @api.multi
    def render_html(self, data):
        model = self.env.context.get('active_model')
        doc = self.env[model].browse(self.env.context.get('active_id'))
        report_lines = self.get_timesheet(doc)
        docargs = {
            'doc_ids': self._ids,
            'doc_model': model,
            'docs': doc,
            'time': date,
            'get_timesheet': report_lines,

        }
        return self.env['report'].render('altex_project.customer_timesheet', docargs)
