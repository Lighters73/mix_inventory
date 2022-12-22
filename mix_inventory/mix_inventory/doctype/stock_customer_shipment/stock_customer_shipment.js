// Copyright (c) 2022, Steven J Lightfoot and contributors
// For license information, please see license.txt

frappe.ui.form.on('Stock Customer Shipment', {
    setup: function(frm) {
		// add a filter
		frm.set_query('source_location', 'stock_move', function(doc, cdt, cdn) {
			return {
				filters: {
					'type': 'storage'
				}
			}
		})
    },
	onload: function(frm) {
        frm.set_value('raised_by', frappe.session.user)
	}
});

frappe.ui.form.on('Stock Move', {
	stock_move_add(frm, cdt, cdn) {
		// set default value for destination
		frappe.model.set_value(cdt, cdn, 'destination_location', 'LOC_CUS')
		// set the default source_location to be the source location of the previous item
		if (frm.doc.stock_move.length > 1) {
			let last_source_location = frm.doc.stock_move[frm.doc.stock_move.length - 2].source_location
			frappe.model.set_value(cdt, cdn, 'source_location', last_source_location)
		}
	}
});

