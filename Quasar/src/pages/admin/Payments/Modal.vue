<template>
  <q-dialog v-model="_dialog">
    <q-card style="width: 900px; max-width: 100vw;">
      <q-card-section class="row items-center q-pa-sm q-mb-sm">
        <div class="q-ml-sm-sm">افزودن پرداختی</div>
        <q-space/>
        <q-btn class="q-mx-auto" icon="mdi-close" flat round size="sm" style="color: #888888; margin-right: 15px"
               v-close-popup/>
      </q-card-section>
      <q-card-section class="items-center">
        <q-form class="row"
                @submit="onSubmit">

          <q-item class="col-lg-12 col-md-6 col-sm-12 col-xs-12">
            <q-select class="col-12" v-model="form.user" map-options :options="users_list" option-value="id"
                      option-label="username" label="کاربر*"/>
          </q-item>

          <q-item class="col-lg-12 col-md-6 col-sm-12 col-xs-12">
            <q-select class="col-12" v-model="form.status" map-options :options="status_list" option-value="value"
                      option-label="key" label="وضعیت*"/>
          </q-item>

          <div class="col-lg-12 col-xs-12 col-sm-4 col- col-md-4 q-pa-xs q-mb-md">
            <div class="field-label"> مبلغ</div>
            <q-input v-model="form.amount"
                     dense/>
          </div>

          <q-card-actions class="bg-white text-teal">
            <q-btn flat label="انصراف" v-close-popup/>
            <q-btn flat :label="type === 'edit' ?  'ویرایش پرداخت': 'ثبت پرداخت'" type="submit"/>
          </q-card-actions>

        </q-form>
      </q-card-section>
    </q-card>
  </q-dialog>
</template>
<script>
export default {
  props: ['showDialog', 'form', 'type', 'users_list', 'colors_list', 'sizes_lis', 'request_type'],

  data () {
    return {
      status_list: [
        {
          key: 'موفق',
          value: true
        },
        {
          key: 'ناموفق',
          value: false
        }
      ]
    }
  },

  methods: {
    onSubmit () {
      const app = this

      if (this.form.count === undefined || this.form.count === '') {
        this.form.count = 1
      }

      if (!this.form.user || this.form.user === 0) {
        app.showNotif('لطفا کاربر را انتخاب کنید')
        return
      }

      if (this.form.status === undefined || this.form.status === 0) {
        app.showNotif('لطفا وضعیت را انتخاب کنید')
        return
      }

      if (this.form.user && this.form.user.id !== undefined) {
        this.form.user_id = this.form.user.id
      }

      if (this.form.status && this.form.status.value !== undefined) {
        this.form.status = this.form.status.value === true ? 1 : 0
      }

      const formData = new FormData()
      for (const item in this.form) {
        if (this.form[item] != null) {
          formData.append(item, this.form[item])
        }
      }

      this.$q.loading.show()

      if (this.type === 'create') {
        this.CreatePayment(app, formData)
      } else {
        this.UpdatePayment(app, formData)
      }
    },

    CreatePayment (app, formData) {
      this.$axios.post(process.env.api + 'api/admin/payments/successful/', formData)
        .then(function () {
          app.showNotif('محصول مورد نظر با موفقیت ثبت شد', 'mdi-checkbox-marked-circle-outline ', 'green')
          app._dialog = false
          app.$parent.$parent.GetAllSuccessfulPayments()
        })
        .finally(function () {
          app.$q.loading.hide()
        })
        .catch(function (error) {
          app.form.status = app.form.status.value === 1
          for (const item in error.response.data) {
            app.showNotif(item + ' : ' + error.response.data[item][0].replace('.', ''))
            break
          }
        })
    },

    UpdatePayment (app, formData) {
      if (this.request_type === 'successful') {
        this.$axios.put(process.env.api + 'api/admin/payments/successful/' + app.form.id + '/', formData)
          .then(function () {
            app.showNotif('پرداخت مورد نظر با موفقیت ویرایش شد', 'mdi-checkbox-marked-circle-outline ', 'green')
            app.$parent.$parent.GetAllSuccessfulPayments()
            app._dialog = false
          })
          .finally(function () {
            app.$q.loading.hide()
          })
          .catch(function (error) {
            app.form.status = app.form.status.value === 1
            for (const item in error.response.data) {
              app.showNotif(item + ' : ' + error.response.data[item][0].replace('.', ''))
              break
            }
          })
      } else {
        this.$axios.put(process.env.api + 'api/admin/payments/unsuccessful/' + app.form.id + '/', formData)
          .then(function () {
            app.showNotif('پرداخت مورد نظر با موفقیت ویرایش شد', 'mdi-checkbox-marked-circle-outline ', 'green')
            app.$parent.$parent.GetAllUnSuccessfulPayments()
            app._dialog = false
          })
          .finally(function () {
            app.$q.loading.hide()
          })
          .catch(function (error) {
            app.form.status = app.form.status.value === 1
            for (const item in error.response.data) {
              app.showNotif(item + ' : ' + error.response.data[item][0].replace('.', ''))
              break
            }
          })
      }
    },

    showNotif (message, icon = 'error', color = 'red') {
      this.$q.notify({
        message: message,
        icon: icon,
        color: color,
        position: 'bottom-right',
        progress: true
      })
    }
  },

  watch: {
    'form.title': function (value) {
      if (this.isSlugSame) {
        this.form.slug = value.replaceAll(' ', '-')
      }
    },

    'form.slug': function (value) {
      if (!this.isSlugSame) {
        this.form.slug = value.replaceAll(' ', '-')
      }
    },

    isSlugSame: function (value) {
      if (value) {
        this.form.slug = this.form.title.replaceAll(' ', '-')
      }
    },

    showDialog: function (value) {
      if (!value) {
        this.text = ''
        this.colors = []
        this.sizes = []
      } else {
        if (this.form.colors && this.form.colors.length > 0) {
          for (const item in this.form.colors) {
            if (this.form.colors[item]) {
              this.colors[item] = this.form.colors[item]
            }
          }
        }
        if (this.form.sizes && this.form.sizes.length > 0) {
          for (const item in this.form.sizes) {
            if (this.form.sizes[item]) {
              this.sizes[item] = this.form.sizes[item]
            }
          }
        }

        if (this.form.text !== undefined) {
          this.text = this.form.text
        }
      }
    }
  },

  computed: {
    _dialog: {
      get () {
        return this.showDialog
      },
      set (value) {
        this.$emit('update:showDialog', value)
      }
    }
  }
}
</script>
