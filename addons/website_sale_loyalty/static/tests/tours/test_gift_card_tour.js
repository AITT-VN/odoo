/** @odoo-module **/

import { registry } from "@web/core/registry";
import * as tourUtils from '@website_sale/js/tours/tour_utils';

registry.category("web_tour.tours").add('shop_sale_gift_card', {
    url: '/shop',
    steps: () => [
        // Add a small drawer to the order (50$)
        ...tourUtils.addToCart({ productName: "TEST - Small Drawer", expectUnloadPage: true }),
        tourUtils.goToCart(),
        {
            content: 'insert gift card code',
            trigger: 'form[name="coupon_code"] input[name="promo"]',
            run: "edit GIFT_CARD",
        },
        {
            content: 'validate the gift card',
            trigger: 'form[name="coupon_code"] .a-submit',
            run: "click",
            expectUnloadPage: true,
        },
        {
            content: 'check gift card line',
            trigger: 'div>strong:contains("PAY WITH GIFT CARD")',
            run: "click",
        },
        {
            trigger: 'form[name="coupon_code"]',
        },
        {
            content: 'insert gift card code',
            trigger: 'form[name="coupon_code"] input[name="promo"]',
            run: "edit 10PERCENT",
        },
        {
            content: 'validate the gift card',
            trigger: 'form[name="coupon_code"] .a-submit',
            run: "click",
            expectUnloadPage: true,
        },
        {
            content: 'check gift card amount',
            trigger: '.oe_website_sale .oe_cart:contains(10% on your order)',
        },
        {
            trigger: "a:contains(continue shopping)",
            run: "click",
            expectUnloadPage: true,
        },
        ...tourUtils.addToCart({ productName: "TEST - Gift Card", expectUnloadPage: true }),
        tourUtils.goToCart({quantity: 2}),
        {
            content: 'check gift card amount',
            trigger: '.oe_website_sale .oe_cart',
        },
    ],
});
