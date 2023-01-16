{
    'name': 'Inherit Payment',
    'version': '1.1',
    'author': 'Thiago Francelino',
    'summary': '',
    'sequence': '1',
    'description': 'inherit payment',
    'category': 'pagamento',
    'depends': ['account', 'project_requests', 'cadastro_cheque'],
    'data': [
        "security/ir.model.access.csv",
        "wizard/pagamento_direto_wizard_view.xml",
        # "views/inherit_project_request_view.xml",
        "views/Inherit_payment_view.xml",
    ],
}
