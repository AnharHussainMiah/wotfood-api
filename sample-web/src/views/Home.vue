<template>
    <div v-if="!showOptions">
        <h1>{{ companyDetail.name }}</h1>
        <p>{{  companyDetail.phone }}</p>
        <p>{{  companyDetail.address }}</p>

        <button @click="btnBasket">Go To My Basket</button>

        <b>Basket Total:</b> {{ basket.items.length }}

        <h3>Opening Times</h3>

        <span v-for="open in openingTimes">
            <b>{{ open.open_day }}</b> {{ open.open_hour }}:{{ open.open_min }} to {{ open.close_hour }}:{{ open.close_min }} <br/>
        </span>

        <h3>Menu</h3>

        <span v-for="category in categories">
            <h2>{{ category }}</h2>
            <span v-for="item in filterItems(category)">
                <button @click="btnAdd(item)">+Add</button> <b>{{ item.name  }} £({{ item.price }})</b> 
                <br/>
                {{ item.description  }}
                <br/>
                <br/>
            </span>
            <hr/>
        </span>

        <button @click="btnBasket">Go To My Basket</button>
    
    </div>
    <div v-else>

        <div v-if="optionData" v-for="title in getTitles(optionData)">
            <h2>{{ title }}</h2>

            <div v-for="option in getSubOptions(title)">
                <div v-if="option.option_kind=='pick-one'">
                    <input
                        type="radio"
                        :name="option.name"
                        :value="option.id"
                        :checked="isIdSelected(option.id)"
                        @change="setPickOne(title, option.id)"
                    />
                    {{ option.name }} £{{ option.price }}<br/>
                </div>
                <div v-else>
                    pick many:
                    {{ option.name }} £{{ option.price }}<br/>
                </div>
            </div>
        </div>
    

        <button @click="btnCancelOption">CANCEL</button>
    </div>
</template>

<script>

// :checked="selected[group.groupId] === item.id"
// @change="select(group.groupId, item.id)"

import config from '../config';
import { postJson } from '../api';
import { basket } from '../store';

export default {
    data() {
        return {
            companyDetail: {},
            openingTimes: {},
            menuData: {},
            categories: {},
            basket: basket,
            showOptions: false,
            optionData: null,
            optionPicked: [],
            optionItem: {}
        }
    },
    mounted () {
        this.getCompanyDetails();
        this.getOpeningTimes();
        this.getMenuData();
    },
    methods: {
        async getCompanyDetails() {
            try {
                const result = await postJson(`${config.BASE_URL}/api/public/shop-details`, {companyId: config.COMPANY_ID});
                // console.log("Success:", result);
                this.companyDetail = result[0];
            } catch (error) {
                console.error("Unable to complete request:", error.message);
            }
        },
        async getOpeningTimes() {
            try {
                const result = await postJson(`${config.BASE_URL}/api/public/opening-times`, {companyId: config.COMPANY_ID});
                // console.log("Success:", result);
                this.openingTimes = result;
            } catch (error) {
                console.error("Unable to complete request:", error.message);
            }
        },
        async getMenuData() {
            try {
                const result = await postJson(`${config.BASE_URL}/api/public/menu-data`, {companyId: config.COMPANY_ID});
                // console.log("Success:", result);
                this.menuData = result;
                this.categories = [...new Set(result.map(item => item.category))];
                console.log(this.categories);
            } catch (error) {
                console.error("Unable to complete request:", error.message);
            }
        },

        async loadOptionData(productId) {
            try {
                const result = await postJson(`${config.BASE_URL}/api/public/item-extra-options`, {productId: productId});
                console.log("Success:", result);
                console.log(result);
                this.optionData = result;
                this.showOptions = true;
            } catch (error) {
                console.error("Unable to complete request:", error.message);
            }
        },

        setPickOne(title, id) {
            const options = this.optionData.filter(x => x.title == title).map(x => x.id);

            // reset this group by title
            this.optionPicked = this.optionPicked.filter(x => !options.includes(x))
            this.optionPicked.push(id);

            console.log(`pciked ${title} | ${id}`)
        },

        isIdSelected(id) {
            return this.optionPicked.includes(id);
        },

        getTitles(optionData) {
            const titles = [...new Set(optionData.map(x => x.title))];
            console.log(titles);
            return titles;
        },

        getSubOptions(title) {
            return this.optionData.filter(x => x.title == title);
        },

        filterItems(cateogry) {
            return this.menuData.filter(x => x.category == cateogry)
        },
        btnAdd(item) {
            if(item.has_options) {
                this.showOptions = false;
                this.optionItem = item;
                this.optionPicked = [];
                this.optionData = null;

                this.loadOptionData(item.id);

                return;
            }
            this.basket.items.push(item)
        },
        btnBasket() {
            this.$router.push({path: "/basket"})
        },
        btnCancelOption() {
            this.showOptions = false
        }
    }
}
</script>