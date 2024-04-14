<template>
  <div class="q-pa-md">
    <div class="q-gutter-y-md">
      <q-card>
        <q-tabs
          align="left"
          v-model="tab"
          class="text-teal text-info"
        >
          <q-tab class="text-primary" name="active_notifyusers_list" icon="mdi-format-list-text"
                 label="اطلاع رسانی های فعال"/>
          <q-tab class="text-primary" name="inactive_notifyusers_list" icon="mdi-format-list-text"
                 label="اطلاع رسانی های غیر فعال"/>
        </q-tabs>
        <q-separator/>

        <q-tab-panels v-model="tab" animated>
          <q-tab-panel name="active_notifyusers_list">
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
                     label="افزودن اطلاع رسانی"/>
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
                    <q-td key="product">{{ props.row.product.title }}</q-td>
                    <q-td key="user">{{ props.row.user.username }}</q-td>
                    <q-td key="original_image">
                      <q-img
                        :src="ShowImage(props.row.product.original_image)"
                        spinner-color="white"
                        style="height: 80px; max-width: 60px"
                      />
                    </q-td>
                    <q-td key="created_at">{{ props.row.created_at | FormatDate }}</q-td>
                    <q-td key="setting">
                      <q-btn
                        @click="EditUserNotify(props.row.id , props.row.user , props.row.product , props.row.active)"
                        style="color: #4facfe" rounded
                        icon="mdi-square-edit-outline" label="ویرایش" size="md" flat
                        dense>
                        <q-tooltip>ویرایش</q-tooltip>
                      </q-btn>
                      |
                      <q-btn
                        @click="DeleteUserNotify(props.row.user.username + '-' +  props.row.product.title , props.row.id)"
                        style="color: red" rounded
                        icon="mdi-trash-can-outline" label="حذف" size="md" flat dense>
                        <q-tooltip>حذف</q-tooltip>
                      </q-btn>
                      |
                      <q-btn
                        @click="SetStatusInActive(props.row.user.username + '-' +  props.row.product.title , props.row.id)"
                        style="color: red" rounded
                        icon="mdi-close-outline" label="غیر فعال کردن" size="md" flat dense>
                        <q-tooltip>غیر فعال کردن</q-tooltip>
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

          <q-tab-panel name="inactive_notifyusers_list">
            <q-input style="width: 300px; float: left !important;"
                     dense v-model.lazy="search"
                     debounce="250"
                     filled type="search">
              <template v-slot:append>
                <q-icon name="search"/>
              </template>
            </q-input>

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
                    <q-td key="product">{{ props.row.product.title }}</q-td>
                    <q-td key="user">{{ props.row.user.username }}</q-td>
                    <q-td key="original_image">
                      <q-img
                        :src="ShowImage(props.row.product.original_image)"
                        spinner-color="white"
                        style="height: 80px; max-width: 60px"
                      />
                    </q-td>
                    <q-td key="created_at">{{ props.row.created_at | FormatDate }}</q-td>
                    <q-td key="setting">
                      <q-btn
                        @click="EditUserNotify(props.row.id , props.row.user , props.row.product , props.row.active)"
                        style="color: #4facfe" rounded
                        icon="mdi-square-edit-outline" label="ویرایش" size="md" flat
                        dense>
                        <q-tooltip>ویرایش</q-tooltip>
                      </q-btn>
                      |
                      <q-btn
                        @click="DeleteUserNotify(props.row.user.username + '-' +  props.row.product.title , props.row.id)"
                        style="color: red" rounded
                        icon="mdi-trash-can-outline" label="حذف" size="md" flat dense>
                        <q-tooltip>حذف</q-tooltip>
                      </q-btn>
                      |
                      <q-btn
                        @click="SetStatusActive(props.row.user.username + '-' +  props.row.product.title , props.row.id)"
                        style="color: green" rounded
                        icon="mdi-shield-check-outline" label="فعال کردن" size="md" flat dense>
                        <q-tooltip>فعال کردن</q-tooltip>
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

        <Modal :showDialog.sync="showDialog" :form="form" :type="type" :products_list="products_list"
               :users_list="users_list" :request_type="request_type"></Modal>
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
      request_type: 'active',

      form: {},

      search: '',

      data: [],
      products_list: [],
      users_list: [],

      paginationPage: 1,
      lastPage: 0,
      pages_count: 0,

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
          name: 'product',
          align: 'left',
          label: 'محصول',
          field: 'product',
          sortable: true
        },
        {
          name: 'user',
          align: 'left',
          label: 'کاربر',
          field: 'user',
          sortable: true
        },
        {
          name: 'original_image',
          align: 'left',
          label: 'عکس محصول',
          field: 'original_image',
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

      tab: 'active_notifyusers_list',
      splitterModel: 20,
      showDialog: false
    }
  },

  filters: {
    FormatDate (date) {
      return moment(date).format('HH:mm  YYYY-MM-DD')
    }
  },

  methods: {
    ShowImage (url) {
      return url.replace('http://localhost:8000/', process.env.api)
    },

    SetStatusInActive (title, id) {
      const app = this

      this.$q.dialog({
        title: 'هشدار',
        message: 'آیا میخواهید وضعیت تایید اطلاع رسانی ' + ' ( ' + title + ' ) ' + 'نقض شود ؟ ',
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
        const formData = new FormData()
        formData.append('id', id)
        formData.append('type', 'inactive')

        app.$axios.post(process.env.api + 'api/admin/products/notify_users/change/active/', formData)
          .then(function () {
            if (app.paginationPage === app.lastPage && app.data.length === 1) {
              app.paginationPage -= 1
            } else {
              app.GetAllActiveUserNotifies()
            }
            app.showNotif('اطلاع رسانی مورد نظر با موفقیت از فعال ها حذف شد', 'mdi-checkbox-marked-circle-outline', 'green')
          })
      })
    },

    SetStatusActive (title, id) {
      const app = this

      this.$q.dialog({
        title: 'هشدار',
        message: 'آیا میخواهید وضعیت فعال اطلاع رسانی ' + ' ( ' + title + ' ) ' + 'نقض شود ؟ ',
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
        const formData = new FormData()
        formData.append('id', id)
        formData.append('type', 'active')

        app.$axios.post(process.env.api + 'api/admin/products/notify_users/change/active/', formData)
          .then(function () {
            if (app.paginationPage === app.lastPage && app.data.length === 1) {
              app.paginationPage -= 1
            } else {
              app.GetAllInActiveUserNotifies()
            }
            app.showNotif('اطلاع رسانی مورد نظر با موفقیت از غیر فعال ها حذف شد', 'mdi-checkbox-marked-circle-outline', 'green')
          })
      })
    },

    GetRequiredLists () {
      const app = this

      this.$axios.get(process.env.api + 'api/admin/products/users/list/')
        .then(function (response) {
          app.users_list = response.data
        })

      this.$axios.get(process.env.api + 'api/admin/products/WithOutPagination')
        .then(function (response) {
          app.products_list = response.data
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

    DeleteUserNotify (name, id) {
      const app = this
      this.$q.dialog({
        title: 'هشدار',
        message: 'آیا میخواهید اطلاع رسانی ' + ' ( ' + name + ' ) ' + 'حذف شود ؟ ',
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
        if (app.request_type === 'active') {
          app.$axios.delete(process.env.api + 'api/admin/products/notify_users/active/' + id)
            .then(function () {
              app.showNotif('اطلاع رسانی مورد نظر با موفقیت حذف شد', 'mdi-checkbox-marked-circle-outline', 'green')

              if (app.paginationPage === app.lastPage && app.data.length === 1) {
                app.paginationPage -= 1
              } else {
                app.GetAllActiveUserNotifies()
              }
            })
            .catch(function () {
              app.showNotif('مشکلی به وجود آمده است')
            })
        } else {
          app.$axios.delete(process.env.api + 'api/admin/products/notify_users/inactive/' + id)
            .then(function () {
              app.showNotif('اطلاع رسانی مورد نظر با موفقیت حذف شد', 'mdi-checkbox-marked-circle-outline', 'green')

              if (app.paginationPage === app.lastPage && app.data.length === 1) {
                app.paginationPage -= 1
              } else {
                app.GetAllInActiveUserNotifies()
              }
            })
            .catch(function () {
              app.showNotif('مشکلی به وجود آمده است')
            })
        }
      })
    },

    EditUserNotify (id, user, product) {
      const app = this

      this.$q.loading.show()
      if (this.request_type === 'active') {
        this.$axios.get(process.env.api + 'api/admin/products/notify_users/active/' + id + '/')
          .then(function (response) {
            app.form = response.data
            app.form.author = user
            app.form.product = product

            app.setDialog('edit')

            app.$q.loading.hide()
          })
      } else {
        this.$axios.get(process.env.api + 'api/admin/products/notify_users/inactive/' + id + '/')
          .then(function (response) {
            app.form = response.data
            app.form.author = user
            app.form.product = product

            app.setDialog('edit')

            app.$q.loading.hide()
          })
      }
    },

    GetAllActiveUserNotifies () {
      const app = this

      this.$q.loading.show()

      this.$axios.get(process.env.api + 'api/admin/products/notify_users/active/?page=' + app.paginationPage + '&search=' + app.search)
        .then(function (response) {
          app.data = response.data.results
          app.lastPage = response.data.last_page

          app.$q.loading.hide()
        })
    },

    GetAllInActiveUserNotifies () {
      const app = this

      this.$q.loading.show()

      this.$axios.get(process.env.api + 'api/admin/products/notify_users/inactive/?page=' + app.paginationPage + '&search=' + app.search)
        .then(function (response) {
          app.data = response.data.results
          app.lastPage = response.data.last_page

          app.$q.loading.hide()
        })
    }
  },

  watch: {
    search () {
      if (this.paginationPage === 0) {
        this.paginationPage = 1
      }
      if (this.tab === 'inactive_notifyusers_list') {
        this.GetAllInActiveUserNotifies()
      } else {
        this.GetAllActiveUserNotifies()
      }
    },
    paginationPage () {
      if (this.paginationPage === 0) {
        this.paginationPage = 1
      }
      if (this.tab === 'inactive_notifyusers_list') {
        this.GetAllInActiveUserNotifies()
      } else {
        this.GetAllActiveUserNotifies()
      }
    },

    tab (value) {
      this.paginationPage = 1

      if (value === 'inactive_notifyusers_list') {
        this.request_type = 'inactive'
        this.GetAllInActiveUserNotifies()
      } else {
        this.request_type = 'active'
        this.GetAllActiveUserNotifies()
      }
    }
  },

  components: {
    Modal
  },

  mounted () {
    this.GetAllActiveUserNotifies()
    this.GetRequiredLists()
  }
}
</script>

<style scoped>
body {
  background-color: #f5f5f5 !important;
}
</style>
