from __future__ import unicode_literals

from frappe import _

def get_data():
    return {
            "fieldname": "Product",
            'transactions': [
                {
                    "label": _("Variants"),
                    'items': ['Product Variant']
                },
            ]
        }