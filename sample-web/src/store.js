import { reactive } from "vue";

export const basket = reactive({
    items: [],
    optionCache: new Map() // because we have to load the item option from the database without caching the application will have really bad performance problems
})