/** @odoo-module **/

export function TimerMixin(BaseComponent) {
    return class extends BaseComponent {
        setup() {
            super.setup();
            this.startTime = null;
            this.endTime = null;
        }

        startTimer() {
            this.startTime = Date.now();
            console.log("Timer Started");
        }

        stopTimer() {
            this.endTime = Date.now();
            const diff = this.endTime - this.startTime;
            console.log("Timer Stopped:", diff, "ms");
            return diff;
        }
    };
}
