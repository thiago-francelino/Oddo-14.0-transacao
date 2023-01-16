from odoo import models, fields, api


class PagamentoDireto(models.TransientModel):
    _name = "pagamento.direto.wizard"

    conta_destino = fields.Many2one("account.account", string='Conta destino', default=25)
    conta_bancaria_destinataria = fields.Many2one("res.partner.bank", string='Conta bancaria destinataria')
    conta_bancaria_origem = fields.Many2one("res.partner.bank", string='Conta bancaria origem')
    currency_id = fields.Many2one('res.currency', default=6, invisible=True)
    valor = fields.Monetary(currency_field="currency_id", string="Valor da transação")
    journal1 = fields.Many2one("account.journal", string='Diario  origem')
    journal2 = fields.Many2one("account.journal", string='Diario destino')
    cliente_cadastrado = fields.Many2one("res.partner", string='Cliente')
    data = fields.Date(String="data")

    devolver_cheque = fields.Boolean(string="Devolução de cheque?")
    pagamento_com_cheque = fields.Boolean(string="Pagamento através de um cheque?")
    pagamento_com_lote = fields.Boolean(string="Pagamento com lote?")

    # cheque_id = fields.Many2one("cadastro.cheque", string="Cheques",
    #                             domain="[('pagamentos_feitos_com_cheque', '=', True), ('pagamento_devolucao_id','=', True)]"
    #                             )
    cheque_id = fields.Many2one("cadastro.cheque", string="Cheques",
                                domain="[('pagamentos_feitos_com_cheque', '=', False)]"
                                )
    valor_cheque = fields.Monetary(related="cheque_id.valor", string="Valor do cheque selecionado")

    lote_id = fields.Many2one('lote.cheque', string="Lote",
                              domain="[('payment_id', '=', False)]")
    valor_lote = fields.Monetary(related="lote_id.valor_total_do_lote", string="Valor total do lote")

    def salvar(self):
        if self.pagamento_com_cheque == True:
            lista1 = {
                'payment_type': 'outbound',
                'partner_type': 'customer',
                'auto_post': True,
                'partner_id': self.cliente_cadastrado.id,
                'destination_account_id': self.conta_destino.id,
                'is_internal_transfer': False,  # alterado
                'journal_id': 8,
                'payment_method_id': 1,
                'payment_token_id': False,
                'partner_bank_id': 1,
                # 'amount': vals_list['valor'],
                'amount': self.cheque_id.valor,
                'currency_id': 6,
                'check_amount_in_words': 'Zero Real',
                'date': self.data,
                'effective_date': False,
                'bank_reference': False,
                'cheque_reference': False,
                'ref': False,
                'edi_document_ids': [],
                'message_follower_ids': [],
                'activity_ids': [],
                'message_ids': [],
                'check_amount_in_words': 'Dez Real',
                'pagamento_com_cheque_id': self.cheque_id.id,
            }
            pagamento1 = self.env['account.payment'].create(lista1)
            pagamento1.action_post()
            lista2 = {
                'payment_type': 'inbound',
                # 'payment_type': 'outbound',
                'auto_post': True,
                'partner_type': 'customer',
                'partner_id': self.cliente_cadastrado.id,
                'destination_account_id': self.conta_destino.id,
                'is_internal_transfer': False,  # alterei
                'journal_id': self.journal2.id,
                'payment_method_id': 1,
                'payment_token_id': False,
                'partner_bank_id': self.conta_bancaria_destinataria.id,
                'amount': self.cheque_id.valor,
                'currency_id': 6,
                'check_amount_in_words': 'Zero Real',
                'date': self.data,
                'effective_date': False,
                'bank_reference': False,
                'cheque_reference': False,
                'ref': False,
                'edi_document_ids': [],
                'message_follower_ids': [],
                'activity_ids': [],
                'message_ids': [],
                'check_amount_in_words': 'Dez Real',
                'pagamento_com_cheque_id': self.cheque_id.id,
            }
            pagamento2 = self.env['account.payment'].create(lista2)
            pagamento2.action_post()

        elif self.pagamento_com_lote == True:

            # for lote in self:
            for cheque in self.lote_id.cheque_id:
                lista1 = {
                    'payment_type': 'outbound',
                    'partner_type': 'customer',
                    'auto_post': True,
                    'partner_id': self.cliente_cadastrado.id,
                    'destination_account_id': self.conta_destino.id,
                    'is_internal_transfer': False,  # alterado
                    'journal_id': 8,
                    'payment_method_id': 1,
                    'payment_token_id': False,
                    'partner_bank_id': 1,
                    # 'amount': vals_list['valor'],
                    'amount': cheque.valor,
                    'currency_id': 6,
                    'check_amount_in_words': 'Zero Real',
                    'date': self.data,
                    'effective_date': False,
                    'bank_reference': False,
                    'cheque_reference': False,
                    'ref': False,
                    'edi_document_ids': [],
                    'message_follower_ids': [],
                    'activity_ids': [],
                    'message_ids': [],
                    'check_amount_in_words': 'Dez Real',
                    # 'pagamento_com_cheque_id': lote.lote_id.cheque_id.id,
                    'pagamento_com_cheque_id': cheque.id,
                    'lote_id': self.lote_id.id,
                    'pago_pelo_lote': True,
                }
                pagamento1 = self.env['account.payment'].create(lista1)
                pagamento1.action_post()

                lista2 = {
                    'payment_type': 'inbound',
                    'auto_post': True,
                    'partner_type': 'customer',
                    'partner_id': self.cliente_cadastrado.id,
                    'destination_account_id': self.conta_destino.id,
                    'is_internal_transfer': False,  # alterei
                    'journal_id': self.journal2.id,
                    'payment_method_id': 1,
                    'payment_token_id': False,
                    'partner_bank_id': self.conta_bancaria_destinataria.id,
                    'amount': cheque.valor,
                    'currency_id': 6,
                    'check_amount_in_words': 'Zero Real',
                    'date': self.data,
                    'effective_date': False,
                    'bank_reference': False,
                    'cheque_reference': False,
                    'ref': False,
                    'edi_document_ids': [],
                    'message_follower_ids': [],
                    'activity_ids': [],
                    'message_ids': [],
                    'check_amount_in_words': 'Dez Real',
                    'pagamento_com_cheque_id': cheque.id,
                    'lote_id': self.lote_id.id,
                    'pago_pelo_lote': True,
                }
                pagamento2 = self.env['account.payment'].create(lista2)
                pagamento2.action_post()
        # ainda em desenvolvimento DEVOLVER CHEQUE
        elif self.devolver_cheque == True:
            lista1 = {
                'payment_type': 'outbound',
                # 'payment_type': 'inbound',
                'partner_type': 'customer',
                'auto_post': True,
                'partner_id': self.cliente_cadastrado.id,
                'destination_account_id': self.conta_destino.id,
                'is_internal_transfer': False,  # alterado
                'journal_id': 8,
                'payment_method_id': 1,
                'payment_token_id': False,
                'partner_bank_id': 1,
                # 'amount': vals_list['valor'],
                'amount': self.cheque_id.valor,
                'currency_id': 6,
                'check_amount_in_words': 'Zero Real',
                'date': self.data,
                'effective_date': False,
                'bank_reference': False,
                'cheque_reference': False,
                'ref': False,
                'edi_document_ids': [],
                'message_follower_ids': [],
                'activity_ids': [],
                'message_ids': [],
                'devolucao': True,
                'check_amount_in_words': 'Dez Real',
                'pagamento_com_cheque_id': self.cheque_id.id,
                # 'pagamento_com_cheque_id': lote.lote_id.cheque_id.id,
                # 'pagamento_com_cheque_id': cheque.id,
                # 'lote_id': self.lote_id.id,
                # 'cheque_devolucao_id': self.cheque_id.id,
            }
            pagamento1 = self.env['account.payment'].create(lista1)
            pagamento1.action_post()

            lista2 = {
                'payment_type': 'inbound',
                # 'payment_type': 'outbound',
                'auto_post': True,
                'partner_type': 'customer',
                'partner_id': self.cliente_cadastrado.id,
                'destination_account_id': self.conta_destino.id,
                'is_internal_transfer': False,  # alterei
                'journal_id': 12,
                'payment_method_id': 1,
                'payment_token_id': False,
                'partner_bank_id': 4,
                'amount': self.cheque_id.valor,
                'currency_id': 6,
                'check_amount_in_words': 'Zero Real',
                'date': self.data,
                'effective_date': False,
                'bank_reference': False,
                'cheque_reference': False,
                'ref': False,
                'edi_document_ids': [],
                'message_follower_ids': [],
                'activity_ids': [],
                'message_ids': [],
                'check_amount_in_words': 'Dez Real',
                'devolucao': True,
                'pagamento_com_cheque_id': self.cheque_id.id,
                # 'pagamento_com_cheque_id': cheque.id,
                # 'lote_id': self.lote_id.id,
                # 'cheque_devolucao_id': self.cheque_id.id,

            }
            pagamento2 = self.env['account.payment'].create(lista2)
            pagamento2.action_post()
        else:
            lista1 = {
                'payment_type': 'outbound',
                'partner_type': 'customer',
                'auto_post': True,
                'partner_id': self.cliente_cadastrado.id,
                'destination_account_id': self.conta_destino.id,
                'is_internal_transfer': False,  # alterado
                'journal_id': self.journal1.id,
                'payment_method_id': 1,
                'payment_token_id': False,
                'partner_bank_id': self.conta_bancaria_origem.id,
                'amount': self.valor,
                'currency_id': 6,
                'check_amount_in_words': 'Zero Real',
                'date': self.data,
                'effective_date': False,
                'bank_reference': False,
                'cheque_reference': False,
                'ref': False,
                'edi_document_ids': [],
                'message_follower_ids': [],
                'activity_ids': [],
                'message_ids': [],
                'check_amount_in_words': 'Dez Real',
            }

            lista2 = {
                'payment_type': 'inbound',
                'auto_post': True,
                'partner_type': 'customer',
                'partner_id': self.cliente_cadastrado.id,
                'destination_account_id': self.conta_destino.id,
                'is_internal_transfer': False,  # alterei
                'journal_id': self.journal2.id,
                'payment_method_id': 1,
                'payment_token_id': False,
                'partner_bank_id': self.conta_bancaria_destinataria.id,
                'amount': self.valor,
                'currency_id': 6,
                'check_amount_in_words': 'Zero Real',
                'date': self.data,
                'effective_date': False,
                'bank_reference': False,
                'cheque_reference': False,
                'ref': False,
                'edi_document_ids': [],
                'message_follower_ids': [],
                'activity_ids': [],
                'message_ids': [],
                'check_amount_in_words': 'Dez Real',
            }
            descricao = 'Valor do pagamento: R$' + str(self.valor) + ' Data: ' + str(self.data)

            pagamento1 = self.env['account.payment'].create(lista1)
            pagamento1.action_post()

            pagamento2 = self.env['account.payment'].create(lista2)
            pagamento2.action_post()

            id_gerproc = self.env['project_request'].search([], order="id asc")

            vals_list3 = {'status': 'aberto',
                          'private_message': 'public',
                          'department_id': 1,  # required
                          'user_requested_id': False,
                          'users_views_ids': [[6, False, []]],
                          # 'department_views_ids': [[6, False, [1, 2]]],
                          'department_views_ids': [[6, False, [1]]],
                          'category_parent_request_id': 1,  # required
                          'category_child_request': 2,  # required
                          'boolean_client': False,
                          'request_client_ids': [[6, False, []]],
                          'description_problem': descricao,  # required
                          'my_requests': [[6, False, []]],
                          'message_follower_ids': [],
                          'activity_ids': [],
                          'message_ids': [],
                          'pagamentos': [pagamento1.id, pagamento2.id],
                          # 'pagamentos': [pagamento1.id],

                          }
            self.env['project_request'].create(vals_list3)

            self.env['account.payment'].atualizar()
        # vals_lista da função q o marcelo pediu
        # [{'name': '/',
        #   'payment_type': 'outbound',
        #   'partner_type': 'customer',
        #   'is_internal_transfer': True,
        #   'journal_id': 7,
        #   'payment_method_id': 2,
        #   'payment_token_id': False,
        #   'partner_bank_id': 4,
        #   'gerproc_id': False,
        #   'amount': 10,
        #   'currency_id': 6,
        #   'check_amount_in_words': 'Dez Real',
        #   'date': '2023-01-06',
        #   'effective_date': False,
        #   'bank_reference': False,
        #   'cheque_reference': False,
        #   'ref': False,
        #   'edi_document_ids': [],
        #   'message_follower_ids': [],
        #   'activity_ids': [],
        #   'message_ids': []}]

        # vals_list gustavo
        # receive_vals = {
        #     'payment_type': 'inbound',
        #     'partner_type': 'customer',
        #     'partner_id': self.partner_id_destino.id,
        #     'is_internal_transfer': False,
        #     'journal_id': self.journal_id.id,
        #     'payment_method_id': 1,
        #     'payment_token_id': False,
        #     'partner_bank_id': self.banco_destinatario.id,
        #     'auto_post': True,
        #     'amount': self.valor,
        #     'currency_id': self.currency_id.id,
        #     'check_amount_in_words': 'Zero Real',
        #     'date': self.data_envio,
        #     'effective_date': False,
        #     'bank_reference': False,
        #     'cheque_reference': False,
        #     'ref': False,
        #     'edi_document_ids': [],
        #     'message_follower_ids': [],
        #     'activity_ids': [],
        #     'message_ids': []
        # }

        # PADRÃO DE ANTES
        # descricao = 'Valor do pagamento: R$' + str(self.valor) + ' Data: ' + str(self.data)
        #
        # pagamento1 = self.env['account.payment'].create(lista1)
        # pagamento1.action_post()
        #
        # pagamento2 = self.env['account.payment'].create(lista2)
        # pagamento2.action_post()
        #
        # id_gerproc = self.env['project_request'].search([], order="id asc")
        #
        # vals_list3 = {'status': 'aberto',
        #               'private_message': 'public',
        #               'department_id': 1,  # required
        #               'user_requested_id': False,
        #               'users_views_ids': [[6, False, []]],
        #               # 'department_views_ids': [[6, False, [1, 2]]],
        #               'department_views_ids': [[6, False, [1]]],
        #               'category_parent_request_id': 1,  # required
        #               'category_child_request': 2,  # required
        #               'boolean_client': False,
        #               'request_client_ids': [[6, False, []]],
        #               'description_problem': descricao,  # required
        #               'my_requests': [[6, False, []]],
        #               'message_follower_ids': [],
        #               'activity_ids': [],
        #               'message_ids': [],
        #               'pagamentos': [pagamento1.id, pagamento2.id],
        #               # 'pagamentos': [pagamento1.id],
        #
        #               }
        # self.env['project_request'].create(vals_list3)
        #
        # self.env['account.payment'].atualizar()

        return
