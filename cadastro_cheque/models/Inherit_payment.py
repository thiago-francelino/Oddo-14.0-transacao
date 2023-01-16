from odoo import models, fields, api

class InheritPayment(models.Model):
    _inherit = 'account.payment'
    effective_date = fields.Char()
    bank_reference = fields.Char()
    cheque_reference = fields.Char()
    cheque_id = fields.Many2one("cadastro.cheque", string='Deposito do cheque')
    pagamento_com_cheque_id = fields.Many2one('cadastro.cheque', string="Pagamento com o cheque")
    lote_id = fields.Many2one("lote.cheque", string="Lote que efetuou este pagamento")
    cheque_devolucao_id = fields.Many2one("lote.cheque", string="Pagamento de devolução do cheque")
    devolucao = fields.Boolean(string="Este cheque foi devolvido!")
    pago_pelo_lote = fields.Boolean(string="Cheque pago através de um lote")
