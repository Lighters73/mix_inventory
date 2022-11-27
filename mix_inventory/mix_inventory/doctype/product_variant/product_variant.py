# Copyright (c) 2022, Steven J Lightfoot and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

class ProductVariant(Document):
    def before_save(self):
        # set the title if not set already
        if self.title is None:
            title = f"{str(self.name)}-{self.description} ({self.source})"
            self.title = title