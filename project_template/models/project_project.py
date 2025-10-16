from odoo import fields, models, Command, api


class ProjectProject(models.Model):

    _inherit = "project.project"

    project_template_id = fields.Many2one("project.template", string="Project template", readonly=True)
    project_project_template_count = fields.Integer(string="Template Count", compute="count_of_project_project")
    project_template_ids = fields.One2many("project.template", "project_id", string="Project Templates")


    def count_of_project_project(self):
        self.write({'project_project_template_count':len(self.project_template_ids)})



    def create_project_template(self):
        tag_ids_list = self.mapped('tag_ids')

        # task_ids_list = [(fields.Command.create(a.name)) for a in  self.task_ids]
        # task_ids_list = []
        # for task in self.task_ids:
        #     task_ids_list.append(Command.create({
        #         'name': task.name,
        #     }))
        #
        task_ids_list = [(fields.Command.create({'name': a.name})) for a in  self.task_ids]



        print("task_ids_list", task_ids_list)




        created_template_id = self.env['project.template'].create({
            'name':f'PR/{self.id}/{self.name} - {self.partner_id.name if self.partner_id.name else ''}',
            'label_tasks': self.label_tasks,
            'partner_id': self.partner_id.id,
            'user_id': self.user_id.id,
            'description': self.description,
            'tag_ids': tag_ids_list,


            'project_task_template_ids':task_ids_list,


            'company_id':self.company_id.id,
            'project_id':self.id,
         })




        return {
            'type': 'ir.actions.act_window',
            'name': 'Project Templates',
            'res_model': 'project.template',
            'view_mode': 'form',
            'target': 'current',
            'res_id': created_template_id.id,
        }

    def see_project_template(self):

    
        print("Sondham Id",self.id)
        print("apparathe ID", self.project_template_ids.project_id)
        return {
            'type': 'ir.actions.act_window',
            'name': 'Related Project',
            'res_model': 'project.template',
            'view_mode': 'list,form',
            'target': 'current',
            'domain':([('project_id','=',self.id)])


        }





