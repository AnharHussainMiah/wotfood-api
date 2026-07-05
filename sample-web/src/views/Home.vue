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
                    <input 
                        type="checkbox" 
                        :id="option.id" 
                        :value="option.id"
                        @change="setManyPicked($event, option.id)"
                    >
                    <label :for="option.id">{{ option.name }} £{{ option.price }}</label><br>
                    
                </div>
            </div>
        </div>
    

        <h3 style="color:red" v-if="optionError !== ''">{{ optionError }}</h3>

        <button @click="btnCancelOption">CANCEL</button>
        <button @click="btnOptionAdd">ADD</button>
    </div>
</template>

<script>

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
            optionData: null, // option data as loaded in from the database
            optionPicked: [], // the options the user has picked
            optionItem: {},   // the current item that was clicked (parent)
            optionError: ''
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
            } catch (error) {
                console.error("Unable to complete request:", error.message);
            }
        },

        async loadOptionData(productId) {
            try {
                const result = await postJson(`${config.BASE_URL}/api/public/item-extra-options`, {productId: productId});
                // console.log("Success:", result);
                // console.log(result);
                this.optionData = result;
                this.showOptions = true;
                basket.optionCache.set(productId, result);
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

        setManyPicked(event, id) {
            if(event.target.checked) {
                console.log(`checkbox ID ${id} picked!`)
                this.optionPicked.push(id);
            } else {
                console.log(`checkbox ID ${id} unpicked!`)
                this.optionPicked = this.optionPicked.filter( x => x !== id);
            }
        },

        btnOptionAdd() {
            this.optionError = "";
            /* -------------------------------------------------------------------------------------
            For each of the option sub groups, for the "pick one" we have to make sure one and only
            one id has been picked. For the "pick many" we have to make sure at least one ID has
            been picked.
            ------------------------------------------------------------------------------------- */
            const titles = [... new Set(this.optionData.map( x => x.title))];

            for(const title of titles) {
                console.log(`Validating (${title})`);
                const options = this.optionData.filter(x => x.title == title);
                
                if(options.length > 0 && options[0].option_kind == 'pick-one') {
                    if(this.optionPicked.filter(x => options.map(y => y.id).includes(x)).length !== 1) {
                        this.optionError = `You have to pick one option from "${title}"`;
                        return
                    }
                }

                if(options.length > 0 && options[0].option_kind == 'pick-many') {
                    if(this.optionPicked.filter(x => options.map(y => y.id).includes(x)).length < 1) {
                        this.optionError = `You have to pick at least one option from "${title}"`;
                        return
                    }
                }
            }

            // all the option(s) are selected we can add this to the basket now

            this.basket.items.push({
                ...this.optionItem,
                options: this.optionPicked
            })
            this.showOptions = false;
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
                this.optionError = '';

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