<template>
    <div class="week-view-wrapper">
        <week-header></week-header>
        <div class="one-week">
            <day-block class="day-block" v-for="(dateObj, ind) in calendar" :dateObj="dateObj" :key="`day-${ind}`">
                <span class="hasSchedule"></span>
                <span class="date">{{ dateObj.day }}</span>
                <span class="lunar"></span>
            </day-block>
        </div>
    </div>
</template>


<script>
import WeekHeader from './WeekHeader';
import DayBlock from './DayBlock';
import { DateObj } from '@/static/js/DateObj';

export default {
    name: 'MonthView',
    components: {
        WeekHeader,
        DayBlock
    },
    data() {
        let today = new Date();
        let curY = today.getFullYear();
        let curM = today.getMonth();
        let curD = today.getDate();
        let curWd = today.getDay();
        let firstDayOfYear = new Date(curY, 0, 1);
        let curW = ((today - firstDayOfYear) / 3600000 / 24 - (7 - firstDayOfYear.getDay())) / 7 + 2;
        let firstDayOfWeek = new Date(curY, curM, curD - curWd);
        let lastDayOfWeek = new Date(curY, curM, curD + 6 - curWd);
        let calendar = [];

        let iterDay = firstDayOfWeek;
        while (iterDay <= lastDayOfWeek) {
            calendar.push(new DateObj(iterDay));
            iterDay.setDate(iterDay.getDate() + 1);
        }
        return {
            calendar: calendar
        };
    },
    methods: {
        handleTest(data) {
            console.log('test');
            console.log(data.msg);
        }
    },
    mounted() {
        uni.$on('test', this.handleTest);
    },
    beforeDestroy() {
        uni.$off('test');
    }
};
</script>

<style lang="scss" scope>
.week-view-wrapper {
}

.one-week {
    display: flex;
    justify-content: space-evenly;
    padding: 10upx 10upx;
}
</style>