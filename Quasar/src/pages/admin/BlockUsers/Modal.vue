<template>
  <q-dialog v-model="_dialog">
    <q-card style="width: 900px; max-width: 100vw;">
      <q-card-section class="row items-center q-pa-sm q-mb-sm">
        <div class="q-ml-sm-sm">افزودن کاربر</div>
        <q-space/>
        <q-btn class="q-mx-auto" icon="mdi-close" flat round size="sm" style="color: #888888; margin-right: 15px"
               v-close-popup/>
      </q-card-section>
      <q-card-section class="items-center">
        <q-form class="row"
                @submit="onSubmit">
          <div class="col-lg-12 col-xs-12 col-sm-4 col- col-md-4 q-pa-xs q-mb-md">
            <div class="field-label"> نام کاربری <span class="text-red"
                                                       style="font-size: 18px !important;"> * </span></div>
            <q-input v-model="form.username" dense/>
          </div>

           <div class="col-lg-12 col-xs-12 col-sm-4 col- col-md-4 q-pa-xs q-mb-md">
            <div class="field-label"> رمز عبور <span class="text-red"
                                                       style="font-size: 18px !important;"> * </span></div>
            <q-input v-model="password" dense/>
          </div>

          <div class="col-lg-12 col-xs-12 col-sm-4 col-md-4 q-pa-xs q-mb-md">
            <div class="field-label"> نام </div>
            <q-input v-model="form.first_name" dense style="margin-top: 6px !important;"/>
          </div>

          <div class="col-lg-12 col-xs-12 col-sm-4 col-md-4 q-pa-xs q-mb-md">
            <div class="field-label"> نام خانوادگی </div>
            <q-input v-model="form.last_name" dense style="margin-top: 6px !important;"/>
          </div>

         <div class="col-lg-12 col-xs-12 col-sm-4 col-md-4 q-pa-xs q-mb-md">
            <div class="field-label"> ایمیل <span class="text-red"
                                                         style="font-size: 18px !important;"> * </span></div>
            <q-input v-model="form.email" dense style="margin-top: 6px !important;"/>
          </div>

        <div class="col-lg-12 col-xs-12 col-sm-4 col-md-4 q-pa-xs q-mb-md">
            <div class="field-label"> موبایل </div>
            <q-input v-model="form.phoneNumber" dense style="margin-top: 6px !important;"/>
          </div>

             <q-item class="col-lg-12 col-md-6 col-sm-12 col-xs-12">
            <q-select class="col-12" v-model="form.is_superuser" map-options :options="super_user" option-value="value"
                      option-label="key" label="آیا مدیر است؟"/>
          </q-item>

          <q-item class="col-lg-12 col-md-6 col-sm-12 col-xs-12">
            <q-select class="col-12" v-model="form.is_active" map-options :options="active_user" option-value="value"
                      option-label="key" label="آیا فعال است؟"/>
          </q-item>

          <q-item class="col-lg-12 col-md-6 col-sm-12 col-xs-12">
            <q-select class="col-12" v-model="form.is_staff" map-options :options="staff_user" option-value="value"
                      option-label="key" label="آیا کارمند سایت است؟"/>
          </q-item>

          <q-item v-if="type === 'edit' && form.image" class="col-lg-6 col-md-12 col-sm-12 col-xs-12" style="float: left !important;">
              <q-img
                        :src="ShowImage(form.image)"
                        spinner-color="white"
                        style="height: 150px; max-width: 200px"
                      />
          </q-item>

          <q-item :class="[type === 'edit' && form.image ? 'col-lg-6' : 'col-lg-12' , 'col-md-12 col-sm-12 col-xs-12']">
            <q-item-section>
              <div class="field-label" style="margin-bottom: 7px"> عکس </div>
              <q-uploader :hide-upload-btn="true" ref="uploadFile"
                          :style="$q.screen.width <= 481 ? 'width: 100%' : ''"/>
            </q-item-section>
          </q-item>

          <q-card-actions class="bg-white text-teal">
            <q-btn flat label="انصراف" v-close-popup/>
            <q-btn flat :label="type === 'edit' ?  'ویرایش کاربر': 'ثبت کاربر'" type="submit"/>
          </q-card-actions>

        </q-form>
      </q-card-section>
    </q-card>
  </q-dialog>
</template>
<script>
export default {
  props: ['showDialog', 'form', 'type'],

  data () {
    return {
      password: '',
      super_user: [
        {
          key: 'بله',
          value: true
        },
        {
          key: 'خیر',
          value: false
        }
      ],

      active_user: [
        {
          key: 'بله',
          value: true
        },
        {
          key: 'خیر',
          value: false
        }
      ],

      staff_user: [
        {
          key: 'بله',
          value: true
        },
        {
          key: 'خیر',
          value: false
        }
      ]
    }
  },

  methods: {
    ShowImage (url) {
      if (url) {
        return url.replace('http://localhost:8000/', process.env.api)
      }
    },

    onSubmit () {
      const app = this

      if (this.$refs.uploadFile.files[0] && this.$refs.uploadFile.files[0].size > 52428800) {
        app.showNotif('حجم عکس انتخاب شده نباید بیشتر از 50 مگابایت باشد !')
        return
      }

      this.form.password2 = this.form.password = this.password

      if (this.form.is_superuser && this.form.is_superuser.value !== undefined) {
        this.form.is_superuser = this.form.is_superuser.value
      }

      if (this.form.is_active && this.form.is_active.value !== undefined) {
        this.form.is_active = this.form.is_active.value
      }

      if (this.form.is_staff && this.form.is_staff.value !== undefined) {
        this.form.is_staff = this.form.is_staff.value
      }

      if (this.$refs.uploadFile.files[0] === undefined) {
        delete this.form.image
      }

      const formData = new FormData()
      for (const item in this.form) {
        if (this.form[item] != null) {
          formData.append(item, this.form[item])
        }
      }

      if (this.$refs.uploadFile.files[0] !== undefined) {
        formData.append('image', this.$refs.uploadFile.files[0])
      }

      this.$q.loading.show()

      if (this.type === 'create') {
        this.CreateUser(app, formData)
      } else {
        this.UpdateUser(app, formData)
      }
    },

    CreateUser (app, formData) {
      this.$axios.post(process.env.api + 'api/admin/users/blocks/list/', formData)
        .then(function () {
          app.showNotif('کاربر مورد نظر با موفقیت ثبت شد', 'mdi-checkbox-marked-circle-outline ', 'green')
          app._dialog = false
          app.$parent.$parent.GetAllUsers()
        })
        .finally(function () {
          app.$q.loading.hide()
        })
        .catch(function (error) {
          for (const item in error.response.data) {
            app.showNotif(item + ' : ' + error.response.data[item][0].replace('.', ''))
            break
          }
        })
    },

    UpdateUser (app, formData) {
      this.$axios.put(process.env.api + 'api/admin/users/blocks/list/' + app.form.id + '/', formData)
        .then(function () {
          app.showNotif('کاربر مورد نظر با موفقیت ویرایش شد', 'mdi-checkbox-marked-circle-outline ', 'green')
          app._dialog = false
        })
        .finally(function () {
          app.$q.loading.hide()
          app.$parent.$parent.GetAllUsers()
        })
        .catch(function (error) {
          for (const item in error.response.data) {
            app.showNotif(item + ' : ' + error.response.data[item][0].replace('.', ''))
            break
          }
        })
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
    _dialog: function (value) {
      if (value) {
        this.password = ''
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
