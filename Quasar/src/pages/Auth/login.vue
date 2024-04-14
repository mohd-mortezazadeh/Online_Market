<template>
  <q-layout>
    <q-page-container>
      <q-page class="flex bg-image flex-center">
        <q-card v-bind:style="$q.screen.lt.sm?{'width': '80%'}:{'width':'30%'}">
          <q-card-section>
            <q-form
              @submit.prevent="Login"
              class="q-ma-md q-gutter-md"
            >
              <q-input
                filled
                v-model="username"
                label="نام کاربری"
                lazy-rules
              />

              <q-input
                type="password"
                filled
                v-model="password"
                label="رمز عبور"
                lazy-rules

              />

              <router-link to="/password/reset">رمز عبور خود را فراموش کرده اید؟</router-link>

              <div style="display: inline">
                ثبت نام نکرده اید؟  <router-link to="/register">ثبت نام</router-link> کنید
              </div>

              <div>
                <q-btn label="ورود" type="submit" color="primary"/>
              </div>
            </q-form>
          </q-card-section>
        </q-card>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script>
export default {
  data () {
    return {
      username: '',
      password: ''
    }
  },

  mounted () {
    this.isLogin()
  },

  methods: {
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
          if (response.data.login_status && response.data.super_user_status) {
            app.$router.push('/')
          }
        })
        .catch(function () {
          localStorage.removeItem('token')
          delete app.$axios.defaults.headers.common.Authorization
          app.$q.loading.hide()
        })
    },

    Login () {
      const app = this

      const form = new FormData()
      form.append('username', this.username)
      form.append('password', this.password)

      this.$q.loading.show()
      this.$axios.post(process.env.api + 'api/auth/login/', form)
        .then(function (response) {
          localStorage.setItem('token', response.data.access)
          app.$axios.defaults.headers.common.Authorization = 'Bearer' + ' ' + response.data.access
          app.$store.commit('shop/setUser', response.data.user)

          localStorage.setItem('username', response.data.user.username)
          localStorage.setItem('user_id', response.data.user.id)

          app.showNotif('شما با موفقیت وارد شدید', 'mdi-checkbox-marked-circle-outline ', 'green')
          if (!response.data.user.is_superuser) {
            window.location.href = '/panel'
            return
          }
          window.location.href = '/admin'
        })
        .catch(function (error) {
          if (error.response.status === 401) {
            app.showNotif(error.response.data.message)
          } else {
            for (const item in error.response.data) {
              app.showNotif(item + ' : ' + error.response.data[item][0])
              break
            }
          }
        })
        .finally(function () {
          app.$q.loading.hide()
        })
    }
  }
}
</script>

<style>
.bg-image {
  background-image: linear-gradient(135deg, #061a47 0%, #01112f 100%);
}
</style>
