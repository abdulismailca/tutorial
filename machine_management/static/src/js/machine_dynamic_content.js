/** @odoo-module **/

import { renderToElement } from "@web/core/utils/render";
import { renderToFragment } from "@web/core/utils/render";
import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";



publicWidget.registry.get_product_tab = publicWidget.Widget.extend({
    selector: '.newly_machine_section',


    async willStart() {

        function chunkArray(arr, chunkSize) {
            const result = [];
            for (let i = 0; i < arr.length; i += chunkSize) {
                result.push(arr.slice(i, i + chunkSize));
            }
            return result;
        }

        const result = await rpc('/newly_machines', {});
        const chunkData = chunkArray(result, 4);
        chunkData[0].is_active = true;
         if(result){
            console.log("data found", result);
            console.log("chunkData",chunkData);
            var uniqueid = this.generateUniqueId();
            console.log("uniqueid",uniqueid);

            this.$target.empty().html(renderToFragment('machine_management.machine_chunk_wise', {chunkData,uniqueid}))
        }



        },


        generateUniqueId() {
       return Date.now().toString(36) + Math.random().toString(36);
   },

});




//odoo.define('elearning_course_snippet.snippet', function(require) {
//'use strict';
//var PublicWidget = require('web.public.widget');
//var rpc = require('web.rpc');
//var core = require('web.core');
//var qweb = core.qweb;
//var Dynamic = PublicWidget.Widget.extend({
//
//selector: '.newly_machine_section',
//
//willStart: async function() {
//
//var self = this;
//
//await rpc.query({
//
//route: '/newly_machines',
//
//}).then((data) => {
//
//this.data = data;
//
//});
//
//},
//
//start: function() {
//
//var chunks = _.chunk(this.data, 4)
//
//chunks[0].is_active = true
//
//this.$el.find('#carousel_machines_snippet').html(
//
//qweb.render('machine_management.machine_chunk_wise', {
//
//chunks
//
//})
//
//)
//
//},
//});
//PublicWidget.registry.dynamic_snippet_blog = Dynamic;
//return Dynamic;
//});
