<template>
    <v-container fluid>
        <v-row >
            <v-col
                    cols="12"
                    style="padding:15px"
            >
                <v-card style="background-color: #212121" elevation="10">
                    <v-container fluid>
                        <v-row>
                            <v-col cols="1" style="text-align: center; font-weight: bold;">
                                <span>Last Status</span>
                                <Tooltip
                                    value="Reported status of the hard drive at this date. This can either be nominal, a warning when the drive is predicted to fail in the near future, or critical if the drive failed"/>
                            </v-col>
                            <v-col cols="2" style="text-align: center; font-weight: bold;">Update Date Time</v-col>
                            <v-col cols="2" style="text-align: center; font-weight: bold;">Serial Number</v-col>
                            <v-col cols="2" style="text-align: center; font-weight: bold;">Model</v-col>
                            <v-col cols="2" style="text-align: center; font-weight: bold;">Capacity</v-col>
                            <v-col cols="2" style="text-align: center; font-weight: bold;">
                                <span>Failure Probability</span>
                                <Tooltip
                                        value="Probability of the drive failing in the near future as predicted by our model"/>
                            </v-col>
                            <v-col cols="1" style="text-align: center;"></v-col>
                        </v-row>
                    </v-container>
                </v-card>
            </v-col>
        </v-row>
        <v-data-iterator
                :items="items"
                :items-per-page.sync="itemsPerPage"
                :page="page"
                :sort-by="sortBy"
                :sort-desc="sortDesc"
                hide-default-footer
        >

            <template v-slot:default="props">
                <ChipRow
                        v-for="item in props.items"
                        :key="item.name"
                >

                    <v-col cols="1" style="text-align: center">
                        <v-icon
                                v-if="item['failure'] == 1"
                                color="red"
                        >mdi-alert-circle</v-icon>
                        <v-icon v-else-if="item['failure_probability'] > 0.5" color="orange">
                            mdi-alert-outline
                        </v-icon>
                        <v-icon
                                v-else
                                color="green"
                        >mdi-check-circle</v-icon>
                    </v-col>
                    <v-col
                            v-for="(key, index) in filteredKeys"
                            :key="index"
                            style="text-align: center"
                            cols="2"
                    >
                        <v-container fluid style="padding: 0px;">
                            <v-row align="center" justify="center">
                                <div>
                                    {{ item[key.toLowerCase()] }}
                                </div>
                                <v-btn
                                        v-if="['serial_number', 'model'].includes(key)"
                                        icon style="margin-left: 10px;"
                                        @click="copyToClipboard(item[key.toLowerCase()])"
                                >
                                    <v-icon>mdi-content-copy</v-icon>
                                </v-btn>
                            </v-row>
                        </v-container>
                    </v-col>
                    <v-col cols="1" style="text-align: center;">
                        <v-btn icon @click="goToInDepth(item.serial_number)">
                            <v-icon>mdi-import</v-icon>
                        </v-btn>
                    </v-col>

                </ChipRow>
            </template>

            <template v-slot:footer>
                <v-row class="mt-2" align="center" justify="center"
                       style="padding-left: 50px; padding-right: 50px;">
                    <span class="grey--text">Items per page</span>
                    <v-menu offset-y>
                        <template v-slot:activator="{ on }">
                            <v-btn
                                    dark
                                    text
                                    class="ml-2"
                                    v-on="on"
                            >
                                {{ itemsPerPage }}
                                <v-icon>mdi-chevron-down</v-icon>
                            </v-btn>
                        </template>
                        <v-list>
                            <v-list-item
                                    v-for="(number, index) in itemsPerPageArray"
                                    :key="index"
                                    @click="updateItemsPerPage(number)"
                            >
                                <v-list-item-title>{{ number }}</v-list-item-title>
                            </v-list-item>
                        </v-list>
                    </v-menu>

                    <v-spacer></v-spacer>

                    <span
                            class="mr-4
            grey--text"
                    >
            Page {{ page }} of {{ numberOfPages }}
          </span>
                    <v-btn
                            fab
                            dark
                            class="mr-1"
                            @click="formerPage"
                    >
                        <v-icon>mdi-chevron-left</v-icon>
                    </v-btn>
                    <v-btn
                            fab
                            dark
                            class="ml-1"
                            @click="nextPage"
                    >
                        <v-icon>mdi-chevron-right</v-icon>
                    </v-btn>
                </v-row>
            </template>
        </v-data-iterator>
        <input type="text" value="foo" id="clipboard"
               style="opacity: 0.1; height:0;position:absolute;z-index: -1;">
        <v-snackbar
                v-model="snackbar"
        >
            {{snackContent}} copied to clipboard
            <v-btn
                    text
                    @click="snackbar = false"
            >
                Close
            </v-btn>
        </v-snackbar>
    </v-container>
</template>
<script>
    import router from "@/router";
    import ChipRow from "@/components/ChipRow";
    import Tooltip from "@/components/Tooltip";

    export default {
        components: {
            ChipRow,
            Tooltip
        },
        data () {
            return {
                itemsPerPageArray: [5, 10, 25],
                filter: {},
                page: 1,
                itemsPerPage: 5,
                snackbar: false,
                snackContent: "",
                keys: [
                    'date',
                    'serial_number',
                    'model',
                    'capacity_bytes',
                    'failure',
                    'failure_probability'
                ],
            }
        },
        props: {
            'sortByName': String,
            'sortDesc': Boolean,
            items: {
                default: []
            }
        },
        computed: {
            sortBy () {
                if(this.sortByName == 'date-time') {
                    return 'date'
                } else if (this.sortByName == 'failure probability') {
                    return 'failure_probability'
                }
                return "foo"

            },

            numberOfPages () {
                return Math.ceil(this.items.length / this.itemsPerPage)
            },
            filteredKeys () {
                return this.keys.filter(key => key != 'failure')
            },
        },
        methods: {
            goToInDepth (serialNumber) {
                router.push('/in-depth-analysis/' + serialNumber)
            },
            nextPage () {
                if (this.page + 1 <= this.numberOfPages) this.page += 1
            },
            formerPage () {
                if (this.page - 1 >= 1) this.page -= 1
            },
            updateItemsPerPage (number) {
                this.itemsPerPage = number
            },
            copyToClipboard(text){
                var copyText = document.getElementById("clipboard");
                copyText.value = text;

                /* Select the text field */
                copyText.select();
                copyText.setSelectionRange(0, 99999); /*For mobile devices*/

                /* Copy the text inside the text field */
                document.execCommand("copy");
                this.snackContent = text;
                this.snackbar = true;
            },
        },
    }
</script>