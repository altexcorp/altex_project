# -*- coding: utf-8 -*-
from openerp import api
from openerp import exceptions
from openerp import fields
from openerp import models


ALTEX_PROJECT = 'altex.project.'


class Project(models.Model):

    """Inherit Project Model to add code and image fields."""

    _inherit = 'project.project'

    code = fields.Char(string='Project Code',
                       size=10,
                       help='Project Code will be used in task code')

    image = fields.Binary(string='Project Image', related='partner_id.image')

    @api.model
    def create(self, vals):
        """Create ir.sequence for each created project."""
        record = super(Project, self).create(vals)

        if record.code:
            self.env['ir.sequence'].create({
                'name': record.name,
                'code': ALTEX_PROJECT + record.code,
                'prefix': record.code + '-',
                'padding': 4,
                'implementation': 'no_gap'
            })
        return record

    @api.multi
    @api.constrains('code')
    def _check_code_unique(self):
        assert self.ensure_one()
        project_ids = self.search([])
        for project in project_ids:
            if project.code == self.code and project != self:
                raise exceptions.ValidationError('The project code must be unique')

    @api.one
    def write(self, vals):
        """Don't Allow the update of the project code."""
        if 'code' in vals and len(self.task_ids) > 0:
            raise exceptions.ValidationError(
                'The project Code cannot be updated. '
                'Otherwise all the task code has to change')
        return super(Project, self).write(vals)


class Task(models.Model):

    """Inherit Project Model to add code and image fields."""

    _inherit = 'project.task'

    code = fields.Char(string='Task Code', copy=False)

    @api.model
    def create(self, vals):
        """Generate Task code using project code and sequence."""
        Project = self.env['project.project']
        Sequence = self.env['ir.sequence']
        if 'code' not in vals:
            if 'project_id' in vals:
                project = Project.browse([vals['project_id']])
                vals['code'] = Sequence.next_by_code(ALTEX_PROJECT + project.code)

        if not vals['code']:
            raise exceptions.ValidationError("a Task must have a code")
        record = super(Task, self).create(vals)
        # Notify Project Followers of the project about the creation of the task.
        record.notify_task_created()
        return record

    @api.one
    def write(self, vals):

        result = super(Task, self).write(vals)
        if 'user_id' in vals:
            self.notify_task_assigned()
        if 'stage_id' in vals:
            self.notify_task_changed()

        return result

    @api.multi
    def notify_task_created(self):

        assert self.ensure_one()
        subject = "Creation D'une Nouvelle Tâche Pour Le Project: " \
                  "<b>" + self.project_id.name.encode('utf-8') + "</b>."
        message = "Je tiens à vous informer que la tâche " \
                  "<b> " + self.code.encode('utf-8') + " </b> portant l’intitulé: <em>" \
                  + self.name.encode('utf-8') + "</em>. \n <p> La tâche cocerne le problème: " \
                  + self.description.encode('utf-8') + "\n" \
                  "<p> Le temps estimé pour la résolution de cette problématique est de: <b>" \
                  + str(self.planned_hours) + "</b> Heure(s)"

        self.message_post(subject=subject,
                          body=message,
                          message_type='notification',
                          partner_ids=[follower.partner_id.id for follower in self.message_follower_ids])

    @api.multi
    def notify_task_assigned(self):

        subject = "Mise à Jour De La Tâche: <b>" + self.code.encode('utf-8') + "</b>"
        message = "Je tiens à vous informer que la tâche " \
                  "<b> " + self.code.encode('utf-8') + " </b> portant l’intitulé: <em>" \
                  + self.name.encode('utf-8') + "</em>, actuellement est assurée par: <b>" \
                  + self.user_id.name.encode('utf-8') + "</b>."

        self.message_post(subject=subject,
                          body=message,
                          message_type='notification',
                          partner_ids=[follower.partner_id.id for follower in self.message_follower_ids])

    @api.multi
    def notify_task_changed(self):

        assert self.ensure_one()
        subject = "Mise à Jour De La Tâche: <b>" + self.code.encode('utf-8') + "</b>"
        message = "Je tiens à vous informer que la tâche " \
                  "<b> " + self.code.encode('utf-8') + " </b> portant l’intitulé: <em>" \
                  + self.name.encode('utf-8') + "</em>. actuellement détient le statut: <b>" \
                  + self.stage_id.name.encode('utf-8') + "</b>."

        print "stage updated", self.code.encode('utf-8')

        print "FOLLOWERS", [follower.id for follower in self.message_follower_ids]
        self.message_post(body=message,
                          subject=subject,
                          subtype='project.mt_project_task_stage',
                          message_type='notification',
                          partner_ids=[follower.partner_id.id for follower in self.message_follower_ids])




