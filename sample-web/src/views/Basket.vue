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

</template>

<script>
import { basket } from '../store'

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
                return sum + (x.price * x.quantity);
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
        }
    }
}


</script>