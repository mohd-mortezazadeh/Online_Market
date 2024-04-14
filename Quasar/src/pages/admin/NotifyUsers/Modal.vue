<template>
  <q-dialog v-model="_dialog">
    <q-card style="width: 900px; max-width: 100vw;">
      <q-card-section class="row items-center q-pa-sm q-mb-sm">
        <div class="q-ml-sm-sm">افزودن اطلاع رسانی</div>
        <q-space/>
        <q-btn class="q-mx-auto" icon="mdi-close" flat round size="sm" style="color: #888888; margin-right: 15px"
               v-close-popup/>
      </q-card-section>
      <q-card-section class="items-center">
        <q-form class="row"
                @submit="onSubmit">

          <q-item class="col-lg-12 col-md-6 col-sm-12 col-xs-12">
            <q-select class="col-12" v-model="form.active" map-options :options="actives_list" option-value="value"
                      option-label="key" label="وضعیت فعال*"/>
          </q-item>

          <q-item class="col-lg-12 col-md-6 col-sm-12 col-xs-12">
            <q-select class="col-12" v-model="form.user" map-options :options="users_list" option-value="id"
                      option-label="username" label="کاربر*"/>
          </q-item>

          <q-item class="col-lg-12 col-md-6 col-sm-12 col-xs-12">
            <q-select class="col-12" v-model="form.product" map-options :options="products_list" option-value="id"
                      option-label="title" label="محصول*"/>
          </q-item>

          <q-card-actions class="bg-white text-teal">
            <q-btn flat label="انصراف" v-close-popup/>
            <q-btn flat :label="type === 'edit' ?  'ویرایش اطلاع رسانی': 'ثبت اطلاع رسانی'" type="submit"/>
          </q-card-actions>

        </q-form>
      </q-card-section>
    </q-card>
  </q-dialog>
</template>
<script>
export default {
  props: ['showDialog', 'form', 'type', 'request_type', 'products_list', 'users_list'],

  data () {
    return {
      actives_list: [
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
    onSubmit () {
      const app = this

      if (this.form.active === undefined || this.form.active === null) {
        app.showNotif('لطفا وضعیت فعال را انتخاب کنید')
        return
      }

      if (!this.form.user) {
        app.showNotif('لطفا کاربر را انتخاب کنید')
        return
      }

      if (!this.form.product) {
        app.showNotif('لطفا محصول را انتخاب کنید')
        return
      }

      this.form.text = this.text

      if (this.form.active && this.form.active.value !== undefined) {
        this.form.active = this.form.active.value
      }

      if (this.form.user && this.form.user.id !== undefined) {
        this.form.user_id = this.form.user.id
      }

      if (this.form.product && this.form.product.id !== undefined) {
        this.form.product_id = this.form.product.id
      }

      if (this.form.active && this.form.active.id !== undefined) {
        this.form.active_id = this.form.active.id
      }

      const formData = new FormData()
      for (const item in this.form) {
        if (this.form[item] != null) {
          formData.append(item, this.form[item])
        }
      }

      this.$q.loading.show()

      if (this.type === 'create') {
        this.CreateNotifyUser(app, formData)
      } else {
        this.UpdateNotifyUser(app, formData)
      }
    },

    CreateNotifyUser (app, formData) {
      this.$axios.post(process.env.api + 'api/admin/products/notify_users/active/', formData)
        .then(function () {
          app.showNotif('اطلاع رسانی مورد نظر با موفقیت ثبت شد', 'mdi-checkbox-marked-circle-outline ', 'green')
          app._dialog = false
          app.$parent.$parent.GetAllActiveUserNotifies()
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

    UpdateNotifyUser (app, formData) {
      if (this.request_type === 'active') {
        this.$axios.put(process.env.api + 'api/admin/products/notify_users/active/' + app.form.id + '/', formData)
          .then(function () {
            app.showNotif('اطلاع رسانی مورد نظر با موفقیت ویرایش شد', 'mdi-checkbox-marked-circle-outline ', 'green')
            app.$parent.$parent.GetAllActiveUserNotifies()
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
        this.$axios.put(process.env.api + 'api/admin/products/notify_users/inactive/' + app.form.id + '/', formData)
          .then(function () {
            app.showNotif('اطلاع رسانی مورد نظر با موفقیت ویرایش شد', 'mdi-checkbox-marked-circle-outline ', 'green')
            app.$parent.$parent.GetAllInActiveUserNotifies()
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
