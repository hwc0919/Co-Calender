<template>
    <div class="header">
        <div class="header-1">
            <div class="left-info-group">
                <span class="year-month">{{ $store.state.curY }}年{{ $store.state.curM + 1 }}月</span>
                <span class="weekday">{{ $store.state.curWd | wd2str }}</span>
            </div>
            <div class="right-btn-group">
                <button @click="showViewMenu = !showViewMenu">视图</button>
                <button>工具</button>
            </div>
        </div>
        <transition name="slide-fade">
            <div class="view-menu" v-show="showViewMenu">
                <button
                    v-for="(name, index) in viewBtns"
                    :class="{ 'active-view': activeViewID === index }"
                    @click="$emit('switch-view', index)"
                    :key="`view-btn-${index}`"
                >
                    {{ name }}
                </button>
            </div>
        </transition>
    </div>
</template>

<script>
export default {
    name: 'HeadMenu',
    props: ['activeViewID'],
    data() {
        return {
            showViewMenu: false,
            viewBtns: ['月视图', '周视图', '日视图', '日程']
        };
    },
    methods: {},
    filters: {
        wd2str(day) {
            switch (day) {
                case 0:
                    return '周日';
                case 1:
                    return '周一';
                case 2:
                    return '周二';
                case 3:
                    return '周三';
                case 4:
                    return '周四';
                case 5:
                    return '周五';
                case 6:
                    return '周六';
            }
        }
    }
};
</script>

<style lang="scss" scoped>
.header {
    padding: 20upx 0;
}

.header-1 {
    display: flex;
    padding: 10upx 40upx;
    justify-content: space-between;
    align-items: center;
}

.year-month {
    font-size: 50upx;
    margin-right: 20upx;
}

.weekday {
    display: inline-block;
    width: 60upx;
    height: 30upx;
    line-height: 30upx;
    font-size: 24upx;
    background-color: $uni-bg-color-grey;
    padding: 6upx 12upx;
    border: 1upx solid gray;
    border-radius: 20upx;
}

button {
    width: 80upx;
    height: 60upx;
    line-height: 58upx;
    display: inline-block;
    font-size: 20upx;
    padding: 0;
}

.left-info-group {
    display: flex;
    justify-content: flex-start;
    align-items: center;
}

.right-btn-group {
    display: flex;
    justify-content: flex-start;
    align-items: center;
}

.right-btn-group button {
    margin-left: 20upx;
}

.slide-fade-enter-active {
    transition: all 0.5s ease;
}

.slide-fade-leave-active {
    transition: all 0.5s ease;
}

.view-menu {
    display: flex;
    transform-origin: top;
    padding: 10upx 80upx;
    justify-content: space-evenly;
}

.active-view {
    color: $uni-color-primary;
}

.slide-fade-enter,
.slide-fade-leave-to {
    transform: scaleY(0);
    opacity: 0;
}
</style>