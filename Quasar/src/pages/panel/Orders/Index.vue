<template>
  <div class="q-pa-md">
    <div class="q-gutter-y-md">
      <q-card>
        <q-tabs
          align="left"
          v-model="tab"
          class="text-teal text-info"
        >
          <q-tab class="text-primary" name="successful_orders_list" icon="mdi-format-list-text"
                 label="سفارشات موفق"/>
          <q-tab class="text-primary" name="unsuccessful_orders_list" icon="mdi-format-list-text"
                 label="سفارشات ناموفق"/>
        </q-tabs>
        <q-separator/>

        <q-tab-panels v-model="tab" animated>
          <q-tab-panel name="successful_orders_list">
            <q-input style="width: 300px; float: left !important;"
                     dense v-model.lazy="search"
                     debounce="250"
                     filled type="search">
              <template v-slot:append>
                <q-icon name="search"/>
              </template>
            </q-input>

            <div class="q-pl-md q-gutter-sm">
              <q-btn color="primary" disable outline @click="setDialog('create')" icon="mdi-file-plus-outline"
                     label="افزودن سفارش"/>
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
                    <q-td key="product">{{ props.row.product ? props.row.product.title : '' }}</q-td>
                    <q-td key="amount">{{ props.row.product ? props.row.product.price : '' }}</q-td>
                    <q-td key="payment">{{ props.row.payment ? props.row.payment.ref_code : '' }}</q-td>
                    <q-td key="size">{{ props.row.size ? props.row.size.title : '' }}</q-td>
                    <q-td key="color">{{ props.row.color ? props.row.color.name : '' }}</q-td>
                    <q-td key="count">{{ props.row.count }}</q-td>
                    <q-td key="name">{{ props.row.name }}</q-td>
                    <q-td key="family">{{ props.row.family }}</q-td>
                    <q-td key="phone">{{ props.row.phone }}</q-td>
                    <q-td key="address1">{{ props.row.address1 }}</q-td>
                    <q-td key="post_code">{{ props.row.post_code }}</q-td>
                    <q-td key="payment_type">
                      <q-badge outline :color="ShowPaymentTypeColor(props.row.payment_type)"
                               :label="ShowPaymentType(props.row.payment_type)"/>
                    </q-td>
                    <q-td key="status">
                      <q-badge outline :color="ShowStatusTypeColor(props.row.status)"
                               :label="ShowStatus(props.row.status)"/>
                    </q-td>
                    <q-td key="created_at">{{ props.row.created_at | FormatDate }}</q-td>
                    <q-td key="setting">
                      <q-btn @click="DeleteOrder(props.row.user.username , props.row.id)" style="color: red" rounded
                             icon="mdi-trash-can-outline" label="حذف" size="md" flat dense>
                        <q-tooltip>حذف</q-tooltip>
                      </q-btn>
                      |
                      <q-btn @click="SetStatusUnSuccess(props.row.user.username , props.row.id)" style="color: red"
                             rounded
                             icon="mdi-close-outline" label="تبدیل به ارسال شده" size="md" flat dense>
                        <q-tooltip>تبدیل به ارسال شده</q-tooltip>
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

          <q-tab-panel name="unsuccessful_orders_list">
            <q-input style="width: 300px; float: left !important;"
                     dense v-model.lazy="search"
                     debounce="250"
                     filled type="search">
              <template v-slot:append>
                <q-icon name="search"/>
              </template>
            </q-input>

            <div class="q-pl-md q-gutter-sm">
              <q-btn color="primary" disable outline @click="setDialog('create')" icon="mdi-file-plus-outline"
                     label="افزودن سفارش"/>
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
                    <q-td key="product">{{ props.row.product ? props.row.product.title : '' }}</q-td>
                    <q-td key="amount">{{ props.row.product ? props.row.product.price : '' }}</q-td>
                    <q-td key="payment">{{ props.row.payment ? props.row.payment.ref_code : '' }}</q-td>
                    <q-td key="size">{{ props.row.size ? props.row.size.title : '' }}</q-td>
                    <q-td key="color">{{ props.row.color ? props.row.color.name : '' }}</q-td>
                    <q-td key="count">{{ props.row.count }}</q-td>
                    <q-td key="name">{{ props.row.name }}</q-td>
                    <q-td key="family">{{ props.row.family }}</q-td>
                    <q-td key="phone">{{ props.row.phone }}</q-td>
                    <q-td key="address1">{{ props.row.address1 }}</q-td>
                    <q-td key="post_code">{{ props.row.post_code }}</q-td>
                    <q-td key="payment_type">
                      <q-badge outline :color="ShowPaymentTypeColor(props.row.payment_type)"
                               :label="ShowPaymentType(props.row.payment_type)"/>
                    </q-td>
                    <q-td key="status">
                      <q-badge outline :color="ShowStatusTypeColor(props.row.status)"
                               :label="ShowStatus(props.row.status)"/>
                    </q-td>
                    <q-td key="created_at">{{ props.row.created_at | FormatDate }}</q-td>
                    <q-td key="setting">
                      <q-btn @click="DeleteOrder(props.row.user.username , props.row.id)" style="color: red" rounded
                             icon="mdi-trash-can-outline" label="حذف" size="md" flat dense>
                        <q-tooltip>حذف</q-tooltip>
                      </q-btn>
                      |
                      <q-btn @click="SetStatusSuccess(props.row.user.username , props.row.id)" style="color: green"
                             rounded
                             icon="mdi-shield-check-outline" label="تبدیل به دریافت شده" size="md" flat dense>
                        <q-tooltip>تبدیل به دریافت شده</q-tooltip>
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
      </q-card>
    </div>
  </div>
