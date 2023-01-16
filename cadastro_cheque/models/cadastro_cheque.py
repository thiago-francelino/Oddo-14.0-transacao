from odoo import models, fields, api
from datetime import date

class CadastroCheque(models.Model):
    #____----==== baixe datetime ====----____

    _name = 'cadastro.cheque'


    barcode = fields.Char(string='Codigo de barras')
    Agency_cheque = fields.Char(string='Agencia')
    number_cheque = fields.Char(string='Numero do cheque')
    account_cheque = fields.Char(string='Conta do cheque')
    cheque_amount_text = fields.Char(string='Valor por extenso')
    bank_cheque = fields.Many2one('bank_cheque')


    currency_id = fields.Many2one('res.currency', default=6, invisible=True)
    valor = fields.Monetary(currency_field="currency_id", string="Valor da transação")
    data_deposito = fields.Date(string="Data de deposito")
    type_cheque = fields.Selection(
        [
            ('5', 'Comum'),
            ('6', 'Bancário'),
            ('7', 'Salário'),
            ('8', 'Administrativo'),
            ('9', 'CPMF')
        ])


    terceiro = fields.Boolean(string="É cheque de terceiro?")
    nome_terceiro = fields.Char(string="Nome do terceiro")
    cpf_terceiro = fields.Char(string="CPF do terceiro")
    telefone_terceiro = fields.Char(string="Telefone do terceiro")
    codigo_boleto = fields.Char(string="Codigo do boleto")
    descricao = fields.Html(string="Descrição")


    movimentos = fields.One2many('account.payment', 'cheque_id', string="Movimentos relacionados ao cadastro do cheque")
    pagamentos_feitos_com_cheque = fields.One2many(comodel_name='account.payment', inverse_name='pagamento_com_cheque_id', string="Pagamento feito com esse cheque")
    lote_cheque_id = fields.Many2many('lote.cheque', string="Pertence ao lote")
    pagamento_devolucao_id = fields.One2many('account.payment', 'cheque_devolucao_id', string="Pagamento relacionado a devolução")
    devolucao_related= fields.Boolean(related="pagamentos_feitos_com_cheque.devolucao", string="Este cheque foi devolvido")
    pago_pelo_lote_related = fields.Boolean(related="pagamentos_feitos_com_cheque.pago_pelo_lote", string="Cheque pago pelo lote")




    @api.model
    def create(self, vals_list):
        rtn = super(CadastroCheque, self).create(vals_list)


        lista1 = {
            'payment_type': 'inbound',
            'partner_type': 'customer',
            'auto_post': True,
            'partner_id': 1,
            'destination_account_id': 559,
            'is_internal_transfer': True,
            'journal_id': 8,
            'payment_method_id': 1,
            'payment_token_id': False,
            'partner_bank_id': 1,
            'amount': vals_list['valor'],
            'currency_id': 6,
            'check_amount_in_words': 'Zero Real',
            'date': date.today(),
            'effective_date': False,
            'bank_reference': False,
            'cheque_reference': False,
            'ref': False,
            'edi_document_ids': [],
            'message_follower_ids': [],
            'activity_ids': [],
            'message_ids': [],
            'cheque_id': rtn.id,
        }
        # vai entar no cheques em carteira
        lista2 = {
            'payment_type': 'outbound',
            'auto_post': True,
            'partner_type': 'customer',
            'partner_id': 1,  # mycompany id
            'destination_account_id': 559,
            'is_internal_transfer': True,
            'journal_id': 7,
            'payment_method_id': 1,
            'payment_token_id': False,
            'partner_bank_id': 2,
            'amount': vals_list['valor'],
            'currency_id': 6,
            'check_amount_in_words': 'Zero Real',
            'date': date.today(),
            'effective_date': False,
            'bank_reference': False,
            'cheque_reference': False,
            'ref': False,
            'edi_document_ids': [],
            'message_follower_ids': [],
            'activity_ids': [],
            'message_ids': [],
            'cheque_id': rtn.id,
        }

        pagamento1 = self.env['account.payment'].create(lista1)
        pagamento2 = self.env['account.payment'].create(lista2)
        pagamento2.action_post()
        pagamento1.action_post()

        return rtn


    bank_cheque = fields.Many2one(
        "bank_cheque",
        required=True,
        tracking=True
    )

    # preenche os campos
    @api.onchange("barcode")
    def on_change_barcode(self):
        for rec in self:
            if rec.barcode and len(rec.barcode) == 34:
                rec.bank_cheque = rec.env['bank_cheque'].sudo().search([('cod', 'in', [rec.barcode[1:4]])])

                rec.Agency_cheque = rec.barcode[4:8]
                rec.number_cheque = rec.barcode[13:19]
                rec.account_cheque = rec.barcode[25:32]
            else:
                rec.barcode = ""


    @api.onchange("valor")
    def on_change_value_code(self):
        currency_id = self.env['res.currency'].browse(self.env.company.currency_id.id)

        for rec in self:
            text_amount = currency_id.amount_to_text(self.valor)
            if text_amount.__eq__("Um Real"):
                rec.cheque_amount_text = text_amount
            else:
                rec.cheque_amount_text = text_amount.replace("Real", "Reais")
