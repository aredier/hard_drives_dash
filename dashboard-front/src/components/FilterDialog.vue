<template>
    <v-dialog
            :value="value"
            width="800px"
            @click:outside="updateDialog(false)"
    >
        <v-card>
            <v-card-title class="grey darken-2">
                Update Filters
            </v-card-title>
            <v-container>
                <v-row align="center" justify="center">
                    <v-col cols="11">
                        <v-autocomplete
                                v-model="selectedModels"
                                :items="models"
                                filled
                                outlined
                                dense
                                chips
                                color="#80DEEA"
                                item-color="#80DEEA"
                                label="Hard Drive Models"
                                item-text="name"
                                item-value="name"
                                multiple
                        >
                            <template v-slot:selection="data">
                                <v-chip
                                        v-bind="data.attrs"
                                        :input-value="data.selected"
                                        close
                                        @click="data.select"
                                        @click:close="remove(data.item)"
                                >
                                    {{ data.item.name }}
                                </v-chip>
                            </template>
                            <template v-slot:item="data">
                                <template>
                                    <v-list-item-content>
                                        <v-list-item-title v-html="data.item.name"></v-list-item-title>
                                    </v-list-item-content>
                                </template>
                            </template>
                        </v-autocomplete>
                    </v-col>
                </v-row>
                <v-row align="center" justify="center">
                    <v-col cols="11">
                        <v-subheader class="pl-0 mb-5">failure probability prediction</v-subheader>
                        <v-range-slider
                                v-model="slider"
                                thumb-label="always"
                                thumb-size="27"
                                max=1
                                min=0
                                step="0.01"
                                color="#80DEEA"
                        ></v-range-slider>
                    </v-col>
                </v-row>
                <v-row align="center" justify="center">
                    <v-subheader style="margin-bottom: 15px;">Hard Drive Status: </v-subheader>
                <v-col cols="2">
                        <v-switch v-model="selectFailures" class="ma-2" label="Failure" color="#80DEEA"></v-switch>
                    </v-col>
                    <v-col cols="2">
                        <v-switch v-model="selectWarnings" class="ma-2" label="Warning" color="#80DEEA"></v-switch>
                    </v-col>
                    <v-col cols="2">
                        <v-switch v-model="selectNominal" class="ma-2" label="Nominal" color="#80DEEA"></v-switch>
                    </v-col>
                </v-row>
            </v-container>
            <v-card-actions>
                <v-spacer />
                <v-btn
                        text
                        color="#80DEEA"
                        @click="updateDialog(false)"
                >Cancel</v-btn>
                <v-btn
                        text
                        @click="updateDialog(true)"
                >Apply</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>
<script>

    export default {
        data () {
            return {
                models: this.$store.state.allModels.map((item) => {return {name: item}}),
                selectedModels: [],
                slider: [0, 1],
                selectNominalselectFailures: true,
                selectFailures: true,
                selectWarnings: true,
                selectNominal: true,
            }
        },
        props: {
            'value': Boolean,
        },
        methods: {
            updateDialog(applyFilters) {
                if (applyFilters) {
                    this.$store.dispatch('applyFilters', {
                        probaRange: this.slider,
                        selectedModels: this.selectedModels,
                        selectWarnings: this.selectWarnings,
                        selectFailures: this.selectFailures,
                        selectNominal: this.selectNominal,
                    });
                }
                this.$emit('input', false)
            },
            remove (item) {
                const index = this.selectedModels.indexOf(item.name);
                if (index >= 0) this.selectedModels.splice(index, 1)
            },
        },
        watch: {
            value: function()  {
                this.slider = this.$store.state.filters.probaRange;
            },

        },
        mounted() {
            this.slider = this.$store.state.filters.probaRange;
        }
    }
</script>