<template>
  <div class="q-pa-md">
    <div class="q-gutter-y-md">
      <q-card>
        <q-tabs
          align="left"
          v-model="tab"
          class="text-teal text-info"
        >
          <q-tab class="text-primary" name="role_permission_list" icon="mdi-format-list-text" label="نقش-دسترسی"/>
        </q-tabs>
        <q-separator/>

        <q-tab-panels v-model="tab" animated>
          <q-tab-panel name="role_permission_list">
            <q-input style="width: 300px; float: left !important;"
                     dense v-model.lazy="search"
                     debounce="250"
                     filled type="search">
              <template v-slot:append>
                <q-icon name="search"/>
              </template>
            </q-input>

            <div class="q-pl-md q-gutter-sm">
              <q-btn color="primary" outline @click="setDialog('create')" icon="mdi-file-plus-outline"
                     label="افزودن نقش-دسترسی"/>
            </div>
            <div class="q-pa-md">
              <q-table
                :data="data"
                :columns="columns"
                :loading="loading"
                row-key="id"
                :rows-per-page-options="[10]"
                binary-state-sort
                flat
                separator="horizontal"
                color="brand"
              >
                <template v-slot:body="props">
                  <q-tr :props="props">
                    <q-td key="id">{{ props.rowIndex + 1 }}</q-td>
                    <q-td key="role">{{ props.row.role.title }}</q-td>
                    <q-td key="permission">{{ props.row.permission.title }}</q-td>
                    <q-td key="created_at">{{ props.row.created_at | FormatDate }}</q-td>
                    <q-td key="setting">
                      <q-btn @click="EditRolePermission(props.row.id , props.row.role , props.row.permission)"
                             style="color: #4facfe" rounded
                             icon="mdi-square-edit-outline" label="ویرایش" size="md" flat
                             dense>
                        <q-tooltip>ویرایش</q-tooltip>
                      </q-btn>
                      |
                      <q-btn
                        @click="DeleteRolePermission(props.row.role.title + '-' + props.row.permission.title , props.row.id)"
                        style="color: red" rounded
                        icon="mdi-trash-can-outline" label="حذف" size="md" flat dense>
                        <q-tooltip>حذف</q-tooltip>
                      </q-btn>
                    </q-td>
                  </q-tr>
                </template>
              </q-table>

              <div class="row justify-center q-mt-md" style="direction: ltr">
                <q-pagination v-model="paginationPage" color="teal" :max="lastPage" :max-pages="6"
                              :boundary-numbers="true" size="sm"/>
              </div>

            </div>
          </q-tab-panel>
        </q-tab-panels>

        <Modal :showDialog.sync="showDialog" :form="form" :type="type" :permission_list="permission_list"
               :role_list="role_list"></Modal>
      </q-card>
    </div>
  </div>
</template>

<script>
import Modal from './Modal.vue'

import moment from 'moment'

export default {
  data () {
    return {
      type: 'create',

      form: {},

      search: '',

      data: [],
      permission_list: [],
      role_list: [],

      paginationPage: 1,
      lastPage: 0,

      loading: false,
      columns: [
        {
          name: 'id',
          required: true,
          label: 'ردیف',
          align: 'left',
          field: row => row.name,
          sortable: true
        },
        {
          name: 'role',
          align: 'left',
          label: 'نقش',
          field: 'role',
          sortable: true
        },
        {
          name: 'permission',
          align: 'left',
          label: 'دسترسی',
          field: 'permission',
          sortable: true
        },
        {
          name: 'created_at',
          align: 'left',
          label: 'تاریخ ثبت',
          field: 'created_at',
          sortable: true
        },
        {
          name: 'setting',
          align: 'left',
          label: 'عملیات',
          field: 'setting',
          sortable: true
        }
      ],

      tab: 'role_permission_list',
      splitterModel: 20,
      showDialog: false
    }
  },
  methods: {
    GetPermissionsListAndRolesList () {
      const app = this

      app.$q.loading.show()

      this.$axios.get(process.env.api + 'api/admin/acl/permissions/all/WithOutPagination/')
        .then(function (response) {
          app.permission_list = response.data
        })

      this.$axios.get(process.env.api + 'api/admin/acl/roles/all/WithOutPagination/')
        .then(function (response) {
          app.role_list = response.data

          app.$q.loading.hide()
        })
    },

    NullData () {
      for (const item in this.form) {
        this.form[item] = ''
      }
    },

    setDialog (type = 'create') {
      this.type = type

      if (type !== 'edit') {
        this.NullData()
      }

      this.showDialog = true
    },

    showNotif (message, icon = 'error', color = 'red', time = 3000) {
      this.$q.notify({
        message: message,
        icon: icon,
        color: color,
        position: 'bottom-right',
        timeout: time,
        progress: true
      })
    },

    DeleteRolePermission (name, id) {
      const app = this
      this.$q.dialog({
        title: 'هشدار',
        message: 'آیا میخواهید نقش-دسترسی ' + ' ( ' + name + ' ) ' + 'حذف شود ؟ ',
        ok: {
          push: true,
          label: 'تایید'
        },
        cancel: {
          push: true,
          color: 'negative'
        },
        persistent: true
      }).onOk(() => {
        app.$axios.delete(process.env.api + 'api/admin/acl/role_permission/' + id)
          .then(function () {
            app.showNotif('نقش-دسترسی مورد نظر با موفقیت حذف شد', 'mdi-checkbox-marked-circle-outline', 'green')
            app.GetAllRolePermissions()
            app.GetPermissionsListAndRolesList()
          })
          .catch(function () {
            app.showNotif('مشکلی به وجود آمده است')
          })
      })
    },

    EditRolePermission (id, role, permission) {
      const app = this

      this.$axios.get(process.env.api + 'api/admin/acl/role_permission/' + id + '/')
        .then(function (response) {
          app.form = response.data
          app.form.permission = permission
          app.form.role = role

          app.setDialog('edit')
          app.$q.loading.hide()
        })
    },

    GetAllRolePermissions () {
      const app = this

      this.$q.loading.show()

      this.$axios.get(process.env.api + 'api/admin/acl/role_permission/?page=' + app.paginationPage + '&search=' + app.search)
        .then(function (response) {
          app.data = response.data.results
          app.lastPage = response.data.last_page

          app.$q.loading.hide()
        })
    }
  },

  filters: {
    FormatDate (date) {
      return moment(date).format('HH:mm  YYYY-MM-DD')
    }
  },

  watch: {
    search () {
      this.GetAllRolePermissions()
    },
    paginationPage () {
      this.GetAllRolePermissions()
    }
  },

  components: {
    Modal
  },

  mounted () {
    this.GetAllRolePermissions()
    this.GetPermissionsListAndRolesList()
  }
}
</script>

<style scoped>
body {
  background-color: #f5f5f5 !important;
}
</style>
