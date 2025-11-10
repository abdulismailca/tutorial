/** @odoo-module **/
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component,useRef } from "@odoo/owl";

const actionRegistry = registry.category("actions");

class CrmDashboard extends Component {
    setup() {
        super.setup();
        this.orm = useService("orm");
        this.leadsByMonthTable = useRef("leads_by_month_table");
        console.log("leadsByMonthTable", this.leadsByMonthTable);
        this._fetch_data();

        this._render_chart();

//        this._lead_by_month();


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

   async _render_chart() {

    let activity_list = await this.orm.call("crm.lead", "get_activity_list", []);
    let lead_by_medium_list = await this.orm.call("crm.lead", "lead_by_medium", []);
    let lead_by_month_table =  await this.orm.call("crm.lead", "lead_by_month_table", []);
    let leads_lost_by_month =  await this.orm.call("crm.lead", "leads_lost_by_month", []);

    console.log("activity list", activity_list);
    console.log("lead_by_medium_list", lead_by_medium_list);


    //pie chart data set
    setTimeout(() => {
        const ctx = document.getElementById("chart_example");
        if (!ctx) return;
        new Chart(ctx, {
            type: "pie",
            data: {
                labels: ['Email', 'Call', 'To-Do'],
                datasets: [{
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.8)',
                        'rgba(54, 162, 235, 0.8)',
                        'rgba(75, 192, 192, 0.8)',
                    ],
                    data: activity_list,
                }]
            },
            options: {},
        });
    }, 300);


    //dougnet data set
    setTimeout(() => {
        const ctx = document.getElementById("doughnut_example");
        if (!ctx) return;
        new Chart(ctx, {
            type: "doughnut",
            data: {
                labels: ['Email', 'Call', 'To-Do'],
                datasets: [{
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.8)',
                        'rgba(54, 162, 235, 0.8)',
                        'rgba(75, 192, 192, 0.8)',
                    ],
                    data: lead_by_medium_list,
                }]
            },
            options: {},
        });
    }, 300);

}

   async _lead_by_month() {

    const tableBody = await this.leadsByMonthTable.el;
    console.log(" this.leadsByMonthTable.el", this.leadsByMonthTable.el)




    const [leads, months] = await this.orm.call('crm.lead', "lead_by_month_table", []);


    tableBody.innerHTML = '';


    for (let i = 0; i < months.length; i++) {
        const row = document.createElement('tr');
        const monthCell = document.createElement('td');
        const leadsCell = document.createElement('td');

        monthCell.textContent = months[i];
        leadsCell.textContent = leads[i];

        row.appendChild(monthCell);
        row.appendChild(leadsCell);
        tableBody.appendChild(row);
    }
}


}

CrmDashboard.template = "crm_dashboard.CrmDashboard";
actionRegistry.add("crm_dashboard_tag", CrmDashboard);
