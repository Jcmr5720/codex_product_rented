{
    'name': 'product_rented',
    'summary': 'Modulo encargado de rentar productos.',
    'version': '1.2.0',
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
        'security/ir.model.access.csv',
        'data/rented_time_option_data.xml',
        'views/product_template_views.xml',
        'views/template_product_rented.xml',
    ],
    'post_init_hook': 'post_init_hook',
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
