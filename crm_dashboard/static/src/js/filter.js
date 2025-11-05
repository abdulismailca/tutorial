/** @odoo-module **/
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component } from "@odoo/owl";
import { Dropdown } from "@web/core/dropdown/dropdown";
import { DropdownItem } from "@web/core/dropdown/dropdown_item";
class CustomFilter extends Component {
   setup() {
       this.action = useService("action");
   }
   // Open Sale Orders in a list view
   openSaleOrders() {
             this.action.doAction({
           type: "ir.actions.act_window",
           name: "Sale Orders",
           res_model: "sale.order",
           views: [[false, "list"], [false, "form"]],
           target: "current",
       });
   }
   // Open Purchase Orders in a list view
   openPurchaseOrders() {
              this.action.doAction({
           type: "ir.actions.act_window",
           name: "Purchase Orders",
           res_model: "purchase.order",
           views: [[false, "list"], [false, "form"]],
           target: "current",
       });
   }
}
CustomFilter.template = "custom_filter";
SystrayDropdown.components = { Dropdown, DropdownItem };
export const systrayItem = {
   Component: SystrayDropdown,
};
registry.category("systray").add("SystrayDropdown", systrayItem, { sequence: 1 });
