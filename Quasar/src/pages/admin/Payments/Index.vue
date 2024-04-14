<template>
  <div class="q-pa-md">
    <div class="q-gutter-y-md">
      <q-card>
        <q-tabs
          align="left"
          v-model="tab"
          class="text-teal text-info"
        >
          <q-tab class="text-primary" name="successful_payments_list" icon="mdi-format-list-text"
                 label="پرداخت ها موفق"/>
          <q-tab class="text-primary" name="unsuccessful_payments_list" icon="mdi-format-list-text"
                 label="پرداخت ها نا موفق"/>
        </q-tabs>
        <q-separator/>

        <q-tab-panels v-model="tab" animated>
          <q-tab-panel name="successful_payments_list">
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
                     label="افزودن پرداخت"/>
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
                    <q-td key="user">{{ props.row.user ? props.row.user.username : '' }}</q-td>
                    <q-td key="amount">{{ props.row.amount }}</q-td>
                    <q-td key="ref_code">{{ props.row.ref_code }}</q-td>
                    <q-td key="coupon">{{ props.row.coupon ? props.row.coupon.code : '' }}</q-td>
                    <q-td key="created_at">{{ props.row.created_at | FormatDate }}</q-td>
                    <q-td key="setting">
                      <q-btn
                        @click="EditPayment(props.row.id , props.row.user , props.row.status)"
                        style="color: #4facfe" rounded
                        icon="mdi-square-edit-outline" label="ویرایش" size="md" flat
                        dense>
                        <q-tooltip>ویرایش</q-tooltip>
                      </q-btn>
                      |
                      <q-btn @click="DeletePayment(props.row.user.username , props.row.id)" style="color: red" rounded
                             icon="mdi-trash-can-outline" label="حذف" size="md" flat dense>
                        <q-tooltip>حذف</q-tooltip>
                      </q-btn>
                      |
                      <q-btn @click="SetStatusUnSuccess(props.row.user.username , props.row.id)" style="color: red" rounded
                             icon="mdi-close-outline" label="ناموفق کردن" size="md" flat dense>
                        <q-tooltip>ناموفق کردن</q-tooltip>
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

          <q-tab-panel name="unsuccessful_payments_list">
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
                    <q-td key="user">{{ props.row.user.username }}</q-td>
                    <q-td key="amount">{{ props.row.amount }}</q-td>
                    <q-td key="ref_code">{{ props.row.ref_code }}</q-td>
                     <q-td key="coupon">{{ props.row.coupon ? props.row.coupon.code : '' }}</q-td>
                    <q-td key="created_at">{{ props.row.created_at | FormatDate }}</q-td>
                    <q-td key="setting">
                      <q-btn
                        @click="EditPayment(props.row.id , props.row.user , props.row.status)"
                        style="color: #4facfe" rounded
                        icon="mdi-square-edit-outline" label="ویرایش" size="md" flat
                        dense>
                        <q-tooltip>ویرایش</q-tooltip>
                      </q-btn>
                      |
                      <q-btn @click="DeletePayment(props.row.user.username , props.row.id)" style="color: red" rounded
                             icon="mdi-trash-can-outline" label="حذف" size="md" flat dense>
                        <q-tooltip>حذف</q-tooltip>
                      </q-btn>
                      |
                      <q-btn @click="SetStatusSuccess(props.row.user.username , props.row.id)" style="color: green" rounded
                             icon="mdi-shield-check-outline" label="موفق کردن" size="md" flat dense>
                        <q-tooltip>موفق کردن</q-tooltip>
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

        <Modal :showDialog.sync="showDialog" :form="form" :type="type"
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
      request_type: 'successful',

      form: {},

      search: '',

      data: [],
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
          name: 'user',
          align: 'left',
          label: 'کاربر',
          field: 'user',
          sortable: true
        },
        {
          name: 'amount',
          align: 'left',
          label: 'مبلغ',
          field: 'amount',
          sortable: true
        },
        {
          name: 'ref_code',
          align: 'left',
          label: 'کد پیگیری',
          field: 'ref_code',
          sortable: true
        },
        {
          name: 'coupon',
          align: 'left',
          label: 'کد تخفیف',
          field: 'coupon',
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

      tab: 'successful_payments_list',
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
    SetStatusSuccess (title, id) {
      const app = this

      this.$q.dialog({
        title: 'هشدار',
        message: 'آیا میخواهید وضعیت تایید پرداخت ' + ' ( ' + title + ' ) ' + 'نقض شود ؟ ',
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
        formData.append('type', 'success')

        app.$axios.post(process.env.api + 'api/admin/payments/change/status/', formData)
          .then(function () {
            if (app.paginationPage === app.lastPage && app.data.length === 1) {
              app.paginationPage -= 1
            } else {
              app.GetAllUnSuccessfulPayments()
            }
            app.showNotif('پرداخت مورد نظر با موفقیت به موفق ها منتقل شد', 'mdi-checkbox-marked-circle-outline', 'green')
          })
      })
    },

    SetStatusUnSuccess (title, id) {
      const app = this

      this.$q.dialog({
        title: 'هشدار',
        message: 'آیا میخواهید وضعیت تایید پرداخت ' + ' ( ' + title + ' ) ' + 'نقض شود ؟ ',
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
        formData.append('type', 'unsuccess')

        app.$axios.post(process.env.api + 'api/admin/payments/change/status/', formData)
          .then(function () {
            if (app.paginationPage === app.lastPage && app.data.length === 1) {
              app.paginationPage -= 1
            } else {
              app.GetAllSuccessfulPayments()
            }
            app.showNotif('پرداخت مورد نظر با موفقیت به ناموفق ها منتقل شد', 'mdi-checkbox-marked-circle-outline', 'green')
          })
      })
    },

    GetRequiredLists () {
      const app = this

      this.$axios.get(process.env.api + 'api/admin/products/users/list/')
        .then(function (response) {
          app.users_list = response.data
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

    DeletePayment (name, id) {
      const app = this
      this.$q.dialog({
        title: 'هشدار',
        message: 'آیا میخواهید پرداخت مورد نظر حذف شود؟',
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
        if (app.request_type === 'successful') {
          app.$axios.delete(process.env.api + 'api/admin/payments/successful/' + id)
            .then(function () {
              app.showNotif('پرداخت مورد نظر با موفقیت حذف شد', 'mdi-checkbox-marked-circle-outline', 'green')

              if (app.paginationPage === app.lastPage && app.data.length === 1) {
                app.paginationPage -= 1
              } else {
                app.GetAllSuccessfulPayments()
              }
            })
            .catch(function () {
              app.showNotif('مشکلی به وجود آمده است')
            })
        } else {
          app.$axios.delete(process.env.api + 'api/admin/payments/unsuccessful/' + id)
            .then(function () {
              app.showNotif('پرداخت مورد نظر با موفقیت حذف شد', 'mdi-checkbox-marked-circle-outline', 'green')

              if (app.paginationPage === app.lastPage && app.data.length === 1) {
                app.paginationPage -= 1
              } else {
                app.GetAllUnSuccessfulPayments()
              }
            })
            .catch(function () {
              app.showNotif('مشکلی به وجود آمده است')
            })
        }
      })
    },

    EditPayment (id) {
      const app = this

      this.$q.loading.show()
      if (this.request_type === 'successful') {
        this.$axios.get(process.env.api + 'api/admin/payments/successful/' + id + '/')
          .then(function (response) {
            app.form = response.data

            app.setDialog('edit')

            app.$q.loading.hide()
          })
      } else {
        this.$axios.get(process.env.api + 'api/admin/payments/unsuccessful/' + id + '/')
          .then(function (response) {
            app.form = response.data

            app.setDialog('edit')

            app.$q.loading.hide()
          })
      }
    },

    GetAllSuccessfulPayments () {
      const app = this

      this.$q.loading.show()

      this.$axios.get(process.env.api + 'api/admin/payments/successful/?page=' + app.paginationPage + '&search=' + app.search)
        .then(function (response) {
          app.data = response.data.results
          app.lastPage = response.data.last_page

          app.$q.loading.hide()
        })
    },

    GetAllUnSuccessfulPayments () {
      const app = this

      this.$q.loading.show()

      this.$axios.get(process.env.api + 'api/admin/payments/unsuccessful/?page=' + app.paginationPage + '&search=' + app.search)
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
      if (this.tab === 'successful_payments_list') {
        this.GetAllSuccessfulPayments()
      } else {
        this.GetAllUnSuccessfulPayments()
      }
    },
    paginationPage () {
      if (this.paginationPage === 0) {
        this.paginationPage = 1
      }
      if (this.tab === 'successful_payments_list') {
        this.GetAllSuccessfulPayments()
      } else {
        this.GetAllUnSuccessfulPayments()
      }
    },

    tab (value) {
      this.paginationPage = 1

      if (value === 'successful_payments_list') {
        this.request_type = 'successful'
        this.GetAllSuccessfulPayments()
      } else {
        this.request_type = 'unsuccessful'
        this.GetAllUnSuccessfulPayments()
      }
    }
  },

  components: {
    Modal
  },

  mounted () {
    this.GetAllSuccessfulPayments()
    this.GetRequiredLists()
  }
}
</script>

<style scoped>
body {
  background-color: #f5f5f5 !important;
}
</style>
