<template>
  <q-dialog v-model="_dialog">
    <q-card style="width: 750px; max-width: 100vw;">
      <q-card-section class="row items-center q-pa-sm q-mb-sm">
        <div class="q-ml-sm-sm">افزودن تنظیمات</div>
        <q-space/>
        <q-btn class="q-mx-auto" icon="mdi-close" flat round size="sm" style="color: #888888; margin-right: 15px"
               v-close-popup/>
      </q-card-section>
      <q-card-section class="items-center">
        <q-form class="row"
                @submit="onSubmit">
          <div class="col-lg-12 col-xs-12 col-sm-4 col- col-md-4 q-pa-xs q-mb-md">
            <div class="field-label"> کلید <span class="text-red"
                                                 style="font-size: 18px !important;"> * </span></div>
            <q-input v-model="form.key"
                     dense/>
          </div>

            <div class="col-lg-12 col-xs-12 col-sm-4 col- col-md-4 q-pa-xs q-mb-md">
            <div class="field-label"> مقدار <span class="text-red"
                                                style="font-size: 18px !important;"> * </span></div>
            <q-editor
              height="250px"
              v-model="value"
              :definitions="{
        bold: {label: 'Bold', icon: null, tip: 'My bold tooltip'}
      }"
            />
          </div>

          <q-card-actions class="bg-white text-teal">
            <q-btn flat label="انصراف" v-close-popup/>
            <q-btn flat :label="type === 'edit' ?  'ویرایش تنظیمات': 'ثبت تنظیمات'" type="submit"/>
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
      value: this.form.value ? this.form.value : ''
    }
  },

  methods: {
    onSubmit () {
      const app = this

      if (!this.form.key) {
        this.showNotif('فیلد کلید الزامی است')
        return
      }
      if (!this.value) {
        this.showNotif('فیلد مقدار الزامی است')
        return
      }

      this.form.value = this.value

      const formData = new FormData()
      for (const item in this.form) {
        if (this.form[item] != null) {
          formData.append(item, this.form[item])
        }
      }

      this.$q.loading.show()

      if (this.type === 'create') {
        this.CreateSettings(app, formData)
      } else {
        this.UpdateSettings(app, formData)
      }
    },

    CreateSettings (app, formData) {
      this.$axios.post(process.env.api + 'api/admin/settings/', formData)
        .then(function () {
          app.showNotif('تنظیمات مورد نظر با موفقیت ثبت شد', 'mdi-checkbox-marked-circle-outline ', 'green')
          app.$parent.$parent.GetAllSettings()
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
    },

    UpdateSettings (app, formData) {
      this.$axios.put(process.env.api + 'api/admin/settings/' + app.form.id + '/', formData)
        .then(function () {
          app.showNotif('تنظیمات مورد نظر با موفقیت ویرایش شد', 'mdi-checkbox-marked-circle-outline ', 'green')
          app.$parent.$parent.GetAllSettings()
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
    showDialog (value) {
      if (!value) {
        this.value = ''
      } else {
        this.value = this.form.value
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
