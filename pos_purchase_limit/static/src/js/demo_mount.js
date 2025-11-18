/** @odoo-module **/

import { registry } from "@web/core/registry";
import { DemoComponent } from "./demo_component";

registry.category("main_components").add("demo_timer_component", {
    Component: DemoComponent,
});
