# Copyright (c) 2022, Steven J Lightfoot and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class StockCustomerShipment(Document):

	def before_save(self):
		for move in self.stock_move:
			move.state = 'Draft'

	def before_submit(self):
		# update the quantities
		lookup_key: str
		for move in self.stock_move:
			move.state = 'Submitted'
			lookup_key = f'{move.destination_location}-{move.product}'
			stock_quantity_doc = frappe.get_doc('Stock Quantity', lookup_key)
			stock_quantity_doc.qty = stock_quantity_doc.qty + move.qty
			stock_quantity_doc.save()

	def before_cancel(self):
		# update the quantities
		for move in self.stock_move:
			move.state = 'Cancelled'
			lookup_key = f'{move.destination_location}-{move.product}'
			stock_quantity_doc = frappe.get_doc('Stock Quantity', lookup_key)
			stock_quantity_doc.qty = stock_quantity_doc.qty - move.qty
			stock_quantity_doc.save()
