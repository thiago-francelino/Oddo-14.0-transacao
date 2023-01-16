from odoo import models, fields, api, _


class InheritPayment(models.Model):
    _inherit = 'account.payment'
    gerproc_id = fields.Many2one("project_request")
    gerproc_parametro = fields.Boolean()
    # pagamento_com_cheque_id = fields.Many2one('cadastro.cheque', string="Pagamento com o cheque")


    #necessaria a criação destes 3 campos a seguir pois existem no xml mas não no python
    effective_date = fields.Date()
    bank_reference = fields.Char()
    cheque_reference = fields.Char()



    def atualizar(self):
        env = self.env['account.payment'].search([], order="id asc")
        payment = env[-1]
        payment2 = env[-2]

        env_gerproc = self.env['project_request'].search([], order="id asc")
        gerproc = env_gerproc[-1]

        payment.update({'gerproc_id': gerproc.id})
        payment2.update({'gerproc_id': gerproc.id})
        payment.update({'gerproc_parametro': True})
        payment2.update({'gerproc_parametro': True})
