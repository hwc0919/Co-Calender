<template>
    <div :class="['header', { 'header-animation': showViewMenu }]">
        <div class="header-1">
            <div class="left-info-group">
                <span class="year-month"> {{ $store.state.c.year }}年{{ $store.state.c.month + 1 }}月 </span>
                <span class="day-diff">{{ info }}</span>
            </div>
            <div class="right-btn-group">
                <span><uni-icons type="list" size="24" @click="showViewMenu = !showViewMenu"></uni-icons></span>
                <span><uni-icons type="more-filled" size="24" @click="$emit('show-drawer')"></uni-icons></span>
            </div>
        </div>
        <div :class="['view-menu', { 'view-menu-animation': showViewMenu }]">
            <button
                v-for="(name, index) in viewBtns"
                :class="{ 'active-view': activeViewID === index }"
                @click="$emit('switch-view', index) && (showViewMenu = false)"
                :key="`view-btn-${index}`"
            >
                {{ name }}
            </button>
        </div>
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
    methods: {
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
    },
    computed: {
        info() {
            let year = this.$store.state.c.year;
            let month = this.$store.state.c.month;
            let day = this.$store.state.c.day;

            let dayDiff = Math.floor((new Date(year, month, day) - this.$store.state.c.today) / 86400000);
            if (dayDiff > 0) {
                return `${dayDiff}天后`;
            } else if (dayDiff < 0) {
                return `${Math.abs(dayDiff)}天前`;
            }
            return this.wd2str(new Date().getDay());
        }
    }
};
</script>

<style lang="scss" scoped>
.header {
    height: 140upx;
    width: 100%;
    padding: 40upx;
    box-sizing: border-box;
    transform-origin: top;
    transition: all 0.3s ease;
}

.header-1 {
    height: 60upx;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.year-month {
    font-size: 50upx;
    margin-right: 20upx;
}

.day-diff {
    display: inline-block;
    height: 30upx;
    line-height: 30upx;
    font-size: 22upx;
    padding: 6upx 20upx;
    border-radius: 16upx;
    color: $color-american-river;
    background-color: $color-city-light;
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

.right-btn-group span {
    margin-left: 20upx;
}

.view-menu {
    height: 100upx;
    display: flex;
    justify-content: space-evenly;
    align-items: center;
    padding: 10upx;
    transform: scaleY(0);
    transform-origin: top;
    transition: all 0.3s ease;
}

.active-view {
    color: $uni-color-primary;
}

.view-menu-animation {
    transform: scaleY(1);
}

.header-animation {
    height: 240upx;
}
</style>