<template>
    <v-content>
        <v-container fluid v-if="!isEmpty">
            <v-row>
                <v-col cols="4">
                    <MainCard
                            :title="notificationTitle"
                            icon="mdi-bell"
                            style="height: 400px;"
                            :isLoading="targetSerialLoading"
                            loadingColor="#FF8A65"
                            tooltip="Past notifications concerning this hard drive"
                    >
                        <NotificationPool :notifications="filterdNotifications"/>
                    </MainCard>
                </v-col>
                <v-col cols="8" >
                    <MainCard
                            title="Past Prediction"
                            icon="mdi-chart-timeline-variant"
                            style="height: 400px;"
                            :isLoading="targetSerialLoading"
                            loadingColor="#FF8A65"
                            tooltip="Past failure predictions. For each day the probability of failure for the next day is outputed."
                    >
                        <template>
                            <div style="position: relative; height: 340px;">
                                <ProbaHistory :history="predictionHistory" style="position: relative; height: 340px;"></ProbaHistory>
                            </div>
                        </template>
                    </MainCard>
                </v-col>
            </v-row>
            <v-row dense>
                <v-col cols="12">
                    <StatusCard
                            :title="fullDataTitle"
                            :items="fullDataItems"
                            :isLoading="targetSerialLoading"
                            loadingColor="#FF8A65"
                    />
                </v-col>
            </v-row>
        </v-container>
        <v-container fluid v-else>
            <v-row>
                <v-col>
                    <MainCard
                            title="Disk Choice" icon="mdi-magnify"
                            :loading="targetSerialLoading"
                    >
                        <v-container>
                            <v-row>
                                <v-card-subtitle>
                                    You need to choose the serial number of the disk you want to investigate. Alternatively you
                                    can click on the <v-icon>mdi-import</v-icon> icon in the overview
                                </v-card-subtitle>
                            </v-row>
                            <v-row dense>
                                <v-col cols="8" offset="2">
                                    <v-text-field
                                            label="Serial Number"
                                            single-line
                                            solo
                                            background-color="#757575"
                                            v-model="searchSerial"
                                            @keyup.enter="search()"
                                    ></v-text-field>
                                </v-col>
                            </v-row>
                            <v-row dense>
                                <v-col cols="6" offset="3">
                                    <v-btn block rounded @click="search()">
                                        Search
                                    </v-btn>
                                </v-col>
                            </v-row>
                        </v-container>
                    </MainCard>
                </v-col>
            </v-row>
        </v-container>
        <v-snackbar
                v-model="snackbar"
                top
                color="#FF8A65"
                style="color: #212121; font-weight: bold;"
        >
            {{this.$route.params.serial}} not found
            <v-btn
                    color="#212121"
                    text
                    @click="snackbar = false"
            >
                Close
            </v-btn>
        </v-snackbar>
    </v-content>
</template>

<script>
    import router from "@/router"
    import MainCard from "@/components/MainCard";
    import ProbaHistory from "@/components/ProbaHistory";
    import StatusCard from "@/components/StatusCard";
    import utils from '@/utils';
    import NotificationPool from "@/components/NotificationPool";
    import {mapState} from "vuex";

    export default {
        name: 'Home',
        components: {
            MainCard,
            ProbaHistory,
            StatusCard,
            NotificationPool,
        },
        data () {
            return {
                searchSerial: this.$route.params.serial == undefined ? "": this.$route.params.serial,
                snackbar: false,
            }
        },
        computed: {
            ...mapState(['targetSerialLoading']),
            notificationTitle() {
                return this.$route.params.serial + "'s Notifications"
            },

            fullDataTitle() {
                return this.$route.params.serial + "'s Full Data"
            },

            fullDataItems() {
                var res = this.$store.state.targetSerialStatuses.map((item) => {
                    item['capacity_bytes'] = utils.humanFileSize(item['capacity_bytes'])
                    return item
                });

                return res
            },

            predictionHistory () {
                return this.$store.state.targetSerialStatuses.map((el) =>{
                    return {
                        failure_probability: el.failure_probability,
                        date: el.date
                    }
                })
            },

            filterdNotifications () {
                return this.$store.state.notifications.filter((item) => item.serial == this.$route.params.serial)
            },

            isEmpty () {
                return !this.targetSerialLoading && ( this.$route.params.serial == undefined || this.fullDataItems.length == 0)
            }
        },
        methods: {
            search (){
                router.push('/in-depth-analysis/' + this.searchSerial)
            },
            getStatuses (){
                this.$store.commit('getTargetSerialStatuses', this.$route.params.serial)
                this.evaluateSnackbar()
            },
            evaluateSnackbar () {
                if (!this.targetSerialLoading) {
                    this.snackbar = this.$route.params.serial != undefined && this.fullDataItems.length == 0
                }
            }
        },
        watch: {
            $route () {
               this.getStatuses()
            },
            targetSerialLoading (value) {
                if (!value) {
                    this.evaluateSnackbar()
                }
            }
        },
        mounted() {
            this.getStatuses()
        }
    }
</script>
<style>

</style>
