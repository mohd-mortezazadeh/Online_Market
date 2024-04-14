<template>
  <q-dialog v-model="_dialog">
    <q-card style="width: 900px; max-width: 100vw;">
      <q-card-section class="row items-center q-pa-sm q-mb-sm">
        <div class="q-ml-sm-sm">افزدون تماس با ما</div>
        <q-space/>
        <q-btn class="q-mx-auto" icon="mdi-close" flat round size="sm" style="color: #888888; margin-right: 15px"
               v-close-popup/>
      </q-card-section>
      <q-card-section class="items-center">
        <q-form class="row"
                @submit="onSubmit">

          <div class="col-lg-12 col-xs-12 col-sm-4 col- col-md-4 q-pa-xs q-mb-md">
            <div class="field-label"> نام <span class="text-red"
                                                style="font-size: 13px !important;"> * </span></div>
            <q-input v-model="form.name"
                     dense/>
          </div>

          <div class="col-lg-12 col-xs-12 col-sm-4 col- col-md-4 q-pa-xs q-mb-md">
            <div class="field-label"> ایمیل <span class="text-red"
                                                  style="font-size: 13px !important;"> * </span></div>
            <q-input type="email" v-model="form.email"
                     dense/>
          </div>

          <div class="col-lg-12 col-xs-12 col-sm-4 col- col-md-4 q-pa-xs q-mb-md">
            <div class="field-label"> وبسایت</div>
            <q-input v-model="form.website"
                     dense/>
          </div>

          <div class="col-lg-12 col-xs-12 col-sm-4 col- col-md-4 q-pa-xs q-mb-md">
            <div class="field-label"> متن <span class="text-red"
                                                style="font-size: 18px !important;"> * </span></div>
            <q-editor
              height="250px"
              v-model="text"
              :definitions="{
        bold: {label: 'Bold', icon: null, tip: 'My bold tooltip'}
      }"
            />
          </div>

          <q-card-actions class="bg-white text-teal">
            <q-btn flat label="انصراف" v-close-popup/>
            <q-btn flat :label="type === 'edit' ?  'ویرایش تماس باما': 'ثبت تماس باما'" type="submit"/>
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
      text: this.form.text ? this.form.text : ''
    }
  },

  methods: {
    onSubmit () {
      const app = this

      if (this.form.name === undefined || this.form.name === '') {
        app.showNotif('فیلد نام الزامی است')
        return
      }

      if (this.form.email === undefined || this.form.email === '') {
        app.showNotif('فیلد ایمیل الزامی است')
        return
      }

      if (this.text === undefined || this.text === '') {
        app.showNotif('فیلد متن الزامی است')
        return
      }

      this.form.text = this.text

      const formData = new FormData()
      for (const item in this.form) {
        if (this.form[item] != null) {
          formData.append(item, this.form[item])
        }
      }

      this.$q.loading.show()

      if (this.type === 'create') {
        this.CreateContactUs(app, formData)
      } else {
        this.UpdateContactUs(app, formData)
      }
    },

    CreateContactUs (app, formData) {
      this.$axios.post(process.env.api + 'api/admin/contact_us/', formData)
        .then(function () {
          app.showNotif('تماس باما نظر با موفقیت ثبت شد', 'mdi-checkbox-marked-circle-outline ', 'green')
          app._dialog = false
          app.$parent.$parent.GetAllContact_us()
          app.text = ''
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

    UpdateContactUs (app, formData) {
      this.$axios.put(process.env.api + 'api/admin/contact_us/' + app.form.id + '/', formData)
        .then(function () {
          app.showNotif('تماس باما نظر با موفقیت ویرایش شد', 'mdi-checkbox-marked-circle-outline ', 'green')
          app.$parent.$parent.GetAllContact_us()
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
        this.text = ''
      } else {
        this.text = this.form.text ? this.form.text : ''
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
