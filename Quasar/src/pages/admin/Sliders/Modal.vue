<template>
  <q-dialog v-model="_dialog">
    <q-card style="width: 900px; max-width: 100vw;">
      <q-card-section class="row items-center q-pa-sm q-mb-sm">
        <div class="q-ml-sm-sm">افزودن اسلایدر</div>
        <q-space/>
        <q-btn class="q-mx-auto" icon="mdi-close" flat round size="sm" style="color: #888888; margin-right: 15px"
               v-close-popup/>
      </q-card-section>
      <q-card-section class="items-center">
        <q-form class="row"
                @submit="onSubmit">
          <div class="col-lg-12 col-xs-12 col-sm-4 col- col-md-4 q-pa-xs q-mb-md">
            <div class="field-label"> عنوان <span class="text-red"
                                                  style="font-size: 18px !important;"> * </span></div>
            <q-input v-model="form.title"
                     dense/>
          </div>

          <div class="col-lg-12 col-xs-12 col-sm-4 col- col-md-4 q-pa-xs q-mb-md">
            <div class="field-label"> آدرس <span class="text-red"
                                                 style="font-size: 18px !important;"> * </span></div>
            <q-input v-model="form.url"
                     type="url"
                     dense/>
          </div>

          <div class="col-lg-12 col-xs-12 col-sm-4 col- col-md-4 q-pa-xs q-mb-md">
            <div class="field-label"> الویت <span class="text-red"
                                                  style="font-size: 18px !important;"> * </span></div>
            <q-input v-model="form.priority"
                     type="number"
                     dense/>
          </div>

          <q-item class="col-lg-12 col-md-6 col-sm-12 col-xs-12">
            <q-select class="col-12" v-model="form.status" map-options :options="status_list" option-value="value"
                      option-label="key" label="وضعیت*"/>
          </q-item>

          <q-item v-if="type === 'edit' && form.image" class="col-lg-6 col-md-12 col-sm-12 col-xs-12"
                  style="float: left !important; margin-top: 35px !important; margin-bottom: 30px">

            <q-img
              :src="ShowImage(form.image)"
              spinner-color="white"
              style="height: 170px; max-width: 200px"
            />
          </q-item>

          <q-item
            :class="[type === 'edit' && form.image ? 'col-lg-6' : 'col-lg-12' , 'col-md-12 col-sm-12 col-xs-12']">
            <q-item-section>
              <div class="field-label"> عکس <span class="text-red"
                                                  style="font-size: 18px !important;"> * </span></div>
              <q-uploader :hide-upload-btn="true" ref="uploadFile"
                          :style="$q.screen.width <= 481 ? 'width: 100%' : ''"/>
            </q-item-section>
          </q-item>

          <q-card-actions class="bg-white text-teal">
            <q-btn flat label="انصراف" v-close-popup/>
            <q-btn flat :label="type === 'edit' ?  'ویرایش اسلایدر': 'ثبت اسلایدر'" type="submit"/>
          </q-card-actions>

        </q-form>
      </q-card-section>
    </q-card>
  </q-dialog>
</template>
<script>
export default {
  props: ['showDialog', 'form', 'type', 'request_type'],

  data () {
    return {
      status_list: [
        {
          key: 'فعال',
          value: true
        },
        {
          key: 'غیر فعال',
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

      if (!this.form.title) {
        app.showNotif('فیلد عنوان الزامی است')
        return
      }

      if (!this.form.url) {
        app.showNotif('فیلد آدرس الزامی است')
        return
      }

      if (!this.form.priority) {
        app.showNotif('فیلد الویت الزامی است')
        return
      }

      if (this.form.status === undefined) {
        app.showNotif('فیلد وضعیت الزامی است')
        return
      }

      if (this.form.status && this.form.status.value !== undefined) {
        this.form.status = this.form.status.value
      }

      if (this.type === 'create') {
        if (!this.$refs.uploadFile.files[0]) {
          app.showNotif('فیلد عکس الزامی است')
          return
        } else if (this.$refs.uploadFile.files[0] && this.$refs.uploadFile.files[0].size > 52428800) {
          app.showNotif('حجم عکس انتخاب شده نباید بیشتر از 50 مگابایت باشد !')
          return
        }
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
        this.CreateSlider(app, formData)
      } else {
        this.UpdateSlider(app, formData)
      }
    },

    CreateSlider (app, formData) {
      this.$axios.post(process.env.api + 'api/admin/sliders/active/', formData)
        .then(function (response) {
          app.showNotif('اسلایدر مورد نظر با موفقیت ثبت شد', 'mdi-checkbox-marked-circle-outline ', 'green')
          app._dialog = false
          app.$parent.$parent.GetAllActiveSliders()
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

    UpdateSlider (app, formData) {
      if (this.request_type === 'active') {
        this.$axios.put(process.env.api + 'api/admin/sliders/active/' + app.form.id + '/', formData)
          .then(function () {
            app.showNotif('اسلایدر مورد نظر با موفقیت ویرایش شد', 'mdi-checkbox-marked-circle-outline ', 'green')
            app.$parent.$parent.GetAllActiveSliders()
            app._dialog = false
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
      } else {
        this.$axios.put(process.env.api + 'api/admin/sliders/disable/' + app.form.id + '/', formData)
          .then(function () {
            app.showNotif('اسلایدر مورد نظر با موفقیت ویرایش شد', 'mdi-checkbox-marked-circle-outline ', 'green')
            app.$parent.$parent.GetAllDisableSliders()
            app._dialog = false
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
