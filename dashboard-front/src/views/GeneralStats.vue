<template>
    <v-content>
        <v-container fluid >
            <v-row dense>
                <v-col cols="12">
                    <MainCard title="Failure evolution" icon="mdi-chart-timeline-variant">
                        <FailureHistory height="100"/>
                    </MainCard>
                </v-col>
            </v-row>
            <v-row dense>
                <v-col cols="12">
                    <StatusCard :items="items" title="Full Data"></StatusCard>
                </v-col>
            </v-row>
        </v-container>
        <v-btn
                bottom
                color="#80DEEA"
                light
                fab
                fixed
                right
                @click="dialog = !dialog"
        >
            <v-icon>mdi-filter</v-icon>
        </v-btn>
        <FilterDialog v-model="dialog"/>
    </v-content>
</template>
<script>
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