<template>
  <q-layout>
    <q-page-container>
      <q-page class="flex bg-image flex-center">
        <q-card v-bind:style="$q.screen.lt.sm?{'width': '80%'}:{'width':'30%'}">
          <q-card-section>
            <q-form
              @submit.prevent="Register"
              class="q-ma-md q-gutter-md"
            >
              <q-input
                filled
                v-model="username"
                label="نام کاربری"
                lazy-rules
              />

              <q-input
                filled
                type="email"
                v-model="email"
                label="ایمیل"
                lazy-rules
              />

              <q-input
                type="password"
                filled
                v-model="password"
                label="رمز عبور"
                lazy-rules

              />

              <q-input
                type="password"
                filled
                v-model="password2"
                label="تکرار رمز عبور"
                lazy-rules

              />

              <div style="display: inline">
                قبلا ثبت نام کرده اید؟
                <router-link to="/login">وارد</router-link>
                شوید
              </div>

              <div style="display: inline">
                <a :href="ShowGoogleAuthLink()">Google</a>
              </div>

              <div>
                <q-btn label="ثبت نام" type="submit" color="primary"/>
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
      email: '',
      password: '',
      password2: ''
    }
  },

  mounted () {
    this.isLogin()
  },

  methods: {
    ShowGoogleAuthLink () {
      return process.env.api + 'login/google-oauth2/'
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

    Register () {
      const app = this

      const form = new FormData()
      form.append('username', this.username)
      form.append('password', this.password)
      form.append('password2', this.password2)
      form.append('email', this.email)

      this.$q.loading.show()
      this.$axios.post(process.env.api + 'api/auth/register/', form)
        .then(function (response) {
          localStorage.setItem('token', response.data.access)
          app.$axios.defaults.headers.common.Authorization = 'Bearer' + ' ' + response.data.access
          app.$store.commit('shop/setUser', response.data.user)

          localStorage.setItem('username', response.data.user.username)
          localStorage.setItem('user_id', response.data.user.id)

          app.showNotif('شما با موفقیت ثبت نام کردید و ایمیل تایید هویت برای شما ارسال شد', 'mdi-checkbox-marked-circle-outline ', 'green')

          app.$router.push('/email/verify')
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
