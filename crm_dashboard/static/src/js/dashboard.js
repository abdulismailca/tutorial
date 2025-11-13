/** @odoo-module **/
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, useRef, onMounted } from "@odoo/owl";

const actionRegistry = registry.category("actions");

class CrmDashboard extends Component {
    setup() {
        this.orm = useService("orm");
        this.leadsByMonthTable = useRef("leads_by_month_table");

        onMounted(async () => {
            await this._loadDashboard();
            this._initFilterListener();
        });
    }

    async _loadDashboard(period = "monthly") {
        await this._fetch_data();
        await this._render_chart(period);
        await this._lead_by_month(period);
    }

    _initFilterListener() {
        const filter = document.getElementById("period_filter");
        filter.addEventListener("change", async (e) => {
            const value = e.target.value;
            await this._loadDashboard(value);
        });
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

    async _render_chart(period) {
        let activity_list = await this.orm.call("crm.lead", "get_activity_list", []);
        let lead_by_medium_list = await this.orm.call("crm.lead", "lead_by_medium", []);
        let lead_by_month_table = await this.orm.call("crm.lead", "lead_by_month_table", [period]);

        const ctx1 = document.getElementById("chart_example");
        if (ctx1) {
            new Chart(ctx1, {
                type: "pie",
                data: {
                    labels: ['Email', 'Call', 'To-Do'],
                    datasets: [{
                        backgroundColor: ['#ff6384', '#36a2eb', '#4bc0c0'],
                        data: activity_list,
                    }],
                },
            });
        }

        const ctx2 = document.getElementById("doughnut_example");
        if (ctx2) {
            new Chart(ctx2, {
                type: "doughnut",
                data: {
                    labels: ['Phone', 'Email', 'Banner', 'Google', 'Direct', 'Website'],
                    datasets: [{
                        backgroundColor: ['#ff6384', '#36a2eb', '#9966ff', '#ffcd56', '#4bc0c0', '#c9cbcf'],
                        data: lead_by_medium_list,
                    }],
                },
            });
        }
    }

    async _lead_by_month(period) {
        const [leads, months] = await this.orm.call('crm.lead', "lead_by_month_table", [period]);

        const tableBody = this.leadsByMonthTable.el.querySelector('tbody');
        tableBody.innerHTML = '';
        for (let i = 0; i < months.length; i++) {
            const row = document.createElement('tr');
            row.innerHTML = `<td>${months[i]}</td><td>${leads[i]}</td>`;
            tableBody.appendChild(row);
        }
    }
}

CrmDashboard.template = "crm_dashboard.CrmDashboard";
actionRegistry.add("crm_dashboard_tag", CrmDashboard);
