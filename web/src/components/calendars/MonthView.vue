<template>
    <div class="month-view-wrapper">
        <week-header></week-header>
        <div
            id="month"
            ref="month"
            :class="['month-view-content', { 'scroll-over-animation': scrollOver }]"
            @touchstart="handleTouchStart"
            @touchmove="handleTouchMove"
            @touchend="handleTouchEnd"
            :style="{ left: left }"
        >
            <div class="one-month" v-for="calendar in calendars" :key="`calendar-${calendar[1][0].month}`">
                <div v-for="(week, ind1) in calendar" :key="`calendar-${calendar[1][0].month}-${ind1}`">
                    <div class="one-week">
                        <day-block
                            v-for="(dateObj, ind2) in week"
                            :key="`calendar-${calendar[1][0].month}-${ind1}-${ind2}`"
                            :dateObj="dateObj"
                            :month="calendar[1][0].month"
                            @click.native="selectDate(dateObj)"
                        >
                        </day-block>
                    </div>
                    <div class="one-week-detail"></div>
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
                this.$store.getters.getMonthCalendar(this.$store.state.year, this.$store.state.month - 1),
                this.$store.getters.getMonthCalendar(this.$store.state.year, this.$store.state.month),
                this.$store.getters.getMonthCalendar(this.$store.state.year, this.$store.state.month + 1)
            ],
            query: query,
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
        resetCalendar() {
            if (this.calendars[1][1][0].month !== this.$store.state.month) {
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
                this.finishSlide(1);
                this.$store.commit('selectDate', dateObj);
            }
            // Select date of previous month
            else if (
                (this.year === dateObj.year && this.month === dateObj.month + 1) ||
                (this.year === dateObj.year + 1 && this.month === 0 && dateObj.year === 11)
            ) {
                this.finishSlide(-1);
                this.$store.commit('selectDate', dateObj);
            } else {
                this.$store.commit('selectDate', dateObj);
                this.resetCalendar();
            }
        },

        /* **************************************** */
        /*             Handle Scroll                */
        /* **************************************** */
        handleTouchStart(event) {
            clearTimeout(this.timeout);
            this.query
                .boundingClientRect(data => {
                    this.x = data.left + uni.upx2px(750);
                })
                .exec();
            this.scrollOver = false;
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
            if (this.dragging) {
                this.dragging = false;
                let velocity = this.x / (new Date() - this.startT);
                if (this.x < uni.upx2px(-750 * 0.75) || velocity < -0.5) {
                    this.finishSlide(1);
                    this.$store.commit('switchMonth', 1);
                } else if (this.x > uni.upx2px(750 * 0.75) || velocity > 0.5) {
                    this.finishSlide(-1);
                    this.$store.commit('switchMonth', -1);
                } else if (this.x !== 0) {
                    this.finishSlide(0);
                }
            }
        }
    },
    computed: {
        year() {
            return this.$store.state.year;
        },
        month() {
            return this.$store.state.month;
        },
        left() {
            return this.x - uni.upx2px(750) + 'px';
        }
    },
    mounted() {
        uni.$on('select-today', () => {
            this.selectDate(this.$store.state.todayObj);
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

.one-week {
    display: flex;
    justify-content: space-evenly;
    padding: 10upx 0;
}

.scroll-over-animation {
    left: -750upx !important;
    transition: left 0.3s ease-out;
}

.one-week-detail {
    height: 100upx;
    background-color: $color-city-light;
}
</style>