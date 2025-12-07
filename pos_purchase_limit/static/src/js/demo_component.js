/** @odoo-module **/

import { Component, onMounted } from "@odoo/owl";
import { TimerMixin } from "./timer_mixin";

class BaseDemoComponent extends Component {
    static template = "DemoTimerComponent";
}

// Apply the mixin to the component
export class DemoComponent extends TimerMixin(BaseDemoComponent) {
    setup() {
        super.setup();

        // Start timer on mount
        onMounted(() => {
            this.startTimer();

            setTimeout(() => {
                const time = this.stopTimer();
                console.log("Time taken:", time, "ms");
            }, 1500);
            if (!navigator.onLine) {
                console.log("Internet is disconnected");
                const formData = {
                                name: "Test Customer",
                                 mobile: "9876543210"
                };

                localStorage.setItem("offline_partner_data", JSON.stringify(formData));
                console.log("Data stored in localStorage");
                }
            window.addEventListener("online", () => {
                    const data = localStorage.getItem("offline_partner_data");

            if (data) {
                const record = JSON.parse(data);

                console.log("Internet is back");
                     console.log("Offline data found:", record);

                 // Optional: remove after logging
                localStorage.removeItem("offline_partner_data");
    } else {
            console.log("No offline data found to sync.");
    }
});

        });

    }
}
