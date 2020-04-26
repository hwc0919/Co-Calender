import Vue from 'vue'
import Vuex from 'vuex'
import App from './App'

Vue.config.productionTip = true
Vue.use(Vuex);

let today = new Date();

const store = new Vuex.Store({
    state: {
        today: today,
        curY: today.getFullYear(),
        curM: today.getMonth(),
        curD: today.getDate(),
        curWd: today.getDay()
    },
    mutations: {
        nextMonth(state) {
            state.curM++;
            if (state.curM > 11) {
                state.curM = 0;
                state.curY++;
            }
        },
        prevMonth(state) {
            state.curM--;
            if (state.curM < 0) {
                state.curM = 11;
                state.curY--;
            }
        }
    }
});

App.mpType = 'app'

const app = new Vue({
    ...App,
    store
}).$mount()
