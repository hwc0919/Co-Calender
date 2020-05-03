<template>
    <div
        :class="[
            'day-block',
            { 'other-month-day': !inThisMonth, 'select-day': selected, 'select-today': selected && isToday }
        ]"
    >
        <span class="hasSchedule"></span>
        <span class="date">{{ dateObj.day }}</span>
        <span class="lunar"></span>
    </div>
</template>

<script>
import { DateObj } from '../../static/js/DateObj';
export default {
    name: 'DayBlock',
    props: ['dateObj', 'month'],
    methods: {},
    computed: {
        selected() {
            return this.$store.state.c.day === this.dateObj.day && this.$store.state.c.month === this.dateObj.month;
        },
        isToday() {
            return this.dateObj.equals(new DateObj(new Date()));
        },
        inThisMonth() {
            return this.dateObj.month === this.month;
        }
    }
};
</script>

<style lang="scss" scope>
.day-block {
    display: flex;
    justify-content: flex-start;
    flex-direction: column;
    border-radius: 50%;
    width: $day-block-width;
    height: $day-block-height;
}

.day-block span {
    display: inline-block;
}

.day-block span:nth-child(1) {
    flex: 2;
}

.day-block span:nth-child(2) {
    flex: 3;
}

.day-block span:nth-child(3) {
    flex: 3;
}

.select-day {
    background-color: $color-city-light;
}

.select-today {
    background-color: $uni-color-primary !important;
    color: white;
}

.other-month-day {
    color: $color-shooting-breeze;
}
</style>