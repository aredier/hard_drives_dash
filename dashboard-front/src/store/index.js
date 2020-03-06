import axios from "axios"
import Vue from 'vue'
import Vuex from 'vuex'
import models from './models'

Vue.use(Vuex);

// function choose(choices) {
//   var index = Math.floor(Math.random() * choices.length);
//   return choices[index];
// }

export default new Vuex.Store({
  state: {

    hard_drive_statuses: [],
    filters: {
      probaRange: [0, 1],
      selectedModels: [],
      selectFailures: true,
      selectWarnings: true,
      selectNominal: true,
    },
    groupedData: [],
    nGroupedPoints: 14,
    dates: [
      "2018-12-05",
      "2018-12-06",
      "2018-12-07",
      "2018-12-08",
      "2018-12-09",
      "2018-12-10",
      "2018-12-11",
      "2018-12-12",
      "2018-12-13",
      "2018-12-14",
      "2018-12-15",
      "2018-12-16",
      "2018-12-17",
      "2018-12-18",
      "2018-12-19",
      "2018-12-20",
      "2018-12-21",
      "2018-12-22",
      "2018-12-23",
      "2018-12-24",
      "2018-12-25",
      "2018-12-26",
      "2018-12-27",
      "2018-12-28",
      "2018-12-29",
      "2018-12-30",
      "2018-12-31",
      "2019-01-01",
      "2019-01-02",
      "2019-01-03"
    ],
    allModels: models.allModels,
    modelLivePerformances: [],
    modelTestPerformances: [],
    notifications: [],
    backend: process.env.NODE_ENV == 'development'? 'http://127.0.0.1:5000/': 'https://chariots-poc.appspot.com/',
    groupedDataLoading : false,
    hard_drive_statuses_loading: false,
    targetSerialLoading: false,
    targetSerialStatuses: [],


  },
  mutations: {
    async loadStatuses(state, n) {
      state.hard_drive_statuses_loading = true;
        var res = await axios.post(state.backend + 'api/v1/statuses', {max_records: n}).then(
            (response) => {
              return response.data.map((el) => {
                el['failure_probability'] = Math.pow(Math.random(), 10)
                return el
              })
            }
        );
      state.hard_drive_statuses = res;
      state.hard_drive_statuses_loading = false;
    },
    setFilters (state, filters) {
      state.filters = filters;
    },
    async fetchGroupedData (state) {

      state.groupedDataLoading = true;
      var raw_res = await axios.post(
          state.backend + 'api/v1/failures_per_day',
          {n_days: 14, filters: state.filters}).then(
          (response) => {
            return response.data
            });

      var keys = Object.keys(raw_res).sort((a, b) => {
              return a.date < b.date? -1: 1
            }).slice(0, 14);
      state.groupedData = keys.map(key => {
        return {
          date: key,
          failures: raw_res[key]
        }
      });
      state.groupedDataLoading = false;

    },
    resetModelPerformance(state) {
      state.modelLivePerformances = []
    },
    fetchUpdateModelPerformance (state) {
      state.modelLivePerformances = state.dates.slice(-14).map((date) => {
        let baseAccuracy = (Math.random() / 2) + 0.5;
        let trueValues = [...Array(Math.floor(Math.random() * 100))].map(() => {
          return Math.random() > 0.5 ? 1: 0
        });
        let predValues = trueValues.map((trueValue) => {
          return Math.random() < baseAccuracy? trueValue: 1 - trueValue
        });
        return {
          date: date,
          yTrue: trueValues,
          yPred: predValues

        }
      }),
      state.modelTestPerformances = state.dates.filter(() => {
        return Math.random() > 0.75
      }).map((date) => {
        let baseAccuracy = (Math.random() / 2) + 0.5;
        let trueValues = [...Array(Math.floor(Math.random() * 100))].map(() => {
          return Math.random() > 0.5 ? 1: 0
        });
        let predValues = trueValues.map((trueValue) => {
          return Math.random() < baseAccuracy? trueValue: 1 - trueValue
        });
        return {
          date: date,
          yTrue: trueValues,
          yPred: predValues

        }
      })
    },
    async updateNotifications (state) {
        let problematicRecords = await axios.post(
            state.backend + 'api/v1/notifications',
            {n_days: 30}
            ).then( (response) => {
              return response.data.map((el) => {
                el['failure_probability'] = Math.pow(Math.random(), 10);
                return el
              })
            }
        );
        state.notifications = problematicRecords.filter((status) =>{
          return status.failure == 1 || status.failure_probability > 0.5
        }).map((status) => {
          if (status.failure == 1) {
            return {
              type: 'failure-error',
              date: status.date,
              serial: status.serial_number,
              id: 'f' + status.date + status.serial_number
            }
          } else {
            return {
              type: 'prediction-warning',
              date: status.date,
              serial: status.serial_number,
              proba: status.failure_probability,
              id: 'w' + status.date + status.serial_number
            }
          }
        })
    },
    popNotificationIndex (state, indexToPop) {
      state.notifications.splice(indexToPop, 1)
    },
    async getTargetSerialStatuses (state, serialNumber) {
      state.targetSerialLoading = true;
      var res = await axios.post(
          state.backend + 'api/v1/serial_statuses', {serial_number: serialNumber}
          ).then(
            (response) => {
              return response.data.map((el) => {
                el['failure_probability'] = Math.pow(Math.random(), 10)
                return el
              })
            }
        );
      state.targetSerialStatuses = res;
      state.targetSerialLoading = false;
    }


  },
  actions: {
    async applyFilters (context, filters) {
      context.commit('setFilters', filters);
      await context.commit('fetchGroupedData');
    },
    updateModelPerformances (context) {
      context.commit('resetModelPerformance');
      context.commit('fetchUpdateModelPerformance');
    },
    async updateStatuses (context) {
      await context.commit('loadStatuses', 1000);
      context.commit('updateNotifications');
    },
    popNotification (context, notification) {
      function sameNotification (otherNotification) {
        return notification.id == otherNotification.id
      }
      let indexToPop = context.state.notifications.findIndex(sameNotification)
      context.commit('popNotificationIndex', indexToPop)
    },
  },
  modules: {
  }
})
