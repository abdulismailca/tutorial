/** @odoo-module **/
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component } from "@odoo/owl";

const actionRegistry = registry.category("actions");

class CrmDashboard extends Component {
    setup() {
        super.setup();
        this.orm = useService("orm");
        this._fetch_data();
        this._render_chart();
    }

    async _fetch_data() {
        let result = await this.orm.call("crm.lead", "get_tiles_data", [], {});


        document.getElementById("my_lead").innerHTML = `<span>${result.total_leads}</span>`;
        document.getElementById("my_opportunity").innerHTML = `<span>${result.total_opportunity}</span>`;
        document.getElementById("future_revenue").innerHTML = `<span>${result.currency}${result.expected_revenue}</span>`;
        document.getElementById("user_invoiced_revenue").innerHTML = `<span>${result.currency}${result.user_all_invoices_amount}</span>`;
        document.getElementById("my_lose_count").innerHTML = `<span>${result.currency}${result.my_lose}</span>`;
        document.getElementById("won_los_ration").innerHTML = `<span>${result.won_los_ration}</span>`;


    }


    _render_chart() {

        let activity_list = this.orm.call("crm.lead", "get_activity_list",[]);
        let lead_by_medium_list = this.orm.call("crm.lead", "lead_by_medium",[]);



        console.log("activity list",activity_list);

        //pie chart

        setTimeout(() => {
            const ctx = document.getElementById("chart_example");
            if (!ctx) return;
            new Chart(ctx, {
                type: "pie",
                data: {
                 labels: ['Email', 'Call ', 'TO Do'],
                    datasets: [{
                 backgroundColor: [
                  'rgba(255, 99, 132, 0.8)',
                  'rgba(54, 162, 235, 0.8)',
                  'rgba(75, 192, 192, 0.8)',
                  'rgba(255, 206, 86, 0.8)'
                 ],
                data:[1,2,3]
             }]
                },
                options: {},
            });
        },300);
    }
}

CrmDashboard.template = "crm_dashboard.CrmDashboard";
actionRegistry.add("crm_dashboard_tag", CrmDashboard);
