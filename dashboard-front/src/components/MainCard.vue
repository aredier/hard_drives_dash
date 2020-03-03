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
            <v-spacer/>
            <slot name="header"></slot>
        </v-app-bar>
        <slot></slot>
    </v-card>
</template>
<script>
    export default {
        props: {
            'title': String,
            'icon': String,
        }
    }
</script>
