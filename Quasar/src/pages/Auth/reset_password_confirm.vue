<template>
  <q-layout>
    <q-page-container>
      <q-page class="flex bg-image flex-center">
        <q-card v-bind:style="$q.screen.lt.sm?{'width': '80%'}:{'width':'30%'}">
          <q-card-section>
            <q-form
              @submit.prevent="ResetPassword"
              class="q-ma-md q-gutter-md"
            >

              <q-input
                filled
                v-model="token"
                hint="کد (token) که به ایمیل شماارسال شده است را وارد کنید"
                label="کد"
                lazy-rules
              />

              <q-input
                filled
                v-model="password"
                label="رمز عبور جدید"
                lazy-rules
              />

              <div>
                <q-btn label="تغییر رمز عبور" type="submit" color="primary"/>
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
      token: '',
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
          if (response.data.login_status) {
            app.$router.push('/')
          }
        })
        .catch(function () {
          localStorage.removeItem('token')
          delete app.$axios.defaults.headers.common.Authorization
          app.$q.loading.hide()
        })
    },

    ResetPassword () {
      const app = this

      const form = new FormData()
      form.append('token', this.token)
      form.append('new_password', this.password)

      this.$q.loading.show()
      this.$axios.post(process.env.api + 'api/auth/password/reset/confirm/', form)
        .then(function () {
          app.showNotif('رمز عبور شما با موفقیت بازیابی شد', 'mdi-checkbox-marked-circle-outline ', 'green')
          app.$router.push('/login')
        })
        .catch(function (error) {
          for (const item in error.response.data) {
            app.showNotif(item + ' : ' + error.response.data[item][0])
            break
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
