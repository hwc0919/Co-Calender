<template>
    <div>
        <span v-for="(tag, ind) in wdTags" :key="`tag-${ind}`">{{ tag }}</span>
    </div>
</template>

<script>
export default {
    name: 'WdHeader',
    data() {
        return {
            wdTags: ['日', '一', '二', '三', '四', '五', '六']
        };
    }
};
</script>

<style lang="scss" scoped>
div {
    display: flex;
    justify-content: space-evenly;
    padding: 10upx;
    color: gray;
}

span {
    display: inline-block;
    width: $day-cell-width;
    font-size: 24upx;
}
</style>