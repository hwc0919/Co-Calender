<template>
    <form>
        <label for="username">用户名</label>
        <input id="username" type="text" v-model.trim="username" placeholder="用户名" />
        <label for="password">密码</label>
        <input id="password" type="password" v-model.trim="password" placeholder="密码" />
        <label for="test">test</label>
        <input id="test" type="checkbox" />
        <button type="button" @click="handleSubmit"></button>
    </form>
</template>

<script>
export default {
    data() {
        return {
            username: '',
            password: ''
        };
    }
};
</script>

<style>
</style>