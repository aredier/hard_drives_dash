<template>

    <v-row>
        <v-col
                cols="12"
                style="padding:5px"
        >
            <v-card style="background-color: #424242" elevation="10" :ripple="ripple" @click="click()">
                <v-container fluid>
                    <v-row align="center" justify="center">
                        <slot></slot>
                    </v-row>
                </v-container>
            </v-card>
        </v-col>
    </v-row>
</template>
<script>
    export default {
        props: {
            ripple: {
                type: Boolean,
                default: false,
            }
        },
        methods: {
            click () {
                this.$emit('click')
            }
        }

    }
</script>