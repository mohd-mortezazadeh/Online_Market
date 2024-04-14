<template>
  <q-dialog v-model="_dialog">
    <q-card style="width: 750px; max-width: 100vw;">
      <q-card-section class="row items-center q-pa-sm q-mb-sm">
        <div class="q-ml-sm-sm">افزودن تیکت</div>
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
                     dense />
          </div>

           <q-item class="col-lg-12 col-md-6 col-sm-12 col-xs-12">
            <q-select class="col-12" v-model="form.user" map-options
                      :options="user_list" option-value="id"
                       option-label="username" label="کاربر*"/>
          </q-item>

              <q-item class="col-lg-12 col-md-6 col-sm-12 col-xs-12">
            <q-select class="col-12" v-model="form.status" map-options
                      :options="status_list" option-value="value"
                       option-label="key" label="وضعیت*"/>
          </q-item>

          <q-card-actions class="bg-white text-teal">
            <q-btn flat label="انصراف" v-close-popup/>
            <q-btn flat :label="type === 'edit' ?  'ویرایش تیکت': 'ثبت تیکت'" type="submit"/>
          </q-card-actions>

        </q-form>
      </q-card-section>
    </q-card>
  </q-dialog>
</template>
<script>
export default {
  props: ['showDialog', 'form', 'type', 'user_list', 'request_type'],

  data () {
    return {
      status_list: [
        {
          key: 'باز',
          value: true
        },
        {
          key: 'بسته',
          value: false
        }
      ],
      isSlugSame: false
    }
  },

  methods: {
    onSubmit () {
      const app = this

      // if (!this.form.parent) {
      //   this.form.parent = null
      // } else {
      //   this.form.parent = process.env.api + 'api/admin/categories/parent/' + this.form.parent.id + '/'
      // }

      if (this.form.title === undefined || this.form.title === '') {
        this.showNotif('فیلد عنوان اجباری است')
        return
      }

      if (this.form.user === undefined || this.form.user === null) {
        this.showNotif('فیلد کاربر اجباری است')
        return
      }

      if (!this.form.user || this.form.user.id === 0) {
        this.form.user = null
      } else {
        this.form.user = this.form.user.id
      }

      if (this.form.status === undefined) {
        app.showNotif('لطفا وضعیت را انتخاب کنید')
        return
      } else {
        if (this.form.status.key) {
          this.form.status = this.form.status.value
        }
      }

      const formData = new FormData()
      for (const item in this.form) {
        if (this.form[item] != null) {
          formData.append(item, this.form[item])
        }
      }

      this.$q.loading.show()

      if (this.type === 'create') {
        this.CreateTicket(app, formData)
      } else {
        this.UpdateTicket(app, formData)
      }
    },

    CreateTicket (app, formData) {
      this.$axios.post(process.env.api + 'api/admin/tickets/open/', formData)
        .then(function () {
          app.showNotif('تیکت مورد نظر با موفقیت ثبت شد', 'mdi-checkbox-marked-circle-outline ', 'green')
          app._dialog = false
        })
        .finally(function () {
          app.$q.loading.hide()
          app.$parent.$parent.GetAllOpenTickets()
          app.$parent.$parent.GetUsersList()
        })
        .catch(function (error) {
          for (const item in error.response.data) {
            app.showNotif(item + ' : ' + error.response.data[item][0].replace('.', ''))
            break
          }
        })
    },

    UpdateTicket (app, formData) {
      if (this.request_type === 'open_tickets_list') {
        this.$axios.put(process.env.api + 'api/admin/tickets/open/' + app.form.id + '/', formData)
          .then(function () {
            app.showNotif('تیکت مورد نظر با موفقیت ویرایش شد', 'mdi-checkbox-marked-circle-outline ', 'green')
            app._dialog = false
          })
          .finally(function () {
            app.$q.loading.hide()
            app.$parent.$parent.GetAllOpenTickets()
            app.$parent.$parent.GetUsersList()
          })
          .catch(function (error) {
            for (const item in error.response.data) {
              app.showNotif(item + ' : ' + error.response.data[item][0].replace('.', ''))
              break
            }
          })
      } else {
        this.$axios.put(process.env.api + 'api/admin/tickets/close/' + app.form.id + '/', formData)
          .then(function () {
            app.showNotif('تیکت مورد نظر با موفقیت ویرایش شد', 'mdi-checkbox-marked-circle-outline ', 'green')
            app._dialog = false
          })
          .finally(function () {
            app.$q.loading.hide()
            app.$parent.$parent.GetAllCloseTickets()
            app.$parent.$parent.GetUsersList()
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
