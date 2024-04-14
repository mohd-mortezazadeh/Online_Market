<template>
  <q-dialog v-model="_dialog">
    <q-card style="width: 900px; max-width: 100vw;">
      <q-card-section class="row items-center q-pa-sm q-mb-sm">
        <div class="q-ml-sm-sm">ویرایش پسندیده</div>
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
            <q-select class="col-12" v-model="form.type" map-options :options="types_list" option-value="value"
                      option-label="key" label="نوع*"/>
          </q-item>

          <q-card-actions class="bg-white text-teal">
            <q-btn flat label="انصراف" v-close-popup/>
            <q-btn flat label="ویرایش پسندیده" type="submit"/>
          </q-card-actions>

        </q-form>
      </q-card-section>
    </q-card>
  </q-dialog>
</template>
<script>
export default {
  props: ['showDialog', 'form', 'users_list', 'request_type'],

  data () {
    return {
      types_list: [
        {
          key: 'لایک',
          value: 'like'
        },
        {
          key: 'دیسلایک',
          value: 'dislike'
        }
      ]
    }
  },

  methods: {
    onSubmit () {
      const app = this

      if (this.form.user === undefined) {
        app.showNotif('لطفا کاربر را انتخاب کنید')
        return
      }

      if (this.form.type === undefined) {
        app.showNotif('لطفا نوع را انتخاب کنید')
        return
      }

      if (this.form.user && this.form.user.id !== undefined) {
        this.form.user_id = this.form.user.id
      }

      if (this.form.type && this.form.type.value !== undefined) {
        this.form.type = this.form.type.value
      }

      const formData = new FormData()
      for (const item in this.form) {
        if (this.form[item] != null) {
          formData.append(item, this.form[item])
        }
      }

      this.$q.loading.show()

      this.UpdateLike_And_DisLike(app, formData)
    },

    UpdateLike_And_DisLike (app, formData) {
      if (this.request_type === 'likes') {
        this.$axios.put(process.env.api + 'api/admin/likes_dislikes/likes/' + app.form.id + '/', formData)
          .then(function () {
            app.showNotif('مورد انتخابی  با موفقیت ویرایش شد', 'mdi-checkbox-marked-circle-outline ', 'green')
            app.$parent.$parent.GetAllLikes()
            app.$parent.$parent.GetRequiredLists()
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
        this.$axios.put(process.env.api + 'api/admin/likes_dislikes/dislikes/' + app.form.id + '/', formData)
          .then(function () {
            app.showNotif('مورد انتخابی  با موفقیت ویرایش شد', 'mdi-checkbox-marked-circle-outline ', 'green')
            app.$parent.$parent.GetAllDisLikes()
            app.$parent.$parent.GetRequiredLists()
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
