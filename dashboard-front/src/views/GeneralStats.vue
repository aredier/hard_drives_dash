<template>
    <v-content>
        <v-container fluid >
            <v-row dense>
                <v-col cols="12">
                    <MainCard
                            title="Failure Evolution"
                            icon="mdi-chart-timeline-variant"
                            :isLoading="groupedDataLoading"
                            tooltip="Evolution of the actual number of failures per day. This graph will adapt to reflect the filters you set."
                    >
                        <FailureHistory height="100"/>
                    </MainCard>
                </v-col>
            </v-row>
            <v-row dense>
                <v-col cols="12">
                    <StatusCard
                            :items="items"
                            title="Last 1000 Data Points"
                            tooltip="Latest hard statuses of the hard drive you have selected through the filters"
                            :isLoading="hard_drive_statuses_loading"/>
                </v-col>
            </v-row>
            <v-btn
                    top
                    color="#80DEEA"
                    light
                    fab
                    fixed
                    right
                    @click="dialog = !dialog"
                    style="margin-top: 75px;"
            >
                <v-icon>mdi-filter</v-icon>
            </v-btn>
            <FilterDialog v-model="dialog"/>
        </v-container>
    </v-content>
</template>
<script>
    import { mapState } from 'vuex'
    import StatusCard from "@/components/StatusCard";
    import FailureHistory from "@/components/FailureHistory";
    import FilterDialog from "@/components/FilterDialog";
    import MainCard from "@/components/MainCard";

    export default {
        data () {
            return {
                sortValue: "date-time",
                sortDesc: true,
                dialog: false,

            }

    },
        components: {
            FailureHistory,
            StatusCard,
            FilterDialog,
            MainCard,
        },
        computed: {
            ...mapState(['groupedDataLoading', 'hard_drive_statuses_loading']),
            items (){
                var res = this.$store.state.hard_drive_statuses.filter((item) => {
                    return item['failure_probability'] > this.$store.state.filters.probaRange[0]
                }).filter((item) => {
                    return item['failure_probability'] < this.$store.state.filters.probaRange[1]
                }).map((item) =>{
                    item['capacity_bytes'] = this.humanFileSize(item['capacity_bytes'])
                    return item
                });
                if (this.$store.state.filters.selectedModels.length > 0){
                    res = res.filter((item) => {
                        return this.$store.state.filters.selectedModels.includes(item.model)
                    })
                }
                if (!this.$store.state.filters.selectNominal){
                    res = res.filter((item) => {
                        return item.failure_probability > 0.5 || item.failure == 1
                    })
                }
                if (!this.$store.state.filters.selectWarnings) {
                    res = res.filter((item) => item.failure_probability < 0.5)
                }
                if (!this.$store.state.filters.selectFailures) {
                    res = res.filter((item) => item.failure == 0)
                }
                return res
            },
        },
        methods: {
            updateItems (number) {
                this.$store.dispatch('updateStatuses', number);
            },
            humanFileSize(bytes) {
                var thresh = 1000;
                if(Math.abs(bytes) < thresh) {
                    return bytes + ' B';
                }
                var units = ['kB','MB','GB','TB','PB','EB','ZB','YB']
                var u = -1;
                do {
                    bytes /= thresh;
                    ++u;
                } while(Math.abs(bytes) >= thresh && u < units.length - 1);
                return bytes.toFixed(1)+' '+units[u];
            }
        },
    }

</script>