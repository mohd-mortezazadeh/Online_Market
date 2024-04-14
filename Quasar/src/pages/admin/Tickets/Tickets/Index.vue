<template>
  <div class="q-pa-md">
    <div class="q-gutter-y-md">
      <q-card>
        <q-tabs
          align="left"
          v-model="tab"
          class="text-teal text-info"
        >
          <q-tab class="text-primary" name="open_tickets_list" icon="mdi-format-list-text" label="تیکت های فعال"/>
          <q-tab class="text-primary" name="close_tickets_list" icon="mdi-format-list-text" label="تیکت های بسته"/>
        </q-tabs>
        <q-separator/>

        <q-tab-panels v-model="tab" animated>
          <q-tab-panel name="open_tickets_list">
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
                     label="افزودن تیکت"/>
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
                    <q-td key="title">{{ props.row.title }}</q-td>
                    <q-td key="user">{{ props.row.user.username }}</q-td>
                    <q-td key="questions_count">{{ props.row.questions_count }}</q-td>
                    <q-td key="answers_count">{{ props.row.answers_count }}</q-td>
                    <q-td key="created_at">{{ props.row.created_at | FormatDate }}</q-td>
                    <q-td key="setting">
                      <q-btn @click="EditTicket(props.row.id , props.row.user)" style="color: #4facfe" rounded
                             icon="mdi-square-edit-outline" label="ویرایش" size="md" flat
                             dense>
                        <q-tooltip>ویرایش</q-tooltip>
                      </q-btn>
                      |
                      <q-btn @click="DeleteTicket(props.row.title , props.row.id)" style="color: red" rounded
                             icon="mdi-trash-can-outline" label="حذف" size="md" flat dense>
                        <q-tooltip>حذف</q-tooltip>
                      </q-btn>
                      |
                      <q-btn @click="SetStatusFalse(props.row.title , props.row.id)" style="color: red" rounded
                             icon="mdi-close-outline" label="بستن" size="md" flat dense>
                        <q-tooltip>بستن</q-tooltip>
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

          <q-tab-panel name="close_tickets_list">
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
                     label="افزودن تیکت"/>
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
                    <q-td key="title">{{ props.row.title }}</q-td>
                    <q-td key="user">{{ props.row.user.username }}</q-td>
                    <q-td key="questions_count">{{ props.row.questions_count }}</q-td>
                    <q-td key="answers_count">{{ props.row.answers_count }}</q-td>
                    <q-td key="created_at">{{ props.row.created_at | FormatDate }}</q-td>
                    <q-td key="setting">
                      <q-btn @click="EditTicket(props.row.id , props.row.user)" style="color: #4facfe" rounded
                             icon="mdi-square-edit-outline" label="ویرایش" size="md" flat
                             dense>
                        <q-tooltip>ویرایش</q-tooltip>
                      </q-btn>
                      |
                      <q-btn @click="DeleteTicket(props.row.title , props.row.id)" style="color: red" rounded
                             icon="mdi-trash-can-outline" label="حذف" size="md" flat dense>
                        <q-tooltip>حذف</q-tooltip>
                      </q-btn>
                      |
                      <q-btn @click="SetStatusTrue(props.row.title , props.row.id)" style="color: green" rounded
                             icon="mdi-shield-check-outline" label="باز کردن" size="md" flat dense>
                        <q-tooltip>باز کردن</q-tooltip>
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

        <Modal :showDialog.sync="showDialog" :form="form" :type="type" :user_list="user_list"
               :request_type="request_type"></Modal>
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
      request_type: 'open_tickets_list',

      form: {},

      search: '',

      data: [],
      user_list: [],

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
          name: 'title',
          align: 'left',
          label: 'نام',
          field: 'title',
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
          name: 'questions_count',
          align: 'left',
          label: 'تعداد سوال ها',
          field: 'questions_count',
          sortable: true
        },
        {
          name: 'answers_count',
          align: 'left',
          label: 'تعداد پاسخ ها',
          field: 'answers_count',
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

      tab: 'open_tickets_list',
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
    GetUsersList () {
      const app = this

      this.$axios.get(process.env.api + 'api/admin/users/all/WithOutPagination/')
        .then(function (response) {
          app.user_list = response.data
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

    SetStatusFalse (title, id) {
      const app = this

      this.$q.dialog({
        title: 'هشدار',
        message: 'آیا میخواهید وضعیت تیکت ' + ' ( ' + title + ' ) ' + 'بسته شود ؟ ',
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
        formData.append('type', 'close')

        app.$axios.post(process.env.api + 'api/admin/tickets/change/status/', formData)
          .then(function () {
            if (app.paginationPage === app.lastPage && app.data.length === 1) {
              app.paginationPage -= 1
            } else {
              app.GetAllOpenTickets()
            }
            app.showNotif('تیکت مورد نظر با موفقیت بسته شد', 'mdi-checkbox-marked-circle-outline', 'green')
          })
      })
    },

    SetStatusTrue (title, id) {
      const app = this

      this.$q.dialog({
        title: 'هشدار',
        message: 'آیا میخواهید وضعیت تیکت ' + ' ( ' + title + ' ) ' + 'باز شود ؟ ',
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
        formData.append('type', 'open')

        app.$axios.post(process.env.api + 'api/admin/tickets/change/status/', formData)
          .then(function () {
            if (app.paginationPage === app.lastPage && app.data.length === 1) {
              app.paginationPage -= 1
            } else {
              app.GetAllCloseTickets()
            }
            app.showNotif('تیکت مورد نظر با موفقیت باز شد', 'mdi-checkbox-marked-circle-outline', 'green')
          })
      })
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

    DeleteTicket (name, id) {
      const app = this
      this.$q.dialog({
        title: 'هشدار',
        message: 'آیا میخواهید تیکت ' + ' ( ' + name + ' ) ' + 'حذف شود ؟ ',
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
        if (app.request_type === 'open_tickets_list') {
          app.$axios.delete(process.env.api + 'api/admin/tickets/open/' + id)
            .then(function () {
              app.showNotif('تیکت مورد نظر با موفقیت حذف شد', 'mdi-checkbox-marked-circle-outline', 'green')
              app.GetAllOpenTickets()
              app.GetUsersList()
            })
            .catch(function () {
              app.showNotif('مشکلی به وجود آمده است')
            })
        } else {
          app.$axios.delete(process.env.api + 'api/admin/tickets/close/' + id)
            .then(function () {
              app.showNotif('تیکت مورد نظر با موفقیت حذف شد', 'mdi-checkbox-marked-circle-outline', 'green')
              app.GetAllCloseTickets()
              app.GetUsersList()
            })
            .catch(function () {
              app.showNotif('مشکلی به وجود آمده است')
            })
        }
      })
    },

    EditTicket (id, user) {
      const app = this

      this.$q.loading.show()
      if (app.request_type === 'open_tickets_list') {
        this.$axios.get(process.env.api + 'api/admin/tickets/open/' + id + '/')
          .then(function (response) {
            app.form = response.data
            app.form.user = user
            app.setDialog('edit')

            app.$q.loading.hide()
          })
      } else {
        this.$axios.get(process.env.api + 'api/admin/tickets/close/' + id + '/')
          .then(function (response) {
            app.form = response.data
            app.form.user = user
            app.setDialog('edit')

            app.$q.loading.hide()
          })
      }
    },

    GetRelations () {
      const app = this

      for (const item in app.data) {
        if (app.data[item].user !== null) {
          this.$axios.get(process.env.api + 'api/admin/users/' + app.data[item].user)
            .then(function (response) {
              app.data[item].user = response.data
            })
        }
      }

      this.$q.loading.hide()
    },

    GetAllCloseTickets () {
      const app = this

      this.$q.loading.show()

      this.$axios.get(process.env.api + 'api/admin/tickets/close/?page=' + app.paginationPage + '&search=' + app.search)
        .then(function (response) {
          app.data = response.data.results
          app.lastPage = response.data.last_page
          app.GetRelations()
        })
    },

    GetAllOpenTickets () {
      const app = this

      this.$q.loading.show()

      this.$axios.get(process.env.api + 'api/admin/tickets/open/?page=' + app.paginationPage + '&search=' + app.search)
        .then(function (response) {
          app.data = response.data.results
          app.lastPage = response.data.last_page
          app.GetRelations()
        })
    }
  },

  watch: {
    search () {
      if (this.paginationPage === 0) {
        this.paginationPage = 1
      }
      if (this.tab === 'open_tickets_list') {
        this.GetAllOpenTickets()
      } else {
        this.GetAllCloseTickets()
      }
    },
    paginationPage () {
      if (this.paginationPage === 0) {
        this.paginationPage = 1
      }
      if (this.tab === 'open_tickets_list') {
        this.GetAllOpenTickets()
      } else {
        this.GetAllCloseTickets()
      }
    },

    tab (value) {
      this.paginationPage = 1

      if (value === 'open_tickets_list') {
        this.request_type = 'open_tickets_list'
        this.GetAllOpenTickets()
      } else {
        this.request_type = 'close_tickets_list'
        this.GetAllCloseTickets()
      }
    }
  },

  components: {
    Modal
  },

  mounted () {
    this.GetAllOpenTickets()
    this.GetUsersList()
  }
}
</script>

<style scoped>
body {
  background-color: #f5f5f5 !important;
}
</style>
