/** @odoo-module **/
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component } from  "@odoo/owl";
const actionRegistry = registry.category("actions");
class CrmDashboard extends Component {
  setup() {
        super.setup();
        this.orm = useService('orm');
        this._fetch_data();
  }
  async _fetch_data(){
     let result = await this.orm.call("crm.lead", "get_tiles_data", [], {});
     document.getElementById('my_lead').innerHTML = `<span>${result.total_leads}</span>`;
     document.getElementById('my_opportunity').innerHTML = `<span>${result.total_opportunity}</span>`;
     document.getElementById('future_revenue').innerHTML = `<span>${result.currency}${result.expected_revenue}</span>`;
     document.getElementById('user_invoiced_revenue').innerHTML = `<span>${result.currency}${result.user_all_invoices_amount}</span>`;
     document.getElementById('my_lose').innerHTML = `<span>${result.currency}${result.my_lose}</span>`;


  }
}
CrmDashboard.template = "crm_dashboard.CrmDashboard";
actionRegistry.add("crm_dashboard_tag", CrmDashboard);
