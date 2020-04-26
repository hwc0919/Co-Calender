<template>
    <view class="content">
        <head-menu :activeViewID="activeViewID" @switch-view="switchView($event)"></head-menu>
        <keep-alive>
            <component :is="activeView"></component>
        </keep-alive>
    </view>
</template>

<script>
import HeadMenu from '../Header/HeadMenu';
import MonthView from '../CalanderViews/MonthView';
import WeekView from '../CalanderViews/WeekView';
import DayView from '../CalanderViews/DayView';
import ScheduleView from '../CalanderViews/ScheduleView';

export default {
    components: {
        HeadMenu,
        MonthView,
        WeekView,
        DayView
    },
    data() {
        let today = new Date();
        let curY = today.getFullYear();
        let curM = today.getMonth();
        let curD = today.getDate();
        let curWd = today.getDay();

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

<style>
.content {
    text-align: center;
    height: 400upx;
}

.logo {
    height: 200upx;
    width: 200upx;
    margin-top: 200upx;
}

.title {
    font-size: 36upx;
    color: #8f8f94;
}
</style>