<script>
    import { Line, mixins} from 'vue-chartjs';
    const {reactiveProp} = mixins;

    export default {
        extends: Line,
        mixins: [reactiveProp],
        props: {
            history: {
                default: () => {return []}
            }
        },
        methods: {
            render  () {
                let startSlice = this.history.length - 15;
                var selectedDates =this.$store.state.dates.slice(startSlice, this.$store.state.dates.length);
                this.renderChart({
                        labels: selectedDates,
                        datasets: [
                            {
                                label: 'failure proba estimation',
                                backgroundColor: '#FF8A65',
                                data: this.history.sort((a, b) =>{
                                    return a.date > b.date? 1: -1;
                                }).slice(
                                    startSlice, this.history.length
                                ).map(el => {
                                    return el.failure_probability
                                }),
                                fontColor: 'white'
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
                                    display: false,
                                    color: "#616161",
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
            groupedData: function () {
                this.render()
            }
        },
    }
</script>