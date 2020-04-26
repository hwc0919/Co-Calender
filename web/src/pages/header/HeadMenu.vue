<template>
    <div>
        <span class="year-month">{{curYear}}年{{curMonth}}月</span><span class="weekday">{{curWeekday}}</span>
        <button>视图</button>
        <button>工具</button>
    </div>
</template>

<script>
    export default {
        name: 'head-menu',
        data() {
            return {}
        },
        methods: {

        },
        computed: {
            curYear: () => new Date().getFullYear(),
            curMonth: () => new Date().getMonth(),
            curWeekday() {
                let day = new Date().getDay();
                switch (day) {
                    case 0: return '周日';
                    case 1: return '周一';
                    case 2: return '周二';
                    case 3: return '周三';
                    case 4: return '周四';
                    case 5: return '周五';
                    case 6: return '周六';
                }
            }
        }
    }
</script>

<style lang="scss" scoped>
    .year-month {
        font-size: 50upx;
    }

    .weekday {
        font-size: 30upx;
        line-height: 30upx;
        background-color: $uni-bg-color-grey;
    }
</style>