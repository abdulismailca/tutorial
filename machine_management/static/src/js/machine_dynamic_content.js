/** @odoo-module **/
console.log("iam here")
import { renderToElement } from "@web/core/utils/render";
import { renderToFragment } from "@web/core/utils/render";
import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";



publicWidget.registry.get_product_rating = publicWidget.Widget.extend({
    selector: '.quality_rating',


    async willStart() {



        const result = await rpc('/quality/rating', {});


         if(result){



            this.$target.empty().html(renderToFragment('quality_rating_template', {}))
        }



        },




});





