# Copyright (c) 2022, Steven J Lightfoot and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class StockInventory(Document):

	# check this - should not change state if already set???
	def before_save(self):
		for line in self.stock_inventory_line:
			line.state = 'Draft'

	def before_submit(self):
		# update the quantities
		lookup_key: str
		for line in self.stock_inventory_line:
			# lookup key is the stock location and product
			lookup_key = f'{self.location}-{line.product}'
			# create a stock quantity record if it does not exist
			if not frappe.db.exists('Stock Quantity', lookup_key):
				doc = frappe.get_doc({
					'doctype': 'Stock Quantity',
					'location': self.location,
					'product': line.product,
					'quantity': line.qty
				})
				doc.insert()
			line.state = 'Submitted'
			stock_quantity_doc = frappe.get_doc('Stock Quantity', lookup_key)
			stock_quantity_doc.qty = line.qty
			stock_quantity_doc.save()

	def before_cancel(self):
		# update the quantities
		for line in self.stock_inventory_line:
			line.state = 'Cancelled'
			lookup_key = f'{self.location}-{line.product}'
			stock_quantity_doc = frappe.get_doc('Stock Quantity', lookup_key)
			stock_quantity_doc.qty = stock_quantity_doc.qty - line.qty
			stock_quantity_doc.save()
