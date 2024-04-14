import Vue from 'vue'
import axios from 'axios'

Vue.prototype.$axios = axios

const token = localStorage.token !== undefined ? 'Bearer' + ' ' + localStorage.token : null
axios.defaults.headers.common.Authorization = token
