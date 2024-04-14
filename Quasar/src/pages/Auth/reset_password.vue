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
                v-model="email"
                type="email"
                hint="ایمیل خود را برای ارسال بازیابی رمز عبور وارد کنید"
                label="ایمیل"
                lazy-rules
              />

              <div>
                <q-btn label="ارسال" type="submit" color="primary"/>
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
      email: ''
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
          app.$q.loading.hide()
        })
    },

    ResetPassword () {
      const app = this

      const form = new FormData()
      form.append('email', this.email)

      this.$q.loading.show()
      this.$axios.post(process.env.api + 'api/auth/password/reset/', form)
        .then(function () {
          app.showNotif('لینک بازیابی رمز عبور با موفقیت ارسال شد', 'mdi-checkbox-marked-circle-outline ', 'green')
          app.$router.push('/password/reset/confirm')
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
