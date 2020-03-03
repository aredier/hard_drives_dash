<script>
import { Bar } from 'vue-chartjs'
import {mapState} from "vuex";

export default {
    extends: Bar,
    computed: mapState(['groupedData']),
    methods: {
        render  () {
            this.renderChart({
                    labels: this.$store.state.groupedData.map((item) => {
                        return item.date
                    }),

                    datasets: [
                        {
                            label: 'failures',
                            backgroundColor: '#80DEEA',
                            data: this.$store.state.groupedData.map((item) => {
                                return item.failures
                            }),
                            fontColor: 'white'
                        },
                    ]
                },
                {
                    responsive: true,
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
                                lineWidth: 1,
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