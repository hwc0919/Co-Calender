<template>
    <div class="register-view-wrapper">
        <form class="register-form">
            <div class="input-group">
                <label for="username">用户名</label>
                <input id="username" v-model.trim="username" placeholder="用户名" />
            </div>
            <div class="input-group">
                <label for="password">密码</label>
                <input id="password" password="true" v-model="password" placeholder="密码" />
            </div>
            <button type="button" @click="handleRegisterSubmit">注册</button>
        </form>
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
        handleRegisterSubmit() {
            this.$http
                .post({
                    url: '/api/auth/register',
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

.register-view-wrapper {
    padding: 50upx;
}
</style>
