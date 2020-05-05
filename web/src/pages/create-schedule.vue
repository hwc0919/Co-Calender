<template>
    <div>
        <div class="header">
            <navigator url="/pages/index/index">
                <button>X</button>
            </navigator>
            <h1>创建日程</h1>
            <button @click="createSchedule">√</button>
        </div>
        <form>
            <input type="text" v-model="title" placeholder="请输入事件标题" />
        </form>
    </div>
</template>


<script>
export default {
    name: 'CreateSchedule',
    data() {
        return {
            title: '',
            time: new Date()
        };
    },
    computed: {
        tableData() {
            return { title: this.title };
        }
    },
    methods: {
        createSchedule() {
            this.$http
                .post({
                    url: '/api/create',
                    data: { ...this.tableData, uid: this.$store.state.u.uid }
                })
                .then(res => {
                    uni.navigateTo({ url: '/pages/index/index' });
                });
        }
    }
};
</script>

<style lang="scss" scoped>
.header {
    display: flex;
    justify-content: space-between;
}

.header button {
    width: 100rpx;
    margin: 0;
}

.header button::after {
    border: none;
}

input {
    height: 100rpx;
    padding: 20rpx;
    margin: 40rpx;
    border: 1px sold gray;
    border-radius: 20rpx;
    background: $color-city-light;
}
</style>