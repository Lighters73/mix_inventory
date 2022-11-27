import frappe

# searches for stock location
@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def product_variant_query(doctype, txt, searchfield, start, page_len, filters):
    return frappe.db.sql("""
			select name, description, source
            from `tabProduct Variant`
            where (name like %(txt)s or product like %(txt)s or source like %(txt)s) and Status = 'Active'
            order by name;
     """, {"txt": "%%%s%%" % txt}
    )

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def location_query(doctype, txt, searchfield, start, page_len, filters):
    return frappe.db.sql("""
			select name, location
            from `tabStock Location`
            where (name like %(txt)s or location like %(txt)s) and type = 'storage'
            order by name;
     """, {"txt": "%%%s%%" % txt}
    )