</template>

<script>
import moment from 'moment'

export default {
  data () {
    return {
      type: 'create',
      request_type: 'successful',

      // form: {},

      search: '',

      data: [],
      // users_list: [],

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
          name: 'product',
          align: 'left',
          label: 'محصول',
          field: 'product',
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
          name: 'payment',
          align: 'left',
          label: 'پرداختی',
          field: 'payment',
          sortable: true
        },
        {
          name: 'size',
          align: 'left',
          label: 'سایز',
          field: 'size',
          sortable: true
        },
        {
          name: 'color',
          align: 'left',
          label: 'رنگ',
          field: 'color',
          sortable: true
        },
        {
          name: 'count',
          align: 'left',
          label: 'تعداد',
          field: 'count',
          sortable: true
        },
        {
          name: 'name',
          align: 'left',
          label: 'نام',
          field: 'name',
          sortable: true
        },
        {
          name: 'family',
          align: 'left',
          label: 'نام خانوادگی',
          field: 'family',
          sortable: true
        },
        {
          name: 'phone',
          align: 'left',
          label: 'موبایل',
          field: 'phone',
          sortable: true
        },
        {
          name: 'address1',
          align: 'left',
          label: 'آدرس 1',
          field: 'address1',
          sortable: true
        },
        {
          name: 'post_code',
          align: 'left',
          label: 'آدرس 2',
          field: 'post_code',
          sortable: true
        },
        {
          name: 'payment_type',
          align: 'left',
          label: 'نوع پرداخت',
          field: 'payment_type',
          sortable: true
        },
        {
          name: 'status',
          align: 'left',
          label: 'وضعیت',
          field: 'status',
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

      tab: 'successful_orders_list',
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
    ShowPaymentType (type) {
      if (type === 'online') {
        return 'آنلاین'
      }
      return 'نقدی (حضوری)'
    },

    ShowPaymentTypeColor (type) {
      if (type === 'online') {
        return 'orange'
      }

      return 'red'
    },

    ShowStatus (type) {
      if (type === 'sending') {
        return 'درحال ارسال'
      } else if (type === 'posted') {
        return 'ارسال شده'
      }
      return 'دریافت شده'
    },

    ShowStatusTypeColor (type) {
      if (type === 'sending') {
        return 'red'
      } else if (type === 'posted') {
        return 'orange'
      }

      return 'secondary'
    },

    SetStatusSuccess (title, id) {
      const app = this

      this.$q.dialog({
        title: 'هشدار',
        message: 'آیا میخواهید وضعیت ارسال سفارش ' + ' ( ' + title + ' ) ' + 'به دریافت شده تغییر پیدا کند ؟ ',
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

        app.$axios.post(process.env.api + 'api/admin/orders/change/status/', formData)
          .then(function () {
            if (app.paginationPage === app.lastPage && app.data.length === 1) {
              app.paginationPage -= 1
            } else {
              app.GetAllUnSuccessfulOrders()
            }
            app.showNotif('پرداخت مورد نظر با موفقیت به موفق ها منتقل شد', 'mdi-checkbox-marked-circle-outline', 'green')
          })
      })
    },

    SetStatusUnSuccess (title, id) {
      const app = this

      this.$q.dialog({
        title: 'هشدار',
        message: 'آیا میخواهید وضعیت ارسال سفارش ' + ' ( ' + title + ' ) ' + 'به ارسال شده تغییر پیدا کند ؟ ',
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

        app.$axios.post(process.env.api + 'api/admin/orders/change/status/', formData)
          .then(function () {
            if (app.paginationPage === app.lastPage && app.data.length === 1) {
              app.paginationPage -= 1
            } else {
              app.GetAllSuccessfulOrders()
            }
            app.showNotif('پرداخت مورد نظر با موفقیت به ناموفق ها منتقل شد', 'mdi-checkbox-marked-circle-outline', 'green')
          })
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

    DeleteOrder (name, id) {
      const app = this
      this.$q.dialog({
        title: 'هشدار',
        message: 'آیا میخواهید سفارش مورد نظر حذف شود؟',
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
          app.$axios.delete(process.env.api + 'api/admin/orders/successful/' + id)
            .then(function () {
              app.showNotif('سفارش مورد نظر با موفقیت حذف شد', 'mdi-checkbox-marked-circle-outline', 'green')

              if (app.paginationPage === app.lastPage && app.data.length === 1) {
                app.paginationPage -= 1
              } else {
                app.GetAllSuccessfulOrders()
              }
            })
            .catch(function () {
              app.showNotif('مشکلی به وجود آمده است')
            })
        } else {
          app.$axios.delete(process.env.api + 'api/admin/orders/unsuccessful/' + id)
            .then(function () {
              app.showNotif('سفارش مورد نظر با موفقیت حذف شد', 'mdi-checkbox-marked-circle-outline', 'green')

              if (app.paginationPage === app.lastPage && app.data.length === 1) {
                app.paginationPage -= 1
              } else {
                app.GetAllUnSuccessfulOrders()
              }
            })
            .catch(function () {
              app.showNotif('مشکلی به وجود آمده است')
            })
        }
      })
    },

    GetAllSuccessfulOrders () {
      const app = this

      this.$q.loading.show()

      this.$axios.get(process.env.api + 'api/panel/orders/success/?page=' + app.paginationPage + '&search=' + app.search)
        .then(function (response) {
          app.data = response.data.results
          app.lastPage = response.data.last_page

          app.$q.loading.hide()
        })
    },

    GetAllUnSuccessfulOrders () {
      const app = this

      this.$q.loading.show()

      this.$axios.get(process.env.api + 'api/panel/orders/fail/?page=' + app.paginationPage + '&search=' + app.search)
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
      if (this.tab === 'successful_orders_list') {
        this.GetAllSuccessfulOrders()
      } else {
        this.GetAllUnSuccessfulOrders()
      }
    },
    paginationPage () {
      if (this.paginationPage === 0) {
        this.paginationPage = 1
      }
      if (this.tab === 'successful_orders_list') {
        this.GetAllSuccessfulOrders()
      } else {
        this.GetAllUnSuccessfulOrders()
      }
    },

    tab (value) {
      this.paginationPage = 1

      if (value === 'successful_orders_list') {
        this.request_type = 'successful'
        this.GetAllSuccessfulOrders()
      } else {
        this.request_type = 'unsuccessful'
        this.GetAllUnSuccessfulOrders()
      }
    }
  },

  mounted () {
    this.GetAllSuccessfulOrders()
  }
}
</script>

<style scoped>
body {
  background-color: #f5f5f5 !important;
}
</style>
