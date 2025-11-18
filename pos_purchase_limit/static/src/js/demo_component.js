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
        });
    }
}
