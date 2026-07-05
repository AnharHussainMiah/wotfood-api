import { reactive } from "vue";

export const basket = reactive({
    items: [],
    optionCache: new Map()
})