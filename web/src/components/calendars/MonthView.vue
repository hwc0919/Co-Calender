<template>
    <div class="month-view-wrapper">
        <week-header></week-header>
        <div
            id="month"
            ref="month"
            :class="['month-view-content', { 'scroll-over-animation': scrollOver }]"
            @touchstart="handleTouchStart"
            @touchmove.prevent="handleTouchMove"
            @touchend="handleTouchEnd"
            @touchcancel="handleTouchEnd"
            :style="{ left: left }"
        >
            <div class="one-month" v-for="calendar in calendars" :key="`calendar-${calendar[1][0].month}`">
                <div
                    class="one-week"
                    :style="{ height: weekHeight }"
                    v-for="(week, ind1) in calendar"
                    :key="`calendar-${calendar[1][0].month}-${ind1}`"
                >
                    <div class="one-week-days">
                        <day-block
                            v-for="(dateObj, ind2) in week"
                            :key="`calendar-${calendar[1][0].month}-${ind1}-${ind2}`"
                            :dateObj="dateObj"
                            :month="calendar[1][0].month"
                            @click.native="selectDate(dateObj)"
                        >
                        </day-block>
                    </div>
                    <div class="one-week-detail" :style="{ height: weekDetailHeight }"></div>
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
        const query = uni
            .createSelectorQuery()
            .in(this)
            .select('#month');
        return {
            calendars: [
                this.$store.getters.getMonthCalendar(this.$store.state.c.year, this.$store.state.c.month - 1),
                this.$store.getters.getMonthCalendar(this.$store.state.c.year, this.$store.state.c.month),
                this.$store.getters.getMonthCalendar(this.$store.state.c.year, this.$store.state.c.month + 1)
            ],
            query: query,
            x: 0,
            oldX: 0,
            startX: 0,
            startY: 0,
            startT: 0,
            scrollX: false,
            scrollY: false,
            timeout: null,
            scrollOver: false,
            showDetail: false,
            scheduleMap: {}
        };
    },
    methods: {
        handleScrollX(direction) {
            /*
                If direction === 0, go back to current month
                If direction === -1, go to previous month
                If direction === 1, go to next month

                When direction === 0, reset x to 0 with animation.
                When direction !== 0, first rotate `this.calandars`,
                finish scroll animation, then update `this.calendars`
            */
            console.log('Handle scroll X', direction);

            let targetX = direction * uni.upx2px(750);
            if (direction === 1) {
                this.calendars.push(this.calendars.shift());
            } else if (direction === -1) {
                this.calendars.unshift(this.calendars.pop());
            }
            this.x += targetX;
            this.$nextTick(() => {
                this.$refs.month.offsetWidth; // Important: Force update
                this.scrollOver = true; // activate .scroll-over-animation
                this.timeout = setTimeout(() => {
                    this.scrollOver = false;
                    this.resetCalendar();
                }, 300);
            });
        },

        handleScrollY(direction) {
            /*
                If direction === -1, close week-details
                If direction === 1, open week-details
            */
            console.log('Handle scroll Y', direction);
            if (direction === 1) this.showDetail = true;
            else if (direction === -1) this.showDetail = false;
        },

        resetCalendar() {
            if (this.calendars[1][1][0].month !== this.$store.state.c.month) {
                console.log('reset');
                this.$set(this.calendars, 0, this.$store.getters.getMonthCalendar(this.year, this.month - 1));
                this.$set(this.calendars, 1, this.$store.getters.getMonthCalendar(this.year, this.month));
                this.$set(this.calendars, 2, this.$store.getters.getMonthCalendar(this.year, this.month + 1));
            }
            this.x = 0;
        },

        selectDate(dateObj) {
            // Select date of next month
            if (
                (this.year === dateObj.year && this.month === dateObj.month - 1) ||
                (this.year === dateObj.year - 1 && this.month === 11 && dateObj.year === 0)
            ) {
                this.handleScrollX(1);
                this.$store.commit('selectDate', dateObj);
            }
            // Select date of previous month
            else if (
                (this.year === dateObj.year && this.month === dateObj.month + 1) ||
                (this.year === dateObj.year + 1 && this.month === 0 && dateObj.year === 11)
            ) {
                this.handleScrollX(-1);
                this.$store.commit('selectDate', dateObj);
            } else {
                this.$store.commit('selectDate', dateObj);
                this.resetCalendar();
            }
        },

        schedulesOnDate() {},

        /* **************************************** */
        /*             Handle Scroll                */
        /* **************************************** */
        handleTouchStart(event) {
            console.log('touch start');
            this.scrollX = this.scrollY = false;
            clearTimeout(this.timeout);
            this.query
                .boundingClientRect(data => {
                    this.x = data.left + uni.upx2px(750);
                    this.oldX = this.x;
                })
                .exec();
            this.scrollOver = false;
            this.startX = event.touches[0].clientX;
            this.startY = event.touches[0].clientY;
            this.startT = new Date();
        },
        handleTouchMove(event) {
            console.log('touch move');
            let curX = event.touches[0].clientX;
            let curY = event.touches[0].clientY;
            console.log('deltaX:', Math.abs(curX - this.startX), 'deltaY:', Math.abs(curY - this.startY));
            if (!this.scrollX && !this.scrollY) {
                if (this.x !== 0 || Math.abs(curX - this.startX) >= Math.abs(curY - this.startY)) {
                    console.log('set scroll X');
                    this.scrollX = true;
                } else {
                    console.log('set scroll Y');
                    this.scrollY = true;
                }
            } else if (this.scrollX) {
                console.log('scrollx');
                this.x = this.oldX + curX - this.startX;
            } else if (this.scrollY) {
                console.log('scrolly');
            }
        },
        handleTouchEnd(event) {
            console.log(event);
            if (this.scrollX) {
                this.scrollX = false;
                let velocity = this.x / (new Date() - this.startT);
                if (this.x < uni.upx2px(-750 * 0.75) || velocity < -0.5) {
                    this.handleScrollX(1);
                    this.$store.commit('switchMonth', 1);
                } else if (this.x > uni.upx2px(750 * 0.75) || velocity > 0.5) {
                    this.handleScrollX(-1);
                    this.$store.commit('switchMonth', -1);
                } else if (this.x !== 0) this.handleScrollX(0);
            } else if (this.scrollY) {
                this.scrollY = false;
                let curY = event.changedTouches[0].clientY;
                this.handleScrollY(curY < this.startY ? -1 : 1);
            } else {
                console.log('Nothing scrolling...');
                if (this.x !== 0) this.handleScrollX(0);
            }
        }
    },
    computed: {
        year() {
            return this.$store.state.c.year;
        },
        month() {
            return this.$store.state.c.month;
        },
        left() {
            return this.x - uni.upx2px(750) + 'px';
        },
        weekHeight() {
            if (this.showDetail) return '160rpx';
            else return '100rpx';
        },
        weekDetailHeight() {
            if (this.showDetail) return '60rpx';
            else return 0;
        }
    },
    mounted() {
        uni.$on('select-today', () => {
            this.selectDate(this.$store.state.c.todayObj);
        });

        this.$http.post({ url: '/api/get-schedules', name: '获取日程' }).then(data => {
            console.log('schedules:', data);
            for (schedule of data) {
                console.log(schedule);
            }
        });
    },
    beforeDestroy() {
        uni.$off('select-today');
    },
    onPageScroll() {
        console.log('scroll');
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

.one-week-days {
    display: flex;
    justify-content: space-evenly;
    height: $day-block-width;
}

.scroll-over-animation {
    left: -750upx !important;
    transition: left 0.3s ease-out;
}

.one-week {
    height: $day-block-width;
    margin: 10upx 0;
    transition: height 0.3s;
}

.one-week-detail {
    transition: height 0.3s;
}
</style>