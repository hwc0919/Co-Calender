<template>
    <form ref="loginForm">
        <label for="username">用户名</label>
        <input id="username" v-model.trim="username" placeholder="用户名" />
        <label for="password">密码</label>
        <input id="password" password="true" v-model="password" placeholder="密码" />
        <button type="button" @click="handleLoginSubmit">登录</button>
    </form>
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
            uni.request({
                url: '/api/auth/login',
                method: 'POST',
                timeout: 3000,
                data: this.formData,
                header: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                dataType: 'json',
                success: res => {
                    console.log('success');
                    console.log(res);
                    console.log(res.data);
                    // this.$store.commit('setUsername', res.data.username);
                },
                fail: err => {
                    console.log('error');
                    console.log(err);
                },
                complete: arg => {
                    console.log('complete');
                    console.log(arg);
                }
            });
        }
    }
};
</script>

<style>
</style>