<template>
    <v-content>
        <v-container fluid>
            <v-row dense>
                <v-col cols="12">
                    <MainCard title="Test Performances" icon="mdi-history"
                              :isLoading="$store.state.trainingMetricsLoading">
                        <v-container fluid>
                            <v-row align="center" style="padding-left: 25px;">
                                <v-col cols="1" align="center" justify="center">
                                    <v-icon color="#BDBDBD" x-large>mdi-information-outline</v-icon>
                                </v-col>
                                <v-col cols="8">
                                    <v-card-subtitle>
                                        Test performance are obtained by splitting the training data temporally and evaluating
                                        model on the test set. The evolution of the performances show how the test
                                        performance evolved with retrains. You can than see how new data or changes on
                                        the model impact performance.
                                   </v-card-subtitle>
                                </v-col>
                            </v-row>
                            <v-row align="stretch" justify="center">
                                <v-col cols="4">
                                    <MainCard title="Performance Evolution" icon="mdi-chart-timeline-variant">
                                        <PerformanceGraph :inputData="performanceHistory" height="375"></PerformanceGraph>
                                    </MainCard>
                                </v-col>
                                <v-col cols="4">
                                    <MainCard style="height: 100%" title="Confusion Matrix" icon="mdi-table">
                                        <ConfusionMatrix :confusionMatrix="confusionMatrix"></ConfusionMatrix>
                                    </MainCard>
                                </v-col>
                                <v-col cols="4">
                                    <MainCard style="height: 100%;" title="Metrics" icon="mdi-speedometer">
                                        <v-list
                                                three-line
                                                style="background-color: #424242"
                                                dense
                                        >

                                            <v-list-item v-for="item in metrics" :key="item.name" style="padding-top: 2px; padding-bottom: 2px;">
                                                <v-list-item-content>
                                                    <v-list-item-title>
                                                        {{item.name}}:
                                                        <v-chip small>
                                                            <strong>{{item.value}}</strong>
                                                        </v-chip>
                                                    </v-list-item-title>
                                                    <v-list-item-subtitle>{{item.descritption}}</v-list-item-subtitle>
                                                </v-list-item-content>
                                            </v-list-item>
                                        </v-list>
                                    </MainCard>
                                </v-col>
                            </v-row>
                        </v-container>
                    </MainCard>
                </v-col>
            </v-row>
        </v-container>
    </v-content>
</template>
<script>
    import MainCard from "@/components/MainCard";
    import PerformanceGraph from "@/components/PerformanceGraph";
    import ConfusionMatrix from "@/components/ConfusionMatrix";
    export default {
        components:{
            MainCard,
            PerformanceGraph,
            ConfusionMatrix
        },
        data () {
            return {
                threshold: 0.05,
            }
        },
        computed: {
            performanceHistory () {
                let raw_history = this.$store.state.metrics.training.history
                return raw_history.sort((a, b) =>{
                    return a.date > b.date? 1: -1;
                }).map((el) => {
                    return {
                        date: el.date,
                        roc_score: el.roc_auc,
                        recall: el.recalls[0.05],
                        precision: el.precisions[0.005]
                    }
                })
            },
            testPerformanceData () {
                return this.$store.state.modelTestPerformances;
            },
            confusionMatrix () {
                return this.$store.state.metrics.training.latest.confusion_matrix[0.005]
            },
            metrics () {
                return [
                    {
                        name: 'roc auc score',
                        value: this.$store.state.metrics.training.latest.roc_auc,
                        descritption: 'The roc auc score gives an idea of how well our model performs independantly of the threshold we end up choosing',
                    },
                    {
                        name: 'precision score',
                        value: this.$store.state.metrics.training.latest.precisions[0.005],
                        descritption: 'The precision score is the proportion of predicted failures that did end up failing.',
                    },
                    {
                        name: 'recall score',
                        value: this.$store.state.metrics.training.latest.recalls[0.05],
                        descritption: 'The recall score is the proportion of failures that were detected in advances by our model',
                    },
                    {
                        name: 'f1 score',
                        value: this.$store.state.metrics.training.latest.f1_scores[0.05],
                        descritption: 'The f1 score is the harmonic average of the precision and the recall. This metric measures the performance of the model by taking into account precision and recall at the same level. Hence it is better in cases of unbalanced dataset than accuracy',
                    },
            ]
        }
        },
        mounted() {
            this.$store.dispatch('getAllMetrics');
        }
    }

</script>
