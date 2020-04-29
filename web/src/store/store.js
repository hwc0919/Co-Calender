import Vue from 'vue';
import Vuex from 'vuex';
import { DateObj } from '@/static/js/DateObj';
import { CalendarTool } from '@/static/js/CalendarTool';

Vue.use(Vuex);

let today = new Date();
let year = today.getFullYear();
let month = today.getMonth();
let day = today.getDate();
let dayOfWeek = today.getDay();
today = new Date(year, month, day);

export const store = new Vuex.Store({
    state: {
        today: today,
        todayObj: new DateObj(today),
        year: year,
        month: month,
        day: day,
        dayOfWeek: dayOfWeek,
        calendars: {}
    },
    getters: {
        getMonthCalendar: (state) => (year, month) => {
            console.log('get', year, month);
            while (month > 11) {
                month -= 12;
                year++;
            }
            while (month < 0) {
                month += 12;
                year--;
            }
            if (!(year in state.calendars)) {
                state.calendars[year] = CalendarTool.calYearCalendar(year);
            }
            return state.calendars[year][month];
        },
        isToday(state) {
            return state.day === state.todayObj.day && state.month === state.todayObj.month && state.year === state.todayObj.year;
        }
    },
    mutations: {
        initCalendar(state) {
            Object.assign(state.calendars, {}, CalendarTool.calThreeYearCalendar(state.year));
        },
        switchMonth(state, direction) {
            if (direction < 0) {
                state.month--;
                if (state.month < 0) {
                    state.month = 11;
                    state.year--;
                }
            } else if (direction > 0) {
                state.month++;
                if (state.month > 11) {
                    state.month = 0;
                    state.year++;
                }
            }
        },
        selectDate(state, dateObj) {
            state.year = dateObj.year;
            state.month = dateObj.month;
            state.day = dateObj.day;
            state.dayOfWeek = dateObj.dayOfWeek;
        },
        resetToToday(state) {
            state.year = state.todayObj.year;
            state.month = state.todayObj.month;
            state.day = state.todayObj.day;
            state.dayOfWeek = state.todayObj.dayOfWeek;
        }
    }
});
