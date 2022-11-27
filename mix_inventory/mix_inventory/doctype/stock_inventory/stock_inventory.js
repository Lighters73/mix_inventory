// Copyright (c) 2022, Steven J Lightfoot and contributors
// For license information, please see license.txt

frappe.ui.form.on('Stock Inventory', {
    setup: function(frm) {
        frm.set_query('location', function() {
            return {
                query: "mix_inventory.controllers.queries.location_query"
            }
        })
    },
	onload: function(frm) {
        frm.set_value('added_by', frappe.session.user)
	}
});