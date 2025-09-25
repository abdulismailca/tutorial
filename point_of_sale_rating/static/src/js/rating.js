/** @odoo-module */



import { patch } from "@web/core/utils/patch";
import { ProductCard } from "@point_of_sale/app/generic_components/product_card/product_card";


patch(ProductCard, {
    props: {
        ...ProductCard.props,
        qty: {type: Number, optional: true},
    },
})













//import { registry } from "@web/core/registry";




//import { usePos } from "@point_of_sale/app/store/pos_hook";
//import { Component } from "@odoo/owl";
//
//
//import { patch } from "@web/core/utils/patch";
//import { PosStore } from "@point_of_sale/app/store/pos_store";
//
//
////patch(PosStore,prototype,{
////   _loadProductProduct(products) {
////    var self = this;
////    super._loadProductProduct(...arguments);
////    for(const prod of products){
////
////    self.db.product_by_id[prod.id].quality_rating =  prod.quality_rating
////
////    }
////
////   }
////
////})
//
//
//
//
