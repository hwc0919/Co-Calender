import Vue from 'vue';
import Vuex from 'vuex';
import { userStore } from './UserStore';
import { calendarStore } from './CalendarStore';

Vue.use(Vuex);

export const store = new Vuex.Store({
    modules: {
        c: calendarStore,
        u: userStore
    }
});
