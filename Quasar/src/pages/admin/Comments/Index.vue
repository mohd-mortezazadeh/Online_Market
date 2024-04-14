<template>
  <div class="q-pa-md">
    <div class="q-gutter-y-md">
      <q-card>
        <q-tabs
          align="left"
          v-model="tab"
          class="text-teal text-info"
        >
          <q-tab class="text-primary" name="accepted_comments" icon="mdi-format-list-text"
                 label="نظرات تایید شده"/>
          <q-tab class="text-primary" name="NotAccepted_comments" icon="mdi-format-list-text"
                 label="نظرات تایید نشده"/>
        </q-tabs>
        <q-separator/>

        <q-tab-panels v-model="tab" animated>
          <q-tab-panel name="accepted_comments">
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
                    <q-td key="title">{{ props.row.title }}</q-td>
                    <q-td key="text">{{ props.row.text }}</q-td>
                    <q-td key="user">{{ props.row.user.username }}</q-td>
                    <q-td key="parent">{{ props.row.parent ? props.row.parent.title : '' }}</q-td>
                    <q-td key="created_at">{{ props.row.created_at | FormatDate }}</q-td>
                    <q-td key="setting">
                      <q-btn
                        @click="EditComment(props.row.id , props.row.user , props.row.category , props.row.status)"
                        style="color: #4facfe" rounded
                        icon="mdi-square-edit-outline" label="ویرایش" size="md" flat
                        dense>
                        <q-tooltip>ویرایش</q-tooltip>
                      </q-btn>
                      |
                      <q-btn @click="DeleteComment(props.row.title , props.row.id)" style="color: red" rounded
                             icon="mdi-trash-can-outline" label="حذف" size="md" flat dense>
                        <q-tooltip>حذف</q-tooltip>
                      </q-btn>
                      |
                      <q-btn
                        @click="SetStatusNotAccepted(props.row.title , props.row.id)"
                        style="color: red" rounded
                        icon="mdi-close-outline" label="تایید نکردن" size="md" flat dense>
                        <q-tooltip>تایید نکردن</q-tooltip>
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

          <q-tab-panel name="NotAccepted_comments">
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
                    <q-td key="title">{{ props.row.title }}</q-td>
                    <q-td key="text">{{ props.row.text }}</q-td>
                    <q-td key="user">{{ props.row.user.username }}</q-td>
                    <q-td key="parent">{{ props.row.parent ? props.row.parent.title : '' }}</q-td>
                    <q-td key="created_at">{{ props.row.created_at | FormatDate }}</q-td>
                    <q-td key="setting">
                      <q-btn
                        @click="EditComment(props.row.id , props.row.user , props.row.category , props.row.status)"
                        style="color: #4facfe" rounded
                        icon="mdi-square-edit-outline" label="ویرایش" size="md" flat
                        dense>
                        <q-tooltip>ویرایش</q-tooltip>
                      </q-btn>
                      |
                      <q-btn @click="DeleteComment(props.row.title , props.row.id)" style="color: red" rounded
                             icon="mdi-trash-can-outline" label="حذف" size="md" flat dense>
                        <q-tooltip>حذف</q-tooltip>
                      </q-btn>
                      |
                      <q-btn
                        @click="SetStatusAccepted(props.row.title , props.row.id)"
                        style="color: green" rounded
                        icon="mdi-shield-check-outline" label="تایید کردن" size="md" flat dense>
                        <q-tooltip>تایید کردن</q-tooltip>
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

        <Modal :showDialog.sync="showDialog" :form="form" :request_type="request_type"></Modal>
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
      request_type: 'accepted',

      form: {},

      search: '',

      data: [],
      products_list: [],
      users_list: [],
      colors_list: [],
      sizes_list: [],

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
          name: 'title',
          align: 'left',
          label: 'عنوان',
          field: 'title',
          sortable: true
        },
        {
          name: 'text',
          align: 'left',
          label: 'متن',
          field: 'text',
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
          name: 'parent',
          align: 'left',
          label: 'پاسخ داده شده به',
          field: 'parent',
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

      tab: 'accepted_comments',
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
    SetStatusAccepted (title, id) {
      const app = this

      this.$q.dialog({
        title: 'هشدار',
        message: 'آیا میخواهید وضعیت تایید نظر ' + ' ( ' + title + ' ) ' + 'نقض شود ؟ ',
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
        formData.append('type', 'accept')

        app.$axios.post(process.env.api + 'api/admin/comments/change/status/', formData)
          .then(function () {
            if (app.paginationPage === app.lastPage && app.data.length === 1) {
              app.paginationPage -= 1
            } else {
              app.GetAllNotAcceptedPayments()
            }
            app.showNotif('نظر مورد نظر با موفقیت به تایید شده ها منتقل شد', 'mdi-checkbox-marked-circle-outline', 'green')
          })
      })
    },

    SetStatusNotAccepted (title, id) {
      const app = this

      this.$q.dialog({
        title: 'هشدار',
        message: 'آیا میخواهید وضعیت تایید نظر ' + ' ( ' + title + ' ) ' + 'نقض شود ؟ ',
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
        formData.append('type', 'NotAccept')

        app.$axios.post(process.env.api + 'api/admin/comments/change/status/', formData)
          .then(function () {
            if (app.paginationPage === app.lastPage && app.data.length === 1) {
              app.paginationPage -= 1
            } else {
              app.GetAllAcceptedPayments()
            }
            app.showNotif('نظر مورد نظر با موفقیت به تایید نشده ها منتقل شد', 'mdi-checkbox-marked-circle-outline', 'green')
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

    DeleteComment (name, id) {
      const app = this
      this.$q.dialog({
        title: 'هشدار',
        message: 'آیا میخواهید نظر' + ' ( ' + name + ' ) ' + 'حذف شود ؟ ',
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
        if (app.request_type === 'accepted') {
          app.$axios.delete(process.env.api + 'api/admin/comments/accepted/' + id)
            .then(function () {
              app.showNotif('پرداخت مورد نظر با موفقیت حذف شد', 'mdi-checkbox-marked-circle-outline', 'green')

              if (app.paginationPage === app.lastPage && app.data.length === 1) {
                app.paginationPage -= 1
              } else {
                app.GetAllAcceptedPayments()
              }
            })
            .catch(function () {
              app.showNotif('مشکلی به وجود آمده است')
            })
        } else {
          app.$axios.delete(process.env.api + 'api/admin/comments/NotAccepted/' + id)
            .then(function () {
              app.showNotif('پرداخت مورد نظر با موفقیت حذف شد', 'mdi-checkbox-marked-circle-outline', 'green')

              if (app.paginationPage === app.lastPage && app.data.length === 1) {
                app.paginationPage -= 1
              } else {
                app.GetAllNotAcceptedPayments()
              }
            })
            .catch(function () {
              app.showNotif('مشکلی به وجود آمده است')
            })
        }
      })
    },

    EditComment (id) {
      const app = this

      this.$q.loading.show()
      if (this.request_type === 'accepted') {
        this.$axios.get(process.env.api + 'api/admin/comments/accepted/' + id + '/')
          .then(function (response) {
            app.form = response.data

            app.setDialog('edit')

            app.$q.loading.hide()
          })
      } else {
        this.$axios.get(process.env.api + 'api/admin/comments/NotAccepted/' + id + '/')
          .then(function (response) {
            app.form = response.data

            app.setDialog('edit')

            app.$q.loading.hide()
          })
      }
    },

    GetAllAcceptedPayments () {
      const app = this

      this.$q.loading.show()

      this.$axios.get(process.env.api + 'api/admin/comments/accepted/?page=' + app.paginationPage + '&search=' + app.search)
        .then(function (response) {
          app.data = response.data.results
          app.lastPage = response.data.last_page

          app.$q.loading.hide()
        })
    },

    GetAllNotAcceptedPayments () {
      const app = this

      this.$q.loading.show()

      this.$axios.get(process.env.api + 'api/admin/comments/NotAccepted/?page=' + app.paginationPage + '&search=' + app.search)
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
      if (this.tab === 'accepted_comments') {
        this.GetAllAcceptedPayments()
      } else {
        this.GetAllNotAcceptedPayments()
      }
    },
    paginationPage () {
      if (this.paginationPage === 0) {
        this.paginationPage = 1
      }
      if (this.tab === 'accepted_comments') {
        this.GetAllAcceptedPayments()
      } else {
        this.GetAllNotAcceptedPayments()
      }
    },

    tab (value) {
      this.paginationPage = 1

      if (value === 'accepted_comments') {
        this.request_type = 'accepted'
        this.GetAllAcceptedPayments()
      } else {
        this.request_type = 'NotAccepted'
        this.GetAllNotAcceptedPayments()
      }
    }
  },

  components: {
    Modal
  },

  mounted () {
    this.GetAllAcceptedPayments()
  }
}
</script>

<style scoped>
body {
  background-color: #f5f5f5 !important;
}
</style>
