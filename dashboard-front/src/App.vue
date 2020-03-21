<template>
    <v-app id="inspire"
           style="background: #616161"
    >
        <v-navigation-drawer
                v-model="drawer"
                :clipped="$vuetify.breakpoint.lgAndUp"
                style="background: #424242"
                app
                temporary
        >
            <v-list dense>
                <v-list-item link @click="pushRoute('/')">
                    <v-list-item-action>
                        <v-icon>mdi-table-large</v-icon>
                    </v-list-item-action>
                    <v-list-item-content>
                        <v-list-item-title>Overview</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
                <v-list-item link @click="pushRoute('/in-depth-analysis')">
                    <v-list-item-action>
                        <v-icon>mdi-chart-line</v-icon>
                    </v-list-item-action>
                    <v-list-item-content>
                        <v-list-item-title>In Depth Analysis</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
                <v-list-group
                        prepend-icon="mdi-speedometer"
                        color="white"
                        no-action
                >
                    <template v-slot:activator>
                        <v-list-item-title>Model Performance</v-list-item-title>
                    </template>
                    <v-list-item link @click="pushRoute('/live-performance')">
                        <v-list-item-content>
                            <v-list-item-title>Live Performance</v-list-item-title>
                        </v-list-item-content>
                    </v-list-item>
                    <v-list-item link @click="pushRoute('/test-performance')">
                        <v-list-item-content>
                            <v-list-item-title>Test Performance</v-list-item-title>
                        </v-list-item-content>
                    </v-list-item>
                </v-list-group>

            </v-list>
        </v-navigation-drawer>

        <v-app-bar
                :clipped-left="$vuetify.breakpoint.lgAndUp"
                app
                style="padding-left: 25px; padding-right: 50px;"
                dark
        >
            <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
            <v-spacer />
            <v-toolbar-title
                    style="width: 300px"
                    class="ml-0 pl-4"
            >
                <span class="hidden-sm-and-down">hard drives monitoring</span>
            </v-toolbar-title>
            <v-spacer />
            <v-menu v-model="notificationMenu"
                    offset-y
                    max-height="400"
                    max-width="550"
                    :close-on-content-click="false">
                <template v-slot:activator="{ on }">
                    <v-badge
                            :value="notificationDot"
                            color="error"
                            overlap
                            dot
                            offset-x="15"
                            offset-y="15"
                    >
                        <v-btn
                                dark
                                v-on="on"
                                icon
                        >
                            <v-icon>mdi-bell</v-icon>
                        </v-btn>
                    </v-badge>
                </template>
                <v-card
                        style="margin-top: 5px; background: #616161"
                >
                    <NotificationPool
                            clickable
                            :notifications="notifications"
                            textSize="small"
                    />
                </v-card>
            </v-menu >
        </v-app-bar>
        <router-view></router-view>
    </v-app>
</template>

<script>
    import router from "@/router";
    import NotificationPool from "@/components/NotificationPool";
    export default {
        props: {
            source: String,
        },
        components: {
            NotificationPool
        },
        methods: {
            pushRoute: function (route){
                router.push({
                    path: route
                })
            }
        },
        data: () => ({
            dialog: false,
            notificationMenu: false,
            notificationDot: true,
            drawer: null,
        }),
        computed: {
            notifications () {
                return this.$store.state.notifications
            }
        },
        watch: {
            notificationMenu (value) {
                if (!value) {
                    this.notificationDot = false;
                }
            }
        },
        created () {
            this.$vuetify.theme = {
                dark: true,
            }
        },
        mounted() {
            this.$store.dispatch('applyFilters', {
                probaRange: [0, 1],
                selectedModels: [],
                selectFailures: true,
                selectWarnings: true,
                selectNominal: true,
            });
            this.$store.dispatch('updateModelPerformances')
        }
    }
</script>
<style>
    body::-webkit-scrollbar {
        width: 0.3em;
        background-color: #757575;
    }

    body::-webkit-scrollbar-track {
        -webkit-box-shadow: inset 0 0 6px rgba(0,0,0,0.3);
    }

    body::-webkit-scrollbar-thumb {
        background-color: #212121;
        outline: 1px solid #212121
    }
    .no-scroll::-webkit-scrollbar {
        display: none;
    }
</style>
