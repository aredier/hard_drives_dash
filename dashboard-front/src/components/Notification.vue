<template>
    <ChipRow :ripple="ripple" @click="click()">
        <v-col cols="1">
            <v-icon :color="color">
                {{icon}}
            </v-icon>
        </v-col>
        <v-col :style='"font-size: " + this.textSize + ";"' cols="9">
            <slot></slot>
        </v-col>
        <v-col cols="2">
            <v-btn icon @click="closeNotification()">
                <v-icon>
                    mdi-close-circle
                </v-icon>
            </v-btn>
        </v-col>
    </ChipRow>
</template>
<script>
    import ChipRow from "@/components/ChipRow";
    export default {
        props:{
            icon: {
                type: String,
                required: true
            },
            ripple: {
                type: Boolean,
                default: true,
            },
            textSize: {
                type: String,
                default: 'medium'
            },
            color: String
        },
        components: {
            ChipRow
        },
        methods:{
            closeNotification () {
                this.$emit(
                    'closeNotification'
                );
            },
            click () {
                this.$emit('click')
            }
        },
    }
</script>
