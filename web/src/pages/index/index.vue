<template>
    <view class="content">
        <head-menu :activeViewID="activeViewID" @switch-view="switchView($event)"></head-menu>
        <!-- <keep-alive>
            <component :is="activeView"></component>
        </keep-alive> -->

        <month-view v-if="activeViewID === 0"></month-view>
        <week-view v-else-if="activeViewID === 1"></week-view>
        <day-view v-else-if="activeViewID === 2"></day-view>

        <div class="corner-btn-group">
            <button
                v-show="!$store.state.selectDate.isToday()"
                @click="$store.commit('selectToday')"
                class="today-btn"
                type="primary"
            >
                今
            </button>
            <button class="create-btn" type="default">
                <uni-icons type="plusempty" size="30" color="$uni-color-primary"></uni-icons>
            </button>
        </div>
    </view>
</template>

<script>
import HeadMenu from '@/components/headers/HeadMenu';
import MonthView from '@/components/calendars/MonthView';
import WeekView from '@/components/calendars/WeekView';
import DayView from '@/components/calendars/DayView';
import ScheduleView from '@/components/calendars/ScheduleView';

export default {
    components: {
        HeadMenu,
        MonthView,
        WeekView,
        DayView
    },
    data() {
        return {
            activeViewID: 0,
            availViews: [MonthView, WeekView, DayView, ScheduleView]
        };
    },
    methods: {
        switchView(id) {
            this.activeViewID = id;
        }
    },
    computed: {
        activeView() {
            return this.availViews[this.activeViewID];
        }
    }
};
</script>

<style lang="scss" scope>
.content {
    text-align: center;
    height: 100%;
}

.corner-btn-group {
    position: absolute;
    display: flex;
    bottom: 40upx;
    right: 40upx;
}

.corner-btn-group button {
    width: 100upx;
    padding: 0;
    height: 100upx;
    text-align: center;
    border-radius: 50%;
    line-height: 100upx;
    font-size: 45upx;
    margin-left: 40upx;
}

.corner-btn-group button::after {
    border: none;
}

.today-btn {
    box-shadow: 0 0 5upx $uni-color-primary;
}

.create-btn {
    background-color: white;
    box-shadow: 0 0 5upx $uni-text-color-grey;
}
</style>