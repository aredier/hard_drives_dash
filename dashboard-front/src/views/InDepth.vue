<template>
    <v-content>
        <v-container fluid>
            <v-row>
                <v-col cols="4">
                    <MainCard
                            :title="notificationTitle"
                            icon="mdi-bell"
                            style="height: 400px;"
                    >
                        <NotificationPool :notifications="filterdNotifications"/>
                    </MainCard>
                </v-col>
                <v-col cols="8" >
                    <MainCard
                            title="Past Prediction"
                            icon="mdi-chart-timeline-variant"
                            style="height: 400px;"
                    >
                        <template>
                            <div style="position: relative; height: 340px;">
                                <ProbaHistory style="position: relative; height: 340px;"></ProbaHistory>
                            </div>
                        </template>
                    </MainCard>
                </v-col>
            </v-row>
            <v-row dense>
                <v-col cols="12">
                    <StatusCard :title="fullDataTitle" :items="fullDataItems"></StatusCard>
                </v-col>
            </v-row>
        </v-container>
    </v-content>
</template>

<script>
    import MainCard from "@/components/MainCard";
    import ProbaHistory from "@/components/ProbaHistory";
    import StatusCard from "@/components/StatusCard";
    import utils from '@/utils';
    import NotificationPool from "@/components/NotificationPool";

    export default {
        name: 'Home',
        components: {
            MainCard,
            ProbaHistory,
            StatusCard,
            NotificationPool,
        },
        computed: {
            notificationTitle() {
                return this.$route.params.serial + "'s Notifications"
            },
            fullDataTitle() {
                return this.$route.params.serial + "'s Full Data"
            },
            fullDataItems() {
                var res = this.$store.state.hard_drive_statuses.filter((item) => {
                    return item.serial_number == this.$route.params.serial
                }).map((item) => {
                    item['capacity_bytes'] = utils.humanFileSize(item['capacity_bytes'])
                    return item
                });

                return res
            },
            filterdNotifications () {
                return this.$store.state.notifications.filter((item) => item.serial == this.$route.params.serial)
            }
        },
    }
</script>
<style>

</style>
