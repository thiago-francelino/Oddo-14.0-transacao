{
    'name': 'cadastro cheque',
    'version': '1.1',
    'author': 'Thiago Francelino',
    'summary': '',
    'sequence': '1',
    'description': 'cadastro cheque',
    'category': 'pagamento',
    # 'depends': ['account'],
    'depends': ['base', 'account'],
    'data': [
        "security/ir.model.access.csv",
        "views/cadastro_cheque_view.xml",
        "views/Inherit_payment_view.xml",
        "data/bank_cheque.xml",
        "views/lote_cheque_view.xml",
    ],
}
