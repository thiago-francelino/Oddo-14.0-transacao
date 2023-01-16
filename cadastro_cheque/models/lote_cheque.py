from odoo import models, fields, api
from datetime import date


class LoteCheque(models.Model):
    _name = 'lote.cheque'
    codigo_do_lote = fields.Char(string="Codigo deste lote")
    responsavel_pelo_lote = fields.Char(string="Responsável pelo lote")
    cpf_responsavel_pelo_lote = fields.Char(string="CPF do responsável pelo lote")
    telefone_responsavel_pelo_lote = fields.Char(string="Telefone do responsável pelo lote")
    data = fields.Date(string="Data de criação do lote", readonly=True, default=date.today())
    tipo_de_pagamento = fields.Selection([
        ('?', '?'),
        ('??', '??'),
        ('???', '???'),
    ], string="Tipo de pagamento")
    currency_id = fields.Many2one("res.currency")
    cheque_id = fields.Many2many('cadastro.cheque',  string="Cheques correspondentes a esse lote",
                                 domain="[('pagamentos_feitos_com_cheque','=',False)]")
    valor_total_do_lote = fields.Monetary(currency_field='currency_id', compute="calcular_valor_total_lote",
                                          string="Valor Total do lote")
    payment_id = fields.One2many("account.payment", "lote_id", string="Pagamentos feitos com esse lote")


    @api.depends('cheque_id')
    def calcular_valor_total_lote(self):
        valor = 0
        for lote in self:
            for cheque in lote.cheque_id:
                valor += cheque.valor
            lote.valor_total_do_lote = valor
