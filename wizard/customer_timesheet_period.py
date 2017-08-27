# -*- coding: utf-8 -*-

from openerp import models, api, fields


class CustomerTimeSheet(models.TransientModel):

    """
    The Project Customer Timesheet is a transient model.

    used to print report timesheet that should be sent to the customer.
    """

    _name = 'project.customer.timesheet'
    _description = 'Project Customer Timesheet'

    project_id = fields.Many2one(comodel_name='project.project',
                                 string='Project',
                                 help='Select the project')
    user_id = fields.Many2one(comodel_name='res.users',
                              string='Resource',
                              help='Select the resource or leave it empty'
                                   ' to print timesheet for all resources')
    from_date = fields.Date(string='From Date')
    to_date = fields.Date(string='To Date')

    mode = fields.Selection([
        ('heur', 'Heure'),
        ('jour', 'Jour')
    ], string='Mode', default='jour')

    etp = fields.Selection([(str(i),str(i)) for i in range(1,25)] , string='Equivalent Temps Plein',  default='8')



    @api.multi
    def print_timesheet(self):
        """
        Select tasks depending the criteria choosed by the user.
        and generate the report to be sent to the customer
        """
        data = {'form': self.read(['project_id', 'user_id', 'from_date', 'to_date', ])[0]}
        return self.env['report'].get_action(self, 'altex_project.customer_timesheet', data=data)

