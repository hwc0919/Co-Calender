<template>
    <view class="content">
        <!-- HeadMenu, show year, month, dayOfWeek and sub-menus -->
        <head-menu
            class="head-menu"
            :activeViewID="activeViewID"
            @switch-view="switchView($event)"
            @show-drawer="showDrawer"
        ></head-menu>

        <!-- Uni-app does not support `keep-alive` or `v-is` -->
        <!-- <keep-alive>
            <component :is="activeView"></component>
        </keep-alive> -->
        <month-view class="calendar-view" v-if="activeViewID === 0"></month-view>
        <week-view class="calendar-view" v-else-if="activeViewID === 1"></week-view>
        <day-view class="calendar-view" v-else-if="activeViewID === 2"></day-view>

        <!-- Right drawer memu -->
        <uni-drawer ref="drawer" :mode="'right'" :width="160">
            <div class="uni-title" @click="handleUsernameClick">{{ $store.state.u.username }}</div>
        </uni-drawer>

        <!-- bottom-right button group -->
        <div class="corner-btn-group">
            <button v-show="!$store.getters.isToday" @click="uniEmitSelectToday" class="today-btn" type="primary">
                今
            </button>
            <button class="create-btn" type="default">
                <uni-icons type="plusempty" size="30" color="$uni-color-primary"></uni-icons>
            </button>
        </div>
    </view>
</template>

<script>
import HeadMenu from '@/components/menus/HeadMenu';
import MonthView from '@/components/calendars/MonthView';
import WeekView from '@/components/calendars/WeekView';
import DayView from '@/components/calendars/DayView';
import ScheduleView from '@/components/calendars/ScheduleView';
import uniDrawer from '@/components/uni-drawer/uni-drawer';

export default {
    components: {
        HeadMenu,
        MonthView,
        WeekView,
        DayView,
        uniDrawer
    },
    data() {
        return {
            activeViewID: 0,
            availViews: [MonthView, WeekView, DayView, ScheduleView]
        };
    },
    methods: {
        // Switch between calendar views
        switchView(id) {
            this.activeViewID = id;
        },
        // Emit global event `select-today`
        uniEmitSelectToday() {
            uni.$emit('select-today');
        },
        // Show right drawer menu
        showDrawer() {
            this.$refs.drawer.open();
        },
        // Navigate to login
        handleUsernameClick() {
            if (!this.$store.state.u.login) {
                console.log('redirect to login');
                uni.navigateTo({
                    url: '/pages/auth/login'
                    // TODO: Add animation
                });
            } else {
                console.log('already login');
            }
        }
    },
    computed: {
        // activeView() {
        //     return this.availViews[this.activeViewID];
        // }
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