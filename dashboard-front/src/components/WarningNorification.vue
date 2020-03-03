<template>
    <Notification
            :textSize="textSize"
            icon="mdi-alert-outline"
            color="orange"
            @closeNotification="closeNotification()"
            @click="click()"
            :ripple="clickable"
    >
        <strong>{{date}}</strong>: {{serialNumber}} expected to fail <strong>tomorrow</strong> with {{Math.round(proba * 100)}}% probability
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
            proba: {
                type: Number,
                required: true,
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
                console.log('bar')
                if (this.clickable) {
                    console.log('got to notiication')
                    this.$emit('click')
                }
            }
        },
}
</script>