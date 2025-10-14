from odoo import fields, models, Command, api


class ProjectProject(models.Model):

    _inherit = "project.project"

    project_template_id = fields.Many2one("project.template", string="Project template")
    is_button_view = fields.Boolean(string="Is button view")


    @api.onchange('project_template_id')
    def link_project_template(self):
       tag_id_list = self.mapped('project_template_id.tag_ids')

       # task_id_list = self.project_template_id.search([])
       # for task in self.project_template_id.task_ids:
       #     task_id_list.append(Command.create({
       #         'name': task.name,
       #     }))

       # print('from from project sub',task_id_list)


       self.write({'name':self.project_template_id.name})
       self.write({'label_tasks':self.project_template_id.label_tasks})
       self.write({'user_id': self.project_template_id.user_id})
       self.write({'description': self.project_template_id.description})
       self.write({'tag_ids':tag_id_list})
       self.write({'partner_id':self.project_template_id.partner_id})
       self.write({'company_id':self.project_template_id.company_id})
       # self.update({
       #     'task_ids': [(fields.Command.set(id))]
       # })
       # self.update({
       #     'task_ids': [(fields.Command.set(a.id)) for a in task_id_list]
       # })







    def create_project_template(self):
        tag_ids_list = self.mapped('tag_ids')
        task_ids_list = []

        for task in self.task_ids:
            task_ids_list.append (Command.create({
                'name': task.name,
            }))

        self.is_button_view = True

        print("its task ids",self.task_ids)


        self.env['project.template'].create({
            'name':self.name,
            'label_tasks': self.label_tasks,
            'partner_id': self.partner_id.id,
            'user_id': self.user_id.id,
            'description': self.description,
            'tag_ids': tag_ids_list,
            'company_id':self.company_id.id,
         })


