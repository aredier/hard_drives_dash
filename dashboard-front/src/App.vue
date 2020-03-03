<template>
    <v-app id="inspire"
           style="background: #616161"
    >
        <v-navigation-drawer
                v-model="drawer"
                :clipped="$vuetify.breakpoint.lgAndUp"
                style="background: #424242"
                app
        >
            <v-list dense>
                <template v-for="item in items">
                    <v-list-item
                            :key="item.text"
                            link
                            @click="pushRoute(item.route)"
                    >
                        <v-list-item-action>
                            <v-icon>{{ item.icon }}</v-icon>
                        </v-list-item-action>
                        <v-list-item-content>
                            <v-list-item-title>
                                {{ item.text }}
                            </v-list-item-title>
                        </v-list-item-content>
                    </v-list-item>
                </template>
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
                    <v-btn
                            dark
                            v-on="on"
                            icon
                    >
                        <v-icon>mdi-bell</v-icon>
                    </v-btn>
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
            drawer: null,
            items: [
                {
                    icon: 'mdi-table-large',
                    text: 'Overview',
                    route: '/',
                },
                {
                    icon: 'mdi-chart-line',
                    text: 'In depth analysis',
                    route: '/in-depth-analysis',
                },
                {
                    icon: 'mdi-speedometer',
                    text: 'model performance',
                    route: '/model-performance',
                },
            ],
        }),
        computed: {
            notifications () {
                return this.$store.state.notifications
            }
        },
        created () {
            this.$vuetify.theme = {
                dark: true,
            }
        },
        mounted() {
            this.$store.dispatch('updateStatuses', 1000);
            this.$store.dispatch('applyFilters', {
                probaRange: [0, 1],
                selectedModels: []
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
