# Copyright (c) 2022, Steven J Lightfoot and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class StockCustomerShipment(Document):

    def before_save(self):
        # update the items to draft
        for move in self.stock_move:
            move.state = 'Draft'

    def before_submit(self):
        # update the quantities
        source_key: str
        destination_key: str
        for move in self.stock_move:
            source_key = f'{move.source_location}-{move.product}'
            destination_key = f'{move.destination_location}-{move.product}'
            # validate item from source_location
            self.validate_item(source_key)
            # create a stock quantity record for the destination item if it does not exist
            if not frappe.db.exists('Stock Quantity', destination_key):
                doc = frappe.get_doc({
                    'doctype': 'Stock Quantity',
                    'location': move.destination_location,
                    'product': move.product,
                    'quantity': move.qty
                })
                doc.insert()
            move.state = 'Submitted'
            # update the quantities - decrease from source location, increase destination location
            sq_source_doc = frappe.get_doc('Stock Quantity', source_key)
            sq_source_doc.qty = sq_source_doc.qty - move.qty
            sq_destination_doc = frappe.get_doc('Stock Quantity', destination_key)
            sq_destination_doc.qty = sq_destination_doc.qty + move.qty
            sq_source_doc.save()
            sq_destination_doc.save()

    def validate_item(self, lookup_key):
        # from the lookup key - extract the product and location
        keys = str(lookup_key).split('-')
        # check the item exists at the location - you can't move stock from a location that does not exist
        if not frappe.db.exists('Stock Quantity', lookup_key):
            frappe.throw(_("Can't proceed, check you have this item at this location\n"
                           "Product: {0} Location: {1}\n".format(keys[1], keys[0])))

    def before_cancel(self):
        # reverse the stock move quantities
        for move in self.stock_move:
            source_key = f'{move.source_location}-{move.product}'
            destination_key = f'{move.destination_location}-{move.product}'
            move.state = 'Cancelled'
            # update the quantities - decrease from destination location, increase source location
            sq_destination_doc = frappe.get_doc('Stock Quantity', destination_key)
            sq_destination_doc.qty = sq_destination_doc.qty - move.qty
            sq_source_doc = frappe.get_doc('Stock Quantity', source_key)
            sq_source_doc.qty = sq_source_doc.qty + move.qty
            sq_destination_doc.save()
            sq_source_doc.save()
