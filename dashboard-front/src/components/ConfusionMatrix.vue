<template>
<v-container fluid align="center" justify="center" fill-height style="height: calc(100% - 60px);">
    <v-row align="center" justify="center">
        <v-col cols="8">
                <v-row >
                    <v-col cols="6" align="center" justify="center"
                           style="border-bottom: solid #757575 2px; border-right: solid #757575 2px; ">
                        <v-btn color="#80DEEA" fab x-large dark>
                            {{confusionMatrix[0][0]}}
                        </v-btn>
                    </v-col>
                    <v-col cols="6" align="center" justify="center"
                           style="border-bottom: solid #757575 2px;">
                        <v-btn color="#FF8A65" fab x-large dark>
                            {{confusionMatrix[0][1]}}
                        </v-btn>
                    </v-col>
                </v-row>
            <v-row >
                <v-col cols="6" align="center" justify="center"
                       style="border-right: solid #757575 2px; ">
                    <v-btn color="#FF8A65" fab x-large dark>
                        {{confusionMatrix[1][0]}}
                    </v-btn>
                </v-col>
                <v-col cols="6" align="center" justify="center">
                    <v-btn color="#80DEEA" fab x-large dark>
                        {{confusionMatrix[1][1]}}
                    </v-btn>
                </v-col>
            </v-row>
        </v-col>
    </v-row>
</v-container>
</template>
<script>
    export default {
        props: {
            confusionMatrix:{
                default: () => [[0, 0], [0, 0]]
            }
        }
    }

</script>