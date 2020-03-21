<script>
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
        methods:{
            render  () {
                this.renderChart({
                        labels: this.inputData.map((item) => {return item.date}),
                        datasets: [
                            {
                                label: 'ROC AUC score',
                                borderColor: '#FF8A65',
                                backgroundColor: '#FF8A65',
                                data: this.inputData.map((item) => {return item.roc_score}),
                                fill: false,
                            },
                            {
                                label: 'Recall Score',
                                borderColor: '#80DEEA',
                                backgroundColor: '#80DEEA',
                                data: this.inputData.map((item) => {return item.recall}),
                                fill: false,
                            },
                            {
                                label: 'precision',
                                borderColor: '#CE93D8',
                                backgroundColor: '#CE93D8',
                                data: this.inputData.map((item) => {return item.precision}),
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