<template>
    <div class="week-view-wrapper">
        <wd-header></wd-header>
        <div class="week-line">
            <span
                class="day-block"
                :class="{ today: dayObj.date == curD }"
                v-for="(dayObj, ind) in calendar"
                :key="`day-${ind}`"
            >
                <span class="hasSchedule"></span>
                <span class="date">{{ dayObj.date }}</span>
                <span class="lunar"></span>
            </span>
        </div>
    </div>
</template>


<script>
import WdHeader from './WdHeader';

export default {
    name: 'MonthView',
    components: {
        WdHeader
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
            calendar.push({
                month: iterDay.getMonth(),
                date: iterDay.getDate(),
                day: iterDay.getDay()
            });
            iterDay.setDate(iterDay.getDate() + 1);
        }
        return {
            curD: curD,
            calendar: calendar
        };
    }
};
</script>

<style lang="scss" scope>
@import '@/static/css/week-line.scss';

.week-view-wrapper {
    padding: 0 10upx;
}
</style>