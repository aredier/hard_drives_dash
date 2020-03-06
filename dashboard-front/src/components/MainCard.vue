<template>
    <v-card
            style="background: #424242"
            elevation="7"
    >
        <v-app-bar
                dark
                height="60px;"
        >
            <v-icon style="margin-right: 15px;">{{icon}}</v-icon>
            <v-toolbar-title>{{title}}</v-toolbar-title>
            <Tooltip :value="tooltip" v-if="tooltip != ''"/>
            <v-spacer/>
            <slot name="header"></slot>
        </v-app-bar>
        <v-container fluid  v-if="isLoading">
            <v-row  align="center" justify="center" style="height: 300px;">
                <v-progress-circular
                        :size="70"
                        :width="7"
                        indeterminate
                        :color="loadingColor" />
            </v-row>
        </v-container>
        <slot v-else></slot>
    </v-card>
</template>
<script>
    import Tooltip from "@/components/Tooltip";
    export default {
        components:{
            Tooltip
        },
        props: {
            'title': String,
            'icon': String,
            'isLoading': {
                type: Boolean,
                default: false
            },
            'loadingColor':{
                type: String,
                default: '#80DEEA'
            },
            'tooltip': {
                type: String,
                default: ''
            }
        }
    }
</script>
