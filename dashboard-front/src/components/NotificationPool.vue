<template>
    <v-container style="overflow-y: scroll; overflow-x: hidden;"
                 class="no-scroll" fluid>
        <template v-for="notification in sortedNotifications">
            <WarningNorification
                    :key="notification.id"
                    v-if="notification.type == 'prediction-warning'"
                    :serialNumber="notification.serial"
                    :date="notification.date"
                    :textSize="textSize"
                    :proba="notification.proba"
                    :clickable="clickable"
                    @closeNotification="closeNotification(notification)"
                    @click="goToInDepth(notification.serial)"
            />
            <ErrorNotification
                    :key="notification.id"
                    v-else
                    :serialNumber="notification.serial"
                    :date="notification.date"
                    :textSize="textSize"
                    :clickable="clickable"
                    @closeNotification="closeNotification(notification)"
                    @click="goToInDepth(notification.serial)"
            />


        </template>
    </v-container>
</template>
<script>
    import router from "@/router";
    import WarningNorification from "@/components/WarningNorification";
    import ErrorNotification from "@/components/ErrorNotification";

    export default {
        components: {
            WarningNorification,
            ErrorNotification,

        },
        props: {
            notifications: {
                required: true
            },
            textSize: {
                type: String,
                default: 'medium'
            },
            clickable: {
                type: Boolean,
                default: false,
            }
        },
        computed: {
            sortedNotifications () {
                let sortedNotifications = this.notifications;
                sortedNotifications.sort((a, b) => a.date > b.date? -1:1)
                return sortedNotifications
            }
        },
        methods: {
            closeNotification (notification){
                this.$store.dispatch("popNotification", (notification))
            },
            goToInDepth (serialNumber) {
                console.log('got to pool')
                router.push('/in-depth-analysis/' + serialNumber)
            },
        }
    }
</script>