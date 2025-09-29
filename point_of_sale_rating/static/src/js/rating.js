import { PosOrderline } from "@point_of_sale/app/models/pos_order_line";
import { Orderline } from "@point_of_sale/app/generic_components/orderline/orderline";
import { patch } from "@web/core/utils/patch";

patch(PosOrderline.prototype, {
    setup(vals) {
        this.quality_rating = this.product_id.quality_rating || "";
        return super.setup(...arguments);
    },
    getDisplayData() {
     console.log("helo",this.get_product());
        return {
            ...super.getDisplayData(),

            quality_rating: this.get_product().quality_rating || "",
        };
    },
});

patch(Orderline, {
    props: {
        ...Orderline.props,
        line: {
            ...Orderline.props.line,
            shape: {
                ...Orderline.props.line.shape,
                quality_rating: { type: String, optional: true },
            },
        },
    },
});
