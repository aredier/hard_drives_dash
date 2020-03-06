<template>
    <v-content>
        <v-container fluid>
            <v-row dense>
                <v-col cols="12">
                    <MainCard title="Live Performances" icon="mdi-fast-forward">
                       <v-container fluid>
                           <v-row align="center" style="padding-left: 25px;">
                               <v-col cols="1" align="center" justify="center">
                                   <v-icon color="#BDBDBD" x-large>mdi-information-outline</v-icon>
                               </v-col>
                               <v-col cols="8">
                                   <v-card-subtitle>
                                       Live Performances measure how accurate the past predictions were at predicting failures.
                                       Because our model predicts the probability of failure of each hard drive for the next day every day, we can see
                                       if the hard drive that were predicted to fail at a certain date did in fact fail or if the
                                       hard drives that failed were detected by the model.
                                   </v-card-subtitle>
                               </v-col>
                           </v-row>
                           <v-row align="stretch" justify="center">
                               <v-col cols="4">
                                   <MainCard title="Performance Evolution" icon="mdi-chart-timeline-variant">
                                       <PerformanceGraph :inputData="livePerformanceData" height="375"></PerformanceGraph>
                                   </MainCard>
                               </v-col>
                               <v-col cols="4">
                                   <MainCard style="height: 100%" title="Confusion Matrix" icon="mdi-table">
                                       <ConfusionMatrix :confusionMatrix="liveConfusionMatrix"></ConfusionMatrix>
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
                metrics: [
                    {
                        name: 'accuracy score',
                        value: '99.9%',
                        descritption: 'The accuracy score represents the proportions of predictions that where right',
                    },
                    {
                        name: 'precision score',
                        value: '3.5%',
                        descritption: 'The precision score is the proportion of predicted failures that did end up failing.',
                    },
                    {
                        name: 'recall score',
                        value: '20.3%',
                        descritption: 'The recall score is the proportion of failures that were detected in advances by our model',
                    },
                    {
                        name: 'roc auc score',
                        value: '0.83',
                        descritption: 'The roc auc score gives an idea of how well our model performs independantly of the threshold we end up choosing',
                    },
                ]
            }
        },
        computed: {
            livePerformanceData () {
                return this.$store.state.modelLivePerformances;
            },
            testPerformanceData () {
                return this.$store.state.modelTestPerformances;
            },
            liveConfusionMatrix () {
                return [
                    [253543, 13095],
                    [12, 15]
                ]
            },
            testConfusionMatrix () {
                return [
                    [253345, 12738],
                    [7, 25]
                ]
            },
        }
    }
</script>
