<template>
    <view class="content">
        <image class="logo" src="/static/logo.png"></image>
        <head-menu></head-menu>
        <view>
            <text class="title">{{title}}</text>
        </view>
    </view>
</template>

<script>
    import HeadMenu from '@/pages/header/HeadMenu';

    export default {
        components: {
            'head-menu': HeadMenu
        },
        data() {
            return {
                title: 'Hello'
            }
        },
        onLoad() {

        },
        methods: {

        }
    }
</script>

<style>
    .content {
        text-align: center;
        height: 400upx;
    }

    .logo {
        height: 200upx;
        width: 200upx;
        margin-top: 200upx;
    }

    .title {
        font-size: 36upx;
        color: #8f8f94;
    }
</style>