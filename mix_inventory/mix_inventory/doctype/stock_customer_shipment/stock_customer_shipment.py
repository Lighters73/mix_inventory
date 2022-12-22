# Copyright (c) 2022, Steven J Lightfoot and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class StockCustomerShipment(Document):
    output_zone = 'LOC_OUT'

    def before_save(self):
        output_key: str
        source_key: str
        for move in self.stock_move:
            # move the stock to the output zone
            source_key = f'{move.source_location}-{move.product}'
            output_key = f'{self.output_zone}-{move.product}'
            # validate source item
            self.validate_item(source_key)
            # create a destination record if it does not exist
            if not frappe.db.exists('Stock Quantity', output_key):
                doc = frappe.get_doc({
                    'doctype': 'Stock Quantity',
                    'location': self.output_zone,
                    'product': move.product,
                    'quantity': move.qty
                })
                doc.insert()
            move.state = 'Draft'
            # update the quantities - decrease from source location, increase output_zone
            sq_source_doc = frappe.get_doc('Stock Quantity', source_key)
            sq_source_doc.qty = sq_source_doc.qty - move.qty
            sq_output_doc = frappe.get_doc('Stock Quantity', output_key)
            sq_output_doc.qty = sq_output_doc.qty + move.qty
            sq_source_doc.save()
            sq_output_doc.save()

    def before_submit(self):
        # update the quantities
        output_key: str
        destination_key: str
        for move in self.stock_move:
            output_key = f'{self.output_zone}-{move.product}'
            destination_key = f'{move.destination_location}-{move.product}'
            # validate output item
            self.validate_item(output_key)
            # create a stock quantity record if it does not exist
            if not frappe.db.exists('Stock Quantity', destination_key):
                doc = frappe.get_doc({
                    'doctype': 'Stock Quantity',
                    'location': move.destination_location,
                    'product': move.product,
                    'quantity': move.qty
                })
                doc.insert()
            move.state = 'Submitted'
            # update the quantities - decrease from output zone, increase destination location
            sq_output_doc = frappe.get_doc('Stock Quantity', output_key)
            sq_output_doc.qty = sq_output_doc.qty - move.qty
            sq_destination_doc = frappe.get_doc('Stock Quantity', destination_key)
            sq_destination_doc.qty = sq_destination_doc.qty + move.qty
            sq_output_doc.save()
            sq_destination_doc.save()

    def validate_item(self, lookup_key):
		# from the lookup key - extract the product and location
        keys = str(lookup_key).split('-')
		# check the item exists at the location - you can't move stock from a location that does not exist
        if not frappe.db.exists('Stock Quantity', lookup_key):
            frappe.throw(_("Can't proceed, check you have this item at this location\n"
                           "Product: {0} Location: {1}\n".format(keys[1], keys[0])))

    def before_cancel(self):
        # check what the state of the document is
        for move in self.stock_move:
            if move.state == 'Draft':  # reverse move to output zone
                lookup_key = f'{self.output_zone}-{move.product}'
            else:  # reverse move to destination
                lookup_key = f'{move.destination_location}-{move.product}'
            move.state = 'Cancelled'
            stock_quantity_doc = frappe.get_doc('Stock Quantity', lookup_key)
            stock_quantity_doc.qty = stock_quantity_doc.qty - move.qty
            stock_quantity_doc.save()
