{
    'name': 'product_rented',
    'summary': 'Modulo encargado de rentar productos.',
    'version': '1.0',
    'author': 'Juan Camilo Muñoz',
    'category': 'Tools',
    'depends': [
        'loyalty',
        'website',
        'web',
        'web_editor',
        'portal',
        'sale',
        'website_sale',
        'mail',
        'product',
    ],
    'data': [
        'views/product_template_views.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            ('include', 'web._assets_bootstrap'),

        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'GPL-3'
}
