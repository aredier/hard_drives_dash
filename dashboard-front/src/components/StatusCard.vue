<template>
    <MainCard :title="title" icon="mdi-table-large">
        <template v-slot:header>
            <span class="grey--text" v-if="hasNumberMenu">Items to display</span>
            <v-menu offset-y v-if="hasNumberMenu">
                <template v-slot:activator="{ on }">
                    <v-btn
                            dark
                            text
                            class="ml-2"
                            v-on="on"
                    >
                        {{ displayedStats }}
                        <v-icon>mdi-chevron-down</v-icon>
                    </v-btn>
                </template>
                <v-list>
                    <v-list-item
                            v-for="(number, index) in DisplayedStatsChoices"
                            :key="index"
                            @click="moreItems(number)"
                    >
                        <v-list-item-title>{{ number }}</v-list-item-title>
                    </v-list-item>
                </v-list>
            </v-menu>
            <v-spacer/>
            <v-select
                    flat
                    hide-details
                    dark
                    :items="['date-time', 'failure probability']"
                    label="sort by"
                    v-model="sortValue"
                    color="#757575"
                    item-color="#757575"
            ></v-select>
            <v-spacer/>
            <v-btn-toggle
                    v-model="sortDesc"
                    mandatory
            >
                <v-btn
                        large
                        depressed
                        :value="false"
                        @click="this.sortDesc = false"
                >
                    <v-icon>mdi-arrow-up</v-icon>
                </v-btn>
                <v-btn
                        large
                        depressed
                        :value="true"
                        @click="this.sortDesc = true"
                >
                    <v-icon>mdi-arrow-down</v-icon>
                </v-btn>
            </v-btn-toggle>
        </template>
        <StatusTable :sortByName="sortValue" :sortDesc="sortDesc" :items="items"/>
    </MainCard>
</template>
<script>
    import StatusTable from "@/components/StatusTable";
    import MainCard from "@/components/MainCard";

    export default {
        components: {
            StatusTable,
            MainCard,
        },
        data () {
            return {
                sortValue: "date-time",
                sortDesc: true,
                displayedStats: this.DisplayedStatsChoices[0],

            }

        },
        props:{
            DisplayedStatsChoices: {
                default: [],
            },
            items: {
                default: [],
            },
            title: {
                type: String,
                required: true
            }
        },
        computed: {
            hasNumberMenu () {
                return this.DisplayedStatsChoices.length > 0
            }
        },
        methods: {
            moreItems (number) {
                self.displayedStats = number;
                this.$emit('loadMore', {
                    number: number
                })
            }
        },
    }
</script>