async render_leads_by_month() {

    const tableBody = this.leadsByMonthTable.el.querySelector('tbody');


    const [leads, months] = await this.orm.call('crm.lead', "get_lead_by_month", []);


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
<div class="col-md-4">
                        <div class="row" style="display:flex; padding: 20px;">
                            <div class="card-body" id="in_ex_body_hide">
                                <div class="leads_stages card-shadow">
                                    <h2>Leads By Months</h2>
                                    <hr/>
                                    <div class="table_container">
                                        <table t-ref="leads_by_month_table" class="table table-striped table-bordered">
                                            <thead>
                                                <tr>
                                                    <th>Month</th>
                                                    <th>Leads</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>



@api.model
def get_lead_by_month(self):

    month_count = []
    month_value = []
    for rec in self.search([]):
        month = rec.create_date.month
        if month not in month_value:
            month_value.append(month)
        month_count.append(month)
    month_val = [{'label': calendar.month_name[month],
                  'value': month_count.count(month)} for month in
                 month_value]
    names = [record['label'] for record in month_val]
    counts = [record['value'] for record in month_val]
    month = [counts, names]
    return month
