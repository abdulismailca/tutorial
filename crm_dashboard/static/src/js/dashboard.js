/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";
const actionRegistry = registry.category("actions");
class CrmDashboard extends Component {}
CrmDashboard.template = "my_module.CrmDashboard";
// Register the component with the action tag
actionRegistry.add("crm_dashboard_tag", CrmDashboard);

