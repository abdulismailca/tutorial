/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { Product } from "@point_of_sale/app/store/product";
import { ProductList } from "@point_of_sale/app/screens/product_screen/product_list/product_list";
import { ProductCard } from "@point_of_sale/app/generic_components/product_card/product_card";

patch(Product.prototype, {
    setup() {
        this._super(...arguments);
        console.log("Loaded product with rating:", this.display_name, this.quality_rating);
    },
});

patch(ProductList.prototype, {
    getProductProps(product) {
        return {
            ...super.getProductProps(product),
            quality_rating: product.quality_rating,
        };
    },
});

patch(ProductCard, {
    props: {
        ...ProductCard.props,
        quality_rating: { type: String, optional: true },
    },
});
