<template>
<body>
<div id="vueBox">
    <button v-on:click="destoryMsg">销魂两兄弟组件的信息交互</button>
    <my-tag1></my-tag1>
    <my-tag2></my-tag2>

</div>
</body>
</template>

<script type="text/javascript">
import Vue from 'vue'
    // 信息中心 - 媒介
    var msgCenter = new Vue();

    Vue.component("my-tag1", {
        template: "<div><p>tag1的num：{{num}}</p><button v-on:click='handle'>数字增加</button></div>",
        data: function () {
            return {
                num: 0
            }
        },
        methods: {
            handle: function () {
                // 向信息中心发送tag1-event事件
                msgCenter.$emit("tag1-event", 20)
            }
        },
        mounted: function () {
            // 信息中心在这里进行执行监听tag2-event事件
            msgCenter.$on("tag2-event", (val) => {
                this.num = this.num + val;
            })
        }
    })


    Vue.component("my-tag2", {
        template: "<div><p>tag2的num：{{num}}</p><button v-on:click='handle'>数字增加</button></div>",
        data: function () {
            return {
                num: 0
            }
        },
        methods: {
            handle: function () {
                msgCenter.$emit("tag2-event", 10)
            }
        },
        mounted: function () {
            msgCenter.$on("tag1-event", (val) => {
                this.num = this.num + val;
            })
        }
    })


</script>