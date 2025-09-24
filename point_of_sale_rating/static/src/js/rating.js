/** @odoo-module **/

import { renderToElement } from "@web/core/utils/render";
import { renderToFragment } from "@web/core/utils/render";
import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";



publicWidget.registry.get_machine_tab = publicWidget.Widget.extend({
    selector: '.newly_machine_section',


    async willStart() {



        const result = await rpc('/newly_machines', {});
        const chunkData = chunkArray(result, 4);
        chunkData[0].is_active = true;
         if(result){

            var uniqueid = this.generateUniqueId();


            this.$target.empty().html(renderToFragment('machine_management.machine_chunk_wise', {chunkData,uniqueid}))
        }



        },


        generateUniqueId() {
       return Date.now().toString(36) + Math.random().toString(36);
   },

});





