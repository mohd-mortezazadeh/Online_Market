<template>
  <q-dialog v-model="_dialog">
    <q-card style="width: 900px; max-width: 100vw;">
      <q-card-section class="row items-center q-pa-sm q-mb-sm">
        <div class="q-ml-sm-sm">ویرایش نظر</div>
        <q-space/>
        <q-btn class="q-mx-auto" icon="mdi-close" flat round size="sm" style="color: #888888; margin-right: 15px"
               v-close-popup/>
      </q-card-section>
      <q-card-section class="items-center">
        <q-form class="row"
                @submit="onSubmit">

          <div class="col-lg-12 col-xs-12 col-sm-4 col- col-md-4 q-pa-xs q-mb-md">
            <div class="field-label"> عنوان <span class="text-red"
                                                  style="font-size: 13px !important;"> * </span></div>
            <q-input v-model="form.title"
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

          <q-item class="col-lg-12 col-md-6 col-sm-12 col-xs-12">
            <q-select class="col-12" v-model="form.status" map-options :options="status_list" option-value="value"
                      option-label="key" label="وضعیت*"/>
          </q-item>

          <q-card-actions class="bg-white text-teal">
            <q-btn flat label="انصراف" v-close-popup/>
            <q-btn flat label="ویرایش نظر" type="submit"/>
          </q-card-actions>

        </q-form>
      </q-card-section>
    </q-card>
  </q-dialog>
</template>
<script>
export default {
  props: ['showDialog', 'form', 'request_type'],

  data () {
    return {
      status_list: [
        {
          key: 'تایید شده',
          value: true
        },
        {
          key: 'تایید نشده',
          value: false
        }
      ],

      text: this.form.text ? this.form.text : ''
    }
  },

  methods: {
    onSubmit () {
      const app = this

      if (this.form.text === undefined || this.form.text === '') {
        app.showNotif('فیلد عنوان الزامی است')
        return
      }

      if (this.text === undefined || this.text === '') {
        app.showNotif('فیلد متن الزامی است')
        return
      }

      if (this.form.status === undefined) {
        app.showNotif('لطفا وضعیت را انتخاب کنید')
        return
      }

      if (this.form.status && this.form.status.value !== undefined) {
        this.form.status = this.form.status.value === true ? 1 : 0
      }

      this.form.text = this.text

      const formData = new FormData()
      for (const item in this.form) {
        if (this.form[item] != null) {
          formData.append(item, this.form[item])
        }
      }

      this.$q.loading.show()

      this.UpdateComment(app, formData)
    },

    UpdateComment (app, formData) {
      if (this.request_type === 'accepted') {
        this.$axios.put(process.env.api + 'api/admin/comments/accepted/' + app.form.id + '/', formData)
          .then(function () {
            app.showNotif('نظر مورد نظر با موفقیت ویرایش شد', 'mdi-checkbox-marked-circle-outline ', 'green')
            app.$parent.$parent.GetAllAcceptedPayments()
            app._dialog = false
          })
          .finally(function () {
            app.$q.loading.hide()
          })
          .catch(function (error) {
            this.form.status = this.form.status.value === 1
            for (const item in error.response.data) {
              app.showNotif(item + ' : ' + error.response.data[item][0].replace('.', ''))
              break
            }
          })
      } else {
        this.$axios.put(process.env.api + 'api/admin/comments/NotAccepted/' + app.form.id + '/', formData)
          .then(function () {
            app.showNotif('نظر مورد نظر با موفقیت ویرایش شد', 'mdi-checkbox-marked-circle-outline ', 'green')
            app.$parent.$parent.GetAllNotAcceptedPayments()
            app._dialog = false
          })
          .finally(function () {
            app.$q.loading.hide()
          })
          .catch(function (error) {
            this.form.status = this.form.status.value === 1
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
    showDialog (value) {
      if (!value) {
        this.text = ''
      } else {
        this.text = this.form.text
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
