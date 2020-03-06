<template>
    <v-tooltip  right max-width="200px">
        <template v-slot:activator="{ on }">
            <v-icon color="#757575" v-on="on" style="margin-left: 5px;">mdi-help-circle</v-icon>
        </template>
        <span>{{value}}</span>
    </v-tooltip>
</template>

<script>
    export default {
        name: "Tooltip",
        props:{
            value: {
                type: String,
                default: ""
            }
        }
    }
</script>

<style scoped>

</style>