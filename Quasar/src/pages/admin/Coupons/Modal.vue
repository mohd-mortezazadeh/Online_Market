<template>
  <q-dialog v-model="_dialog">
    <q-card style="width: 750px; max-width: 100vw;">
      <q-card-section class="row items-center q-pa-sm q-mb-sm">
        <div class="q-ml-sm-sm">افزودن کد تخفیف</div>
        <q-space/>
        <q-btn class="q-mx-auto" icon="mdi-close" flat round size="sm" style="color: #888888; margin-right: 15px"
               v-close-popup/>
      </q-card-section>
      <q-card-section class="items-center">
        <q-form class="row"
                @submit="onSubmit">

          <div class="col-lg-12 col-xs-12 col-sm-4 col- col-md-4 q-pa-xs q-mb-md">
                        <q-checkbox keep-color v-model="code" label="ساخت اتوماتیک کد منحصر بفرد" color="cyan" style="float: left !important;" />

            <div class="field-label"> کد <span class="text-red"
                                               style="font-size: 18px !important;"> * </span></div>
            <q-input :disable="IsUseRandomGenerator()" v-model="form.code" dense/>
          </div>

          <div class="col-lg-12 col-xs-12 col-sm-4 col- col-md-4 q-pa-xs q-mb-md">
            <div class="field-label"> درصد <span class="text-red"
                                                 style="font-size: 18px !important;"> * </span></div>
            <q-input type="number" v-model="form.percent" dense/>
          </div>

          <div class="col-lg-12 col-xs-12 col-sm-4 col- col-md-4 q-pa-xs q-mb-md">
            <div class="field-label"> تعداد قابل استفاده <span class="text-red"
                                                               style="font-size: 12px !important;"> (اگر وارد نکنید پیشفرض 1 میشود) </span>
            </div>
            <q-input type="number" v-model="form.uses_number" dense/>
          </div>

          <q-item class="col-lg-12 col-md-6 col-sm-12 col-xs-12">
            <q-select class="col-12" v-model="form.user" map-options
                      lazy-rules
                      required
                      :options="user_list" option-value="id"
                      option-label="username" label="کاربر"/>
          </q-item>

          <div class="col-lg-12 col-xs-12 col-sm-4 col- col-md-4 q-pa-xs q-mb-md">
            <div class="field-label"> تاریخ انقضا <span class="text-red"
                                                        style="font-size: 18px !important;"> * </span></div>
            <q-date v-model="form.expiration"/>
          </div>

          <q-card-actions class="bg-white text-teal">
            <q-btn flat label="انصراف" v-close-popup/>
            <q-btn flat :label="type === 'edit' ?  'ویرایش کد تخفیف': 'ثبت کد تخفیف'" type="submit"/>
          </q-card-actions>

        </q-form>
      </q-card-section>
    </q-card>
  </q-dialog>
</template>
<script>

export default {
  props: ['showDialog', 'form', 'type', 'user_list'],

  data () {
    return {
      code: false,
      date: '2019/02/01'
    }
  },

  methods: {
    onSubmit () {
      const app = this

      if (!this.form.user || this.form.user.id === null) {
        this.form.user = ''
      } else {
        this.form.user = this.form.user.id
      }

      this.form.expiration = this.form.expiration.replaceAll('/', '-')

      const formData = new FormData()
      for (const item in this.form) {
        if (this.form[item] != null) {
          formData.append(item, this.form[item])
        }
      }

      this.$q.loading.show()

      if (this.type === 'create') {
        this.CreateCoupon(app, formData)
      } else {
        this.UpdateCoupon(app, formData)
      }
    },

    CreateCoupon (app, formData) {
      this.$axios.post(process.env.api + 'api/admin/coupons/', formData)
        .then(function () {
          app.showNotif('کد تخفیف مورد نظر با موفقیت ثبت شد', 'mdi-checkbox-marked-circle-outline ', 'green')
          app._dialog = false
        })
        .finally(function () {
          app.$q.loading.hide()
          app.$parent.$parent.GetAllCoupons()
          app.$parent.$parent.GetUsersList()
        })
        .catch(function (error) {
          for (const item in error.response.data) {
            app.showNotif(item + ' : ' + error.response.data[item][0].replace('.', ''))
            break
          }
        })
    },

    UpdateCoupon (app, formData) {
      this.$axios.put(process.env.api + 'api/admin/coupons/' + app.form.id + '/', formData)
        .then(function () {
          app.showNotif('کد تخفیف مورد نظر با موفقیت ویرایش شد', 'mdi-checkbox-marked-circle-outline ', 'green')
          app._dialog = false
        })
        .finally(function () {
          app.$q.loading.hide()
          app.$parent.$parent.GetAllCoupons()
          app.$parent.$parent.GetUsersList()
        })
        .catch(function (error) {
          for (const item in error.response.data) {
            app.showNotif(item + ' : ' + error.response.data[item][0].replace('.', ''))
            break
          }
        })
    },

    GenerateUniqueCode () {
      var uuid = require('uuid')
      var code = uuid.v4()
      this.form.code = code
    },

    IsUseRandomGenerator () {
      if (this.code === true) {
        return true
      }

      return false
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
    code (value) {
      if (value === true) {
        this.GenerateUniqueCode()
      } else if (this.type === 'create') {
        this.form.code = ''
      }
    },

    showDialog (value) {
      if (value === false) {
        this.code = false
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
