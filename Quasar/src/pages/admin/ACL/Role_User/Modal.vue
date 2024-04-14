<template>
  <q-dialog v-model="_dialog">
    <q-card style="width: 750px; max-width: 100vw;">
      <q-card-section class="row items-center q-pa-sm q-mb-sm">
        <div class="q-ml-sm-sm">افزودن نقش-کاربری</div>
        <q-space/>
        <q-btn class="q-mx-auto" icon="mdi-close" flat round size="sm" style="color: #888888; margin-right: 15px"
               v-close-popup/>
      </q-card-section>
      <q-card-section class="items-center">
        <q-form class="row"
                @submit="onSubmit">

          <q-item class="col-lg-12 col-md-6 col-sm-12 col-xs-12">
            <q-select class="col-12" v-model="form.user" map-options
                      :options="user_list" option-value="id"
                      option-label="username" label="کاربر*"/>
          </q-item>

          <q-item class="col-lg-12 col-md-6 col-sm-12 col-xs-12">
            <q-select
              map-options
              class="col-12"
              v-model="roles"
              multiple
              :options="role_list"
              option-label="title"
              option-value="id"
              use-chips
              stack-label
              label="نقش (میتوانید چند نقش را انتخاب کنید)*"
            />
          </q-item>

          <q-card-actions class="bg-white text-teal">
            <q-btn flat label="انصراف" v-close-popup/>
            <q-btn flat :label="type === 'edit' ?  'ویرایش نقش-کاربری': 'ثبت نقش-کاربری'" type="submit"/>
          </q-card-actions>

        </q-form>
      </q-card-section>
    </q-card>
  </q-dialog>
</template>
<script>
export default {
  props: ['showDialog', 'form', 'type', 'user_list', 'role_list'],

  data () {
    return {
      roles: []
    }
  },

  methods: {
    onSubmit () {
      const app = this

      if (this.form.user === undefined || this.form.user === null) {
        this.showNotif('فیلد کاربر اجباری است')
        return
      }

      if (this.roles.length === 0) {
        this.showNotif('فیلد نقش اجباری است')
        return
      }

      if (!this.form.user || this.form.user.id === 0) {
        this.form.user = null
      } else {
        this.form.user = this.form.user.id
      }

      for (const item in this.roles) {
        if (this.roles[item] !== undefined) {
          this.roles[item] = this.roles[item].id
        }
      }

      this.form.role = this.roles

      const formData = {
        user: this.form.user,
        roles: this.roles
      }

      this.$q.loading.show()

      if (this.type === 'create') {
        this.CreateRoleUser(app, formData)
      } else {
        this.UpdateRoleUser(app, formData)
      }
    },

    CreateRoleUser (app, formData) {
      this.$axios.post(process.env.api + 'api/admin/acl/role_user/create/update/', formData)
        .then(function () {
          app.showNotif('نقش-کاربری های مورد نظر با موفقیت ثبت شد', 'mdi-checkbox-marked-circle-outline ', 'green')
          app.$parent.$parent.GetAllRoleUsers()
          app.$parent.$parent.GetUsersListAndRolesList()
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

    UpdateRoleUser (app, formData) {
      this.$axios.put(process.env.api + 'api/admin/acl/role_user/create/update/?id=' + app.form.id + '/', formData)
        .then(function () {
          app.showNotif('نقش-کاربری های مورد نظر با موفقیت ویرایش شد', 'mdi-checkbox-marked-circle-outline ', 'green')
          app.$parent.$parent.GetAllRoleUsers()
          app.$parent.$parent.GetUsersListAndRolesList()
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
        this.roles = []
      } else {
        if (this.form.role) {
          this.roles.push(this.form.role)
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
