<template>
    <Notification
            :textSize="textSize"
            icon="mdi-alert-circle"
            color="red"
            @closeNotification="closeNotification()"
            @click="click()"
            :ripple="clickable"
    >
        <strong>{{date}}</strong>: {{serialNumber}} failed.
    </Notification>
</template>
<script>
    import Notification from "@/components/Notification";
    export default {
        props:{
            serialNumber: String,
            date: String,
            textSize: {
                type: String,
                default: 'medium'
            },
            clickable: {
                type: Boolean,
                default: false,
            }
        },
        components: {
            Notification
        },
        methods:{
            closeNotification () {
                this.$emit('closeNotification')
            },
            click () {
                if (this.clickable) {
                    console.log('got to notiication')
                    this.$emit('click')
                }
            }
        },
    }
</script>
