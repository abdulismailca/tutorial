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
            await this._fetch_data();
            await this._render_lost_lead_graph();
            await this._render_activity_chart();
            await this._render_leads_by_medium();
            await this._render_leads_by_campaign();
            await this._lead_by_month();

            // Handle filter change
            const filterSelect = document.getElementById("period_filter");
            filterSelect.addEventListener("change", async (event) => {
                const period = event.target.value;
                await this._refresh_all(period);
            });
        });
    }

    async _refresh_all(period) {
        await this._render_lost_lead_graph(period);
        await this._render_activity_chart(period);
        await this._render_leads_by_medium(period);
        await this._render_leads_by_campaign(period);
        await this._lead_by_month(period);

    }

    async _fetch_data() {
        const result = await this.orm.call("crm.lead", "get_tiles_data", [], {});
        document.getElementById("my_lead").innerText = result.total_leads;
        document.getElementById("my_opportunity").innerText = result.total_opportunity;
        document.getElementById("future_revenue").innerText = result.currency + result.expected_revenue;
        document.getElementById("user_invoiced_revenue").innerText = result.currency + result.user_all_invoices_amount;
        document.getElementById("my_lose_count").innerText = result.currency + result.my_lose;
        document.getElementById("won_los_ration").innerText = result.won_los_ration;
    }

    async _render_lost_lead_graph() {
        const data = await this.orm.call("crm.lead", "get_lost_won_graph_data", []);
        const ctx = document.getElementById("lost_lead_graph");
        if (!ctx) return;
        new Chart(ctx, {
            type: "bar",
            data: {
                labels: data.labels,
                datasets: [{
                    label: "Lost vs Won vs Open",
                    backgroundColor: ['#28a745', '#dc3545', '#ffc107'],
                    data: data.values,
                }],
            },
            options: {
                responsive: true,
                plugins: { legend: { display: false } },
                scales: { y: { beginAtZero: true } },
            },
        });
    }

    async _render_activity_chart() {
        const activity_list = await this.orm.call("crm.lead", "get_activity_list", []);
        const ctx = document.getElementById("chart_example");
        if (!ctx) return;
        new Chart(ctx, {
            type: "pie",
            data: {
                labels: ['Email', 'Call', 'To-Do'],
                datasets: [{
                    backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56'],
                    data: activity_list,
                }],
            },
        });
    }

    async _render_leads_by_medium() {
        const lead_by_medium_list = await this.orm.call("crm.lead", "lead_by_medium", []);
        const ctx = document.getElementById("doughnut_example");
        if (!ctx) return;
        new Chart(ctx, {
            type: "doughnut",
            data: {
                labels: ['Phone', 'Email', 'Banner', 'Google Adwords', 'Direct', 'Website'],
                datasets: [{
                    backgroundColor: [
                        '#FF6384', '#36A2EB', '#FFCE56',
                        '#4BC0C0', '#9966FF', '#FF9F40'
                    ],
                    data: lead_by_medium_list,
                }],
            },
        });
    }

    async _render_leads_by_campaign() {
        const data = await this.orm.call("crm.lead", "lead_by_campaign", []);
        const ctx = document.getElementById("leads_by_campaign_chart");
        if (!ctx) return;
        new Chart(ctx, {
            type: "doughnut",
            data: {
                labels: data.labels,
                datasets: [{
                    backgroundColor: [
                        '#FF6384', '#36A2EB', '#FFCE56',
                        '#4BC0C0', '#9966FF', '#FF9F40'
                    ],
                    data: data.values,
                }],
            },
        });
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

    async _lead_by_month(period) {
        const tableBody = this.leadsByMonthTable.el.querySelector("tbody");
        const [leads, months] = await this.orm.call("crm.lead", "lead_by_month_table", [period]);
        tableBody.innerHTML = "";
        for (let i = 0; i < months.length; i++) {
            const row = document.createElement("tr");
            const monthCell = document.createElement("td");
            const leadsCell = document.createElement("td");
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
