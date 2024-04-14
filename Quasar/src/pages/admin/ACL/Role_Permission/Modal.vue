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
            <q-select class="col-12" v-model="form.role" map-options
                      :options="role_list" option-value="id"
                      option-label="title" label="نقش*"/>
          </q-item>

          <q-item class="col-lg-12 col-md-6 col-sm-12 col-xs-12">
            <q-select
              map-options
              class="col-12"
              v-model="permissions"
              multiple
              :options="permission_list"
              option-label="title"
              option-value="id"
              use-chips
              stack-label
              label="دسترسی (میتوانید چند دسترسی را انتخاب کنید)*"
            />
          </q-item>

          <q-card-actions class="bg-white text-teal">
            <q-btn flat label="انصراف" v-close-popup/>
            <q-btn flat :label="type === 'edit' ?  'ویرایش نقش-دسترسی': 'ثبت نقش-دسترسی'" type="submit"/>
          </q-card-actions>

        </q-form>
      </q-card-section>
    </q-card>
  </q-dialog>
</template>
<script>
export default {
  props: ['showDialog', 'form', 'type', 'permission_list', 'role_list'],

  data () {
    return {
      permissions: []
    }
  },

  methods: {
    onSubmit () {
      const app = this

      if (this.form.role === undefined || this.form.role === null) {
        this.showNotif('فیلد نقش اجباری است')
        return
      }

      if (this.permissions.length === 0) {
        this.showNotif('فیلد دسترسی اجباری است')
        return
      }

      if (!this.form.role || this.form.role.id === 0) {
        this.form.role = null
      } else {
        this.form.role = this.form.role.id
      }

      for (const item in this.permissions) {
        if (this.permissions[item] !== undefined && typeof this.permissions[item] !== 'number') {
          this.permissions[item] = this.permissions[item].id
        }
      }

      this.form.permission = this.permissions

      const formData = {
        role: this.form.role,
        permissions: this.permissions
      }

      this.$q.loading.show()

      if (this.type === 'create') {
        this.CreateRolePermission(app, formData)
      } else {
        this.UpdateRolePermission(app, formData)
      }
    },

    CreateRolePermission (app, formData) {
      this.$axios.post(process.env.api + 'api/admin/acl/role_permission/create/update/', formData)
        .then(function () {
          app.showNotif('نقش-کاربری های مورد نظر با موفقیت ثبت شد', 'mdi-checkbox-marked-circle-outline ', 'green')
          app.$parent.$parent.GetAllRolePermissions()
          app.$parent.$parent.GetPermissionsListAndRolesList()
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

    UpdateRolePermission (app, formData) {
      this.$axios.put(process.env.api + 'api/admin/acl/role_permission/create/update/?id=' + app.form.id + '/', formData)
        .then(function () {
          app.showNotif('نقش-کاربری های مورد نظر با موفقیت ویرایش شد', 'mdi-checkbox-marked-circle-outline ', 'green')
          app.$parent.$parent.GetAllRolePermissions()
          app.$parent.$parent.GetPermissionsListAndRolesList()
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
        this.permissions = []
      } else {
        if (this.form.permission) {
          this.permissions.push(this.form.permission)
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
