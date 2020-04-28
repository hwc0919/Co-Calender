import Vue from 'vue'
import App from './App'
import uniIcons from "@/components/uni-icons/uni-icons.vue"
import { store } from '@/store/store';

Vue.config.productionTip = true
Vue.component('uni-icons', uniIcons);

App.mpType = 'app'

const app = new Vue({
    ...App,
    store
}).$mount()
