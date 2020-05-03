<script>
export default {
    data: {},
    onLaunch: function() {
        this.$store.commit('initCalendar');
        uni.getStorage({
            key: 'user',
            success: res => {
                console.log('read user from storage', res.data);
                this.$store.commit('setUser', res.data);
            }
        });
        console.log('App Launch');
        console.log(this.$store.state.c.year);
    },
    onShow: function() {
        console.log('App Show');
    },
    onHide: function() {
        console.log('App Hide');
    }
};
</script>

<style lang="scss">
/*每个页面公共css */
html,
body {
    background-color: $uni-bg-color-grey;
    box-sizing: border-box;
}

input {
    box-sizing: border-box;
}
</style>