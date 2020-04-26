<template>
    <div class="month-view-wrapper">
        <wd-header></wd-header>
        <div
            class="month-view-content"
            @touchstart="handleTouchStart"
            @touchmove="handleTouchMove"
            @touchend="handleTouchEnd"
            :style="{ left: left }"
        >
            <div class="one-month" v-for="(calendar, ind0) in calendars" :key="`calendar-${ind0}`">
                <div class="week-line" v-for="(week, ind1) in calendar" :key="`calendar-${ind0}-${ind1}`">
                    <div
                        class="day-block"
                        :class="{
                            gray: dayObj.month != (curM + ind0 - 1) % 12,
                            today: isToday(dayObj) && ind0 === 1
                        }"
                        v-for="(dayObj, ind2) in week"
                        :key="`calendar-${ind0}-${ind1}-${ind2}`"
                    >
                        <span class="hasSchedule"></span>
                        <span class="date">{{ dayObj.date }}</span>
                        <span class="lunar"></span>
                    </div>
                </div>
            </div>
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
        return {
            calendars: [[[]], [[]], [[]]],
            nextCalendar: [[]],
            x: 0,
            startX: 0,
            startT: 0,
            dragging: false
        };
    },
    methods: {
        isToday(dayObj) {
            return (
                this.today.getYear() == dayObj.year &&
                this.today.getDate() == dayObj.date &&
                this.today.getMonth() == dayObj.month &&
                this.today.getMonth() == this.curM
            );
        },
        calCalendar(curY, curM) {
            let calendar = [[]];
            let firstDayOfMonth = new Date(curY, curM, 1);
            let lastDayOfMonth = new Date(curY, curM + 1, 0);
            let iterDay = new Date(curY, curM, 1 - firstDayOfMonth.getDay());
            while (!(iterDay.getDay() === 0 && iterDay > lastDayOfMonth)) {
                if (calendar[calendar.length - 1].length === 7) calendar.push([]);
                calendar[calendar.length - 1].push({
                    year: iterDay.getYear(),
                    month: iterDay.getMonth(),
                    date: iterDay.getDate(),
                    day: iterDay.getDay()
                });
                iterDay.setDate(iterDay.getDate() + 1);
            }
            return calendar;
        },
        refreshCalendar(direction) {
            if (!direction) {
                this.$set(this.calendars, 0, this.calCalendar(this.curY, this.curM - 1));
                this.$set(this.calendars, 1, this.calCalendar(this.curY, this.curM));
                this.$set(this.calendars, 2, this.calCalendar(this.curY, this.curM + 1));
                return;
            }
            let calendar = [[]];
            while (!(iterDay.getDay() === 0 && iterDay > lastDayOfMonth)) {
                if (calendar[calendar.length - 1].length === 7) calendar.push([]);
                calendar[calendar.length - 1].push({
                    month: iterDay.getMonth(),
                    date: iterDay.getDate(),
                    day: iterDay.getDay()
                });
                iterDay.setDate(iterDay.getDate() + 1);
            }
            this.calendar = calendar;
        },
        handleTouchStart(event) {
            this.startX = event.touches[0].clientX;
            this.startT = new Date();
            this.dragging = true;
        },
        handleTouchMove(event) {
            if (this.dragging) {
                let curX = event.touches[0].clientX;
                this.x = curX - this.startX;
            }
        },
        handleTouchEnd() {
            let velocity = this.x / (new Date() - this.startT);
            if (this.x < uni.upx2px(-750 * 0.7) || velocity < -0.5) {
                this.$store.commit('nextMonth');
            } else if (this.x > uni.upx2px(750 * 0.7) || velocity > 0.5) {
                this.$store.commit('prevMonth');
            }
            this.refreshCalendar();
            this.x = 0;
        }
    },
    mounted() {
        this.refreshCalendar();
    },
    computed: {
        today() {
            return this.$store.state.today;
        },
        curY() {
            return this.$store.state.curY;
        },
        curM() {
            return this.$store.state.curM;
        },
        curD() {
            return this.$store.state.curD;
        },
        curWd() {
            return this.$store.state.curWd;
        },
        left() {
            return this.x - uni.upx2px(780) + 'px';
        }
    }
};
</script>

<style lang="scss" scope>
@import '@/static/css/week-line.scss';

.month-view-content {
    width: 750upx * 3 + 60upx;
    position: relative;
    display: flex;
}

.one-month {
    width: 770upx;
    padding: 0 10px;
}
</style>