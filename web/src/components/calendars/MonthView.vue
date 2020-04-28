<!--

1.月份切换的逻辑
    调用 $store.mutations.selectDate, 修改 $store.state.selectDate
    this.watch 监听 $store.state.selectDate, 
        调用 $store.mutations.switchMonth, 修改 $store.state.month
        调用 this.finishSlide(direction), 完成滑动翻页

2.月份切换的两种可能途径:
    1. 通过滑动, 若滑动速度或滑动幅度超过阈值, 触发切换,
    2. 通过点击上月或下月的日期, 触发 DayBlock.handleClick

月份切换的组件间耦合度很大.
-->

<template>
    <div class="month-view-wrapper">
        <week-header></week-header>
        <div
            ref="month"
            :class="['month-view-content', { 'scroll-over-animation': scrollOver }]"
            @touchstart="handleTouchStart"
            @touchmove="handleTouchMove"
            @touchend="handleTouchEnd"
            :style="{ left: left }"
        >
            <div class="one-month" v-for="(calendar, ind0) in calendars" :key="`calendar-${ind0}`">
                <div class="one-week" v-for="(week, ind1) in calendar" :key="`calendar-${ind0}-${ind1}`">
                    <day-block
                        v-for="(dateObj, ind2) in week"
                        :key="`calendar-${ind0}-${ind1}-${ind2}`"
                        :dateObj="dateObj"
                    >
                    </day-block>
                </div>
            </div>
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
        return {
            calendars: [[], [], []],
            x: 0,
            startX: 0,
            startT: 0,
            dragging: false,
            showDragging: false,
            canDrag: true,
            timeout: null,
            scrollOver: false
        };
    },
    methods: {
        finishSlide(direction) {
            if (direction === 0) {
                this.scrollOver = true;
                this.timeout = setTimeout(() => {
                    this.scrollOver = false;
                    this.x = 0;
                }, 300);
                return;
            }
            let targetX = direction * uni.upx2px(750);
            this.refreshCalendar();
            this.x += targetX;
            this.$nextTick(() => {
                this.$refs.month.offsetWidth; // Important: Force update
                this.scrollOver = true; // activate .scroll-over-animation
                this.timeout = setTimeout(() => {
                    this.scrollOver = false;
                    this.x = 0;
                }, 300);
            });
        },
        refreshCalendar() {
            this.$set(this.calendars, 0, this.$store.getters.getMonthCalendar(this.year, this.month - 1));
            this.$set(this.calendars, 1, this.$store.getters.getMonthCalendar(this.year, this.month));
            this.$set(this.calendars, 2, this.$store.getters.getMonthCalendar(this.year, this.month + 1));
        },
        handleTouchStart(event) {
            clearTimeout(this.timeout);
            this.x = 0;
            this.scrollOver = false;
            this.startX = event.touches[0].clientX;
            this.startT = new Date();
            this.dragging = true;
        },
        handleTouchMove(event) {
            if (this.dragging) {
                let curX = event.touches[0].clientX;
                if (this.showDragging) {
                    this.x = curX - this.startX;
                } else {
                    if (Math.abs(curX - this.startX) > uni.upx2px(30)) {
                        this.showDragging = true;
                    }
                }
            }
        },
        handleTouchEnd() {
            if (this.dragging) {
                this.dragging = false;
                this.showDragging = false;
                let velocity = this.x / (new Date() - this.startT);
                let s = this.$store.state.selectDate;

                if (this.x < uni.upx2px(-750 * 0.7) || velocity < -0.5) {
                    let newS = new DateObj(new Date(s.year, s.month + 1, s.day));
                    this.$store.commit('selectDate', newS);
                } else if (this.x > uni.upx2px(750 * 0.7) || velocity > 0.5) {
                    let newS = new DateObj(new Date(s.year, s.month - 1, s.day));
                    this.$store.commit('selectDate', newS);
                } else if (this.x !== 0) {
                    this.finishSlide(0);
                }
            }
        }
    },
    mounted() {
        this.refreshCalendar();
    },
    computed: {
        today() {
            return this.$store.state.today;
        },
        year() {
            return this.$store.state.year;
        },
        month() {
            return this.$store.state.month;
        },
        day() {
            return this.$store.state.day;
        },
        dayOfWeek() {
            return this.$store.state.dayOfWeek;
        },
        left() {
            return this.x - uni.upx2px(750) + 'px';
        }
    },
    watch: {
        '$store.state.selectDate'(selectDate) {
            if (
                (selectDate.year === this.year && selectDate.month === this.month - 1) ||
                (selectDate.year === this.year - 1 && selectDate.month === 11 && this.month === 0)
            ) {
                this.$store.commit('switchMonth', -1);
                this.finishSlide(-1);
            } else if (
                (selectDate.year === this.year && selectDate.month === this.month + 1) ||
                (selectDate.year === this.year + 1 && selectDate.month === 0 && this.month === 11)
            ) {
                this.$store.commit('switchMonth', 1);
                this.finishSlide(1);
            } else if (selectDate.isToday()) {
                this.$store.commit('resetToToday');
                this.refreshCalendar();
            }
        }
    }
};
</script>

<style lang="scss" scope>
.month-view-content {
    width: 750upx * 3;
    position: relative;
    display: flex;
}

.one-month {
    width: 750upx;
    padding: 0 10upx;
}

.one-week {
    display: flex;
    justify-content: space-evenly;
    padding: 10upx 0;
}

.scroll-over-animation {
    left: -750upx !important;
    transition: left 0.3s ease-out;
}
</style>