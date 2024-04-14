<template>
  <q-layout view="lHh Lpr lFf">
    <q-header class="b-header b-shadow bg-white text-grey-8">
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="leftDrawerOpen = !leftDrawerOpen"
        />

        <q-toolbar-title>
          Blazar Shop
        </q-toolbar-title>

        <q-space/>

        <div class="q-gutter-sm row items-center no-wrap">
          <q-btn round dense flat :icon="$q.fullscreen.isActive ? 'fullscreen_exit' : 'fullscreen'"
                 @click="$q.fullscreen.toggle()"
                 v-if="$q.screen.gt.sm">
            <q-tooltip>تمام صفحه</q-tooltip>
          </q-btn>
          <q-btn @click="Logout" dense flat color="danger" icon="logout">
            <q-tooltip>خروج</q-tooltip>
          </q-btn>

        </div>
      </q-toolbar>
    </q-header>

    <q-drawer
      :width="260"
      v-model="leftDrawerOpen"
      show-if-above
      content-class="bg-grey-1"
    >
      <q-list>
        <div class="flex flex-center">
          <!--     user profile image or company logo   -->
          <img
            class="shadow-3 profile-img"
            alt="Blazar logo"
            src="~assets/Blazar.png"
            width="160"
          >
          <span class="profile-text">
              {{ ShowUserName() }}
          </span>

        </div>

        <q-separator inset="true" class="q-my-sm"/>
        <SideBar></SideBar>
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view/>
    </q-page-container>
  </q-layout>
</template>

<script>

import SideBar from 'components/SideBar'

export default {
  name: 'MainLayout',
  components: {
    SideBar
  },
  data () {
    return {
      dark: false,
      leftDrawerOpen: false
    }
  },

  beforeMount () {
    // localStorage.removeItem('token')
    // delete this.$axios.defaults.headers.common.Authorization
    this.isLogin()
  },

  methods: {
    ShowUserName () {
      return localStorage.getItem('username')
    },
    showNotif (message, icon = 'error', color = 'red') {
      this.$q.notify({
        message: message,
        icon: icon,
        color: color,
        position: 'bottom-left',
        progress: true
      })
    },

    isLogin () {
      const app = this

      this.$axios.post(process.env.api + 'api/auth/isLogin/')
        .then(function (response) {
          if (!response.data.login_status) {
            app.$router.push('/login')
          }
          app.$store.commit('shop/setUser', response.data.user)
        })
        .catch(function () {
          app.$router.push('/login')
        })
        .finally(function () {
          app.$q.loading.hide()
        })
    },

    Logout () {
      const app = this

      this.$q.loading.show()
      this.$axios.post(process.env.api + 'api/auth/logout/')
        .then(function () {
          localStorage.removeItem('token')
          delete app.$axios.defaults.headers.common.Authorization

          app.showNotif('شما با موفقیت خارج شدید', 'mdi-checkbox-marked-circle-outline ', 'green')
          app.$router.push('/login')
        })
        .finally(function () {
          app.$q.loading.hide()
        })
    }
  }
}
</script>
