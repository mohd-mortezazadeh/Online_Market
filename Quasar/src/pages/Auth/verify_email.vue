<template>
  <q-layout>
    <q-page-container>
      <q-page class="flex bg-image flex-center">
        <q-card v-bind:style="$q.screen.lt.sm?{'width': '80%'}:{'width':'30%'}">
          <q-card-section>
            <q-form
              @submit.prevent="VerifyEmail"
              class="q-ma-md q-gutter-md"
            >

              <q-input
                filled
                v-model="token"
                hint="کد (token) که به ایمیل شماارسال شده است را وارد کنید"
                label="کد"
                lazy-rules
              />

              <div>
                <q-btn label="تایید حساب" type="submit" color="primary"/>
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
    this.isVerified()
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

    isVerified () {
      this.$axios.post(process.env.api + 'api/auth/email/verification/check/')
        .then(function (response) {
          if (response.data.verified_at) {
            window.location.href = '/'
          }
        })
    },

    VerifyEmail () {
      const app = this

      const form = new FormData()
      form.append('token', this.token)

      this.$q.loading.show()
      this.$axios.post(process.env.api + 'api/auth/email/verification/', form)
        .then(function () {
          app.showNotif('حساب کابری شما با موفقیت تایید شد', 'mdi-checkbox-marked-circle-outline ', 'green')
          app.$router.push('/')
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
