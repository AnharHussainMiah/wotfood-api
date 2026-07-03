<template>
    <h1>My Basket</h1>
    <button @click="btnBack">back</button>
    <br/>

    <span v-for="item in groupItems(basket.items)">
        {{ item.quantity }}x <b>{{ item.name }}</b> (£{{ item.price }}) <button @click="btnMinus(item)">MINUS</button><button @click="btnAdd(item)">ADD</button> <button @click="btnDelete(item)">DEL</button>
        <br/>

    </span>

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
        }
    }
}


</script>