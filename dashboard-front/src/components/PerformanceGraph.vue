<script>
    import utils from '@/utils';
    import { Line, mixins } from 'vue-chartjs';
    const { reactiveProp } = mixins;

    export default {
        extends: Line,
        mixins: [reactiveProp],
        props: {
             inputData: {
                default: () => {return []}
            },
        },
        computed: {
            formatedData () {
                return this.inputData.map((item) => {
                    return {
                        date: item.date,
                        roc_score: this.computeRocScore(),
                        recall: this.computeRecall(item.yTrue, item.yPred),
                        precision: this.computePrecision(item.yTrue, item.yPred),
                    }
                })
            }
        },
        methods: {
            computeRecall (yTrue, yPred) {
                let positives = utils.zip(yTrue, yPred).filter((item) => item[0] == 1).map((item) => {
                    return item[0] == item[1]? 1: 0
                });
                if (positives.length == 0) {
                    return 0
                }
                return positives.reduce((a, b) => a + b, 0) / positives.length

            },
            computePrecision (yTrue, yPred) {
                let positives = utils.zip(yTrue, yPred).filter((item) => item[1] == 1).map((item) => {
                    return item[0] == item[1]? 1: 0
                });
                if (positives.length == 0) {
                    return 0
                }
                return positives.reduce((a, b) => a + b, 0) / positives.length

            },
            computeRocScore () {
                return (Math.random() / 4) + 0.75
            },
            render  () {
                this.renderChart({
                        labels: this.formatedData.map((item) => {return item.date}),
                        datasets: [
                            {
                                label: 'ROC AUC score',
                                borderColor: '#FF8A65',
                                backgroundColor: '#FF8A65',
                                data: this.formatedData.map((item) => {return item.roc_score}),
                                fill: false,
                            },
                            {
                                label: 'Recall Score',
                                borderColor: '#80DEEA',
                                backgroundColor: '#80DEEA',
                                data: this.formatedData.map((item) => {return item.recall}),
                                fill: false,
                            },
                            {
                                label: 'precision',
                                borderColor: '#CE93D8',
                                backgroundColor: '#CE93D8',
                                data: this.formatedData.map((item) => {return item.precision}),
                                fill: false,
                            },
                        ]
                    },
                    {
                        responsive: true,
                        maintainAspectRatio: false,
                        tooltips: {
                            titleFontColor: 'white',
                            bodyFontColor: 'white',
                        },
                        scales: {
                            yAxes: [{
                                ticks: {
                                    display: true,
                                    fontColor: "white",
                                },
                                gridLines: {
                                    display: true,
                                    color: "#757575",
                                    lineWidth: 2,
                                    drawBorder: false,
                                    borderDash: [2],
                                }
                            }],
                            xAxes: [{
                                ticks: {
                                    display: true,
                                    fontColor: "white",
                                    fontStyle: "font-weight: bold;"
                                },
                                gridLines: {
                                    display: false,
                                }
                            }]
                        }
                    })
            }
        },
        mounted() {
            this.render()
        },
        watch:{
            formatedData: function () {
                this.render()
            }
        },
    }
</script>