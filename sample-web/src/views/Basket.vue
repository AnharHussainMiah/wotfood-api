<template>
    <h1>My Basket</h1>
    <button @click="btnBack">back</button>
    <br/>

    <span v-for="item in groupItems(basket.items)">
        {{ item.quantity }}x <b>{{ item.name }}</b> (£{{ item.price }}) <button @click="btnMinus(item)">MINUS</button><button @click="btnAdd(item)">ADD</button> <button @click="btnDelete(item)">DEL</button>
        <div v-if="item.options && item.options.length > 0">
            <span v-for="id in item.options">
                {{ renderOptionData(item.id, id) }}<br/>
            </span>
        </div>
        <br/>

    </span>

    <h2>TOTAL:  £{{  computeTotal() }}</h2>

    <button @click="btnCheckout">Check Out on wotFood</button>

</template>

<script>
import config from '../config';
import { basket } from '../store'
import { postJson } from '../api';

export default {
    data() {
        return {
            basket: basket
        }
    },
    methods: {
        btnBack() {
            this.$router.push({path: "/"})
        },
        btnDelete(item) {
            this.basket.items = this.basket.items.filter(x => x.name != item.name);
        },
        btnAdd(item) {
            const {quantity, ...newItem } = item;
            this.basket.items.push(newItem);
        },

        btnMinus(item) {
            const key = this.makeCompoundKey(item);
            const index = this.basket.items.findIndex( x => this.makeCompoundKey(x) == key);
            if(index !== -1) {
                this.basket.items.splice(index, 1);
            }
        },

        makeCompoundKey(item) {
            const key = `${item.name}|${JSON.stringify(
                [...new Set(item.options ?? [])].sort((a, b) => a - b)
            )}`;
            return key;
        },

        renderOptionData(itemId, optionId) {
            const options = this.basket.optionCache.get(itemId);
            const option = options.filter(x => x.id == optionId);

            if(option.length > 0) {
                return `....... (${option[0].title}) ${option[0].name} £${option[0].price}`
            }

            return `${itemId} | ${optionId}`
        },

        groupItems(items) {
            const grouped = [...items.reduce((map, item) => {

            const key = this.makeCompoundKey(item);

            const existing = map.get(key);

            if (existing) {
                existing.quantity++;
            } else {
                map.set(key, {
                ...item,
                quantity: 1,
                });
            }

            return map;
            }, new Map()).values()];

            // console.log(grouped);
            return grouped.sort();
        },

        computeTotal() {
            const total = this.groupItems(this.basket.items).reduce((sum, x) => {
                if(x.options) {
                    return sum + (x.price + (this.computeItemOptionTotal(x)) * x.quantity);
                } else {
                    return sum + (x.price * x.quantity);
                }
            }, 0);
            return total;
        },

        computeItemOptionTotal(item) {
            const options = this.basket.optionCache.get(item.id);

            const idToPrice = new Map(options.map(x => [x.id, x]));

            const subtotal = item.options.reduce((sum, id) => {
                return sum + (idToPrice.get(id)?.price ?? 0);
            }, 0);

            return subtotal;
        },

        btnCheckout() {
            /* -------------------------------------------------------------------------------------
            Here we use the "handover api", we have to craft the correct payload, and in theory if
            all the server side checks pass, it should return as a unique session that we can then
            redirect to for the customer to complete the sale.

            If the customer hits the back button, they will lose the basket, allthough we may have
            to potentially think about a way to persist the basket perhaps?

            Schema:

            PublicBasket {
                companyId: 1,
                
                basket: [
                    {
                        productId: 1,
                        quantity: 2,
                        options: []
                    },
                    {
                        productId: 2,
                        quantity: 1,
                        options: [
                            {
                                groupName: "Size",
                                id: 2
                            },
                            {
                                groupName: "Toppings",
                                id: 4
                            }
                        ]
                    }
                ],

                sessionId: null
            }


            redirection to: /basket?sessionId=xxx

            ------------------------------------------------------------------------------------- */
            const PublicBasket = {
                companyId: config.COMPANY_ID,
                basket: this.groupItems(this.basket.items).map(x => ({
                        productId: x.id, 
                        quantity: x.quantity,
                        options: x.options && x.options.length > 0 ? this.injectOptionTitle(x.options, x.id) : []
                    })
                ),
                sessionId: null
            };

            this.submitBasket(PublicBasket);
        },

        async submitBasket(basket) {
            try {
                const result = await postJson(`${config.BASE_URL}/api/public/handover-basket`, basket);
                console.log("Success:", result);
                
                // if we have the sessionId, built the url and redirect here

            } catch (error) {
                console.error("Unable to complete request:", error.message);
            }
        },

        injectOptionTitle(options, itemId) {
            /*
            when we have options [1, 2, 3]
            
            we want to return 
            
            [
                {
                    groupName: "Size", // groupName is actually the title
                    id: 1
                },
                ... (and so forth)
            ]

            */
        
            const optionsCache = this.basket.optionCache.get(itemId);            
            
            const optionMap = new Map(optionsCache.map(x => [x.id, x]));

            const result = options.map(id => {
                const option = optionMap.get(id);
                return option
                    ? { groupName: option.title, id: option.id }
                    : null;
            }).filter(Boolean);
            
            return result;
        }
    }
}


</script>