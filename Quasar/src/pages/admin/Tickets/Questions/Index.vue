<template>
  <div class="q-pa-md">
    <div class="q-gutter-y-md">
      <q-card>
        <q-tabs
          align="left"
          v-model="tab"
          class="text-teal text-info"
        >
          <q-tab class="text-primary" name="questions_list" icon="mdi-format-list-text" label="سوال های تیکت ها"/>
        </q-tabs>
        <q-separator/>

        <q-tab-panels v-model="tab" animated>
          <q-tab-panel name="questions_list">
             <q-input style="width: 300px; float: left !important;"
                     dense v-model.lazy="search"
                     debounce="250"
                     filled type="search">
              <template v-slot:append>
                <q-icon name="search"/>
              </template>
            </q-input>

            <div class="q-pl-md q-gutter-sm">
              <q-btn color="primary" outline @click="setDialog('create')" icon="mdi-file-plus-outline" label="افزودن سوال"/>
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
                    <q-td key="text">{{ ShowTruncatedText(props.row.text) }}</q-td>
                    <q-td key="ticket">{{ props.row.ticket.title }}</q-td>
                    <q-td key="created_at">{{ props.row.created_at | FormatDate }}</q-td>
                    <q-td key="setting">
                      <q-btn @click="EditQuestions(props.row.id , props.row.ticket)" style="color: #4facfe" rounded icon="mdi-square-edit-outline" label="ویرایش" size="md" flat
                             dense>
                        <q-tooltip>ویرایش</q-tooltip>
                      </q-btn>
                      |
                      <q-btn @click="DeleteQuestions(ShowTruncatedText(props.row.text) , props.row.id)" style="color: red" rounded
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

        <Modal :showDialog.sync="showDialog" :form="form" :type="type" :tickets_list="tickets_list"></Modal>
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
      tickets_list: [],

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
          name: 'text',
          align: 'left',
          label: 'سوال',
          field: 'text',
          sortable: true
        },
        {
          name: 'ticket',
          align: 'left',
          label: 'تیکت',
          field: 'ticket',
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

      tab: 'questions_list',
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
    ShowTruncatedText (text) {
      if (text && text.length > 25) {
        return text.substring(0, 25) + ' ...'
      }
      return text
    },
    GetTicketsList () {
      const app = this

      this.$axios.get(process.env.api + 'api/admin/tickets/all/open/')
        .then(function (response) {
          app.tickets_list = response.data
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

    DeleteQuestions (name, id) {
      const app = this
      this.$q.dialog({
        title: 'هشدار',
        message: 'آیا میخواهید سوال ' + ' ( ' + name + ' ) ' + 'حذف شود ؟ ',
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
        app.$axios.delete(process.env.api + 'api/admin/tickets/questions/' + id)
          .then(function (response) {
            app.showNotif('سوال تیکت مورد نظر با موفقیت حذف شد', 'mdi-checkbox-marked-circle-outline', 'green')
            app.GetAllQuestions()
            app.GetTicketsList()
          })
          .catch(function () {
            app.showNotif('مشکلی به وجود آمده است')
          })
      })
    },

    EditQuestions (id, ticket) {
      const app = this

      this.$q.loading.show()
      this.$axios.get(process.env.api + 'api/admin/tickets/questions/' + id + '/')
        .then(function (response) {
          app.form = response.data
          app.form.ticket = ticket
          app.setDialog('edit')

          app.$q.loading.hide()
        })
    },

    GetRelations () {
      const app = this

      for (const item in app.data) {
        if (app.data[item].ticket !== null) {
          this.$axios.get(process.env.api + 'api/admin/tickets/open/' + app.data[item].ticket)
            .then(function (response) {
              app.data[item].ticket = response.data
            })
        }
      }

      this.$q.loading.hide()
    },

    GetAllQuestions () {
      const app = this

      this.$q.loading.show()

      this.$axios.get(process.env.api + 'api/admin/tickets/questions/?page=' + app.paginationPage + '&search=' + app.search)
        .then(function (response) {
          app.data = response.data.results
          app.lastPage = response.data.last_page
          app.GetRelations()
        })
    }
  },

  watch: {
    search () {
      this.GetAllQuestions()
    },
    paginationPage () {
      this.GetAllQuestions()
    }
  },

  components: {
    Modal
  },

  mounted () {
    this.GetAllQuestions()
    this.GetTicketsList()
  }
}
</script>

<style scoped>
body {
  background-color: #f5f5f5 !important;
}
</style>
