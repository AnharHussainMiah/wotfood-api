# wotFood Public API

wotFood is an online fast food ordering platform like `JustEat` / `uberEats` and others. The purpose of this documentation is aimed at external 3rd Parties that wish to integrate with the wotFood platform using the "Public APIs".

## General Platform overview

wotFood is a custom multi-tenant eCommerce platform with deep hardware integration that runs at the partner's shops. We have a number of "landing pages" that are static and these pages link to each specfic online shop. When customers place an order, this is routed in realtime to the hardware at the shop, orders are then authorised or declined and the results are feed back to the customer. Once an order has been authorised the order is printed at the shop and the customer is given a confirmation email.

![](wotFood-Overview.png)

## Customer Journey

The customer experience for each shop can be deeply unique that can reflect very closely to each shops own branding, and the Public APIs allows pulling each shops metadata. Using the shops metadata the usual basket/cart interaction can be implemented.

Once all the products/items are added to the shopping basket/cart, a "call to action" button with something like "Checkout on wotFood" can then be used, and then the basket/cart data can be securely transferred to the wotFood platform using the `handover` API. Once the basket data has been transferred the customer can be redirected to the wotFood checkout page where they can place their order with the shop and make payment.

![](wotFood-handover.png)

### Public API

- Headers: `Content-Type: application/json`
- HTTP Verb: `POST`
- Staging Base URL: `https://neo.wotfood.co.uk`

| URL                            | Mandatory Parameters     | Description                                 |
| ------------------------------ | ------------------------ | ------------------------------------------- |
| /api/public/shop-details       | Company Id               | Returns meta data about the shop            |
| /api/public/opening-times      | Company Id               | Returns the shops opening and closing times |
| /api/public/menu-data          | Company Id               | Returns the shops menu data                 |
| /api/public/item-extra-options | Compnay Id + Item Id     | Returns Items custom optional exta data     |
| /api/public/handover-basket    | company Id + Basket Data | Returns the session Id for this checkout    |

## Sample Tests

This project includes a sample integration with the `public` API in the folder `wotfood-public-api`, this includes a basic set of unit tests you can run to confirm the APIs are running and what payload response you can expect to get.

To run the unit tests, we assume you have `uv` installed (and Python 3):

```shell
# change into the testing directory
$ cd wotfood-public-api/
# make sure to install all the dependencies
$ uv sync
# run the tests
$ uv run pytest -s
```

## Fully integrated Web App Sample

We have included a sample website that fully integrates all the Public API, this can be found in the folder `sample-web`, this is a clean implementation written using the Vue Framework. You can potentially use this as a starting point. This code fully demonstrates how to implement the handover API, as well as handle options and rendering baskets etc.

To test out and see how the "optional" and variations is implemented, in the sample you can use the product "Chingri Sizzler" under the "Non Veg Appetisers" category.

