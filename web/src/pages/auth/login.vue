<template>
    <div class="login-view-wrapper">
        <form class="login-form" ref="loginForm">
            <div class="input-group">
                <label for="username">用户名</label>
                <input id="username" v-model.trim="username" placeholder="用户名" />
            </div>
            <div class="input-group">
                <label for="password">密码</label>
                <input id="password" password="true" v-model="password" placeholder="密码" />
            </div>
            <button type="button" @click="handleLoginSubmit">登录</button>
        </form>
        <navigator class="navi" url="/pages/auth/register" open-type="navigate" hover-class="other-navigator-hover">
            没有账号?注册一个!
        </navigator>
    </div>
</template>

<script>
export default {
    data() {
        return {
            username: '',
            password: ''
        };
    },
    computed: {
        formData() {
            return {
                username: this.username,
                password: this.password
            };
        }
    },
    methods: {
        handleLoginSubmit() {
            this.$http
                .post({
                    url: '/api/auth/login',
                    timeout: 3000,
                    data: this.formData
                })
                .then(data => {
                    console.log('then', data);
                    this.$store.commit('login', { login: true, username: data.username, uid: data.uid });
                    uni.navigateTo({ url: '/pages/index/index' });
                })
                .catch(msg => {
                    console.log('catch', msg);
                });
        }
    }
};
</script>

<style lang="scss" scoped>
@import './form.scss';

.login-view-wrapper {
    padding: 50upx;
}
</style>