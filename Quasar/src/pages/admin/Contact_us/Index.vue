<template>
  <div class="q-pa-md">
    <div class="q-gutter-y-md">
      <q-card>
        <q-tabs
          align="left"
          v-model="tab"
          class="text-teal text-info"
        >
          <q-tab class="text-primary" name="contact_us_list" icon="mdi-format-list-text"
                 label="لیست تماس با ما"/>
        </q-tabs>
        <q-separator/>

        <q-tab-panels v-model="tab" animated>
          <q-tab-panel name="contact_us_list">
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
                     label="افزودن تماس باما"/>
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
                    <q-td key="name">{{ props.row.name }}</q-td>
                    <q-td key="email">{{ props.row.email }}</q-td>
                    <q-td key="website">{{ props.row.website }}</q-td>
                    <q-td key="text">{{ ShowText(props.row.text) }}</q-td>
                    <q-td key="created_at">{{ props.row.created_at | FormatDate }}</q-td>
                    <q-td key="setting">
                      <q-btn
                        @click="EditContact_us(props.row.id)"
                        style="color: #4facfe" rounded
                        icon="mdi-square-edit-outline" label="ویرایش" size="md" flat
                        dense>
                        <q-tooltip>ویرایش</q-tooltip>
                      </q-btn>
                      |
                      <q-btn @click="DeleteContact_us(props.row.name , props.row.id)" style="color: red" rounded
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

        <Modal :showDialog.sync="showDialog" :form="form" :type="type"></Modal>
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
          name: 'name',
          align: 'left',
          label: 'نام',
          field: 'name',
          sortable: true
        },
        {
          name: 'email',
          align: 'left',
          label: 'ایمیل',
          field: 'email',
          sortable: true
        },
        {
          name: 'website',
          align: 'left',
          label: 'وبسایت',
          field: 'website',
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

      tab: 'contact_us_list',
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

    ShowText (text) {
      return text.slice(0, 50) + ' ...'
    },

    DeleteContact_us (name, id) {
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
        app.$axios.delete(process.env.api + 'api/admin/contact_us/' + id)
          .then(function () {
            app.showNotif('تماس باما مورد نظر با موفقیت حذف شد', 'mdi-checkbox-marked-circle-outline', 'green')

            if (app.paginationPage === app.lastPage && app.data.length === 1) {
              app.paginationPage -= 1
            } else {
              app.GetAllContact_us()
            }
          })
          .catch(function () {
            app.showNotif('مشکلی به وجود آمده است')
          })
      })
    },

    EditContact_us (id) {
      const app = this

      this.$axios.get(process.env.api + 'api/admin/contact_us/' + id + '/')
        .then(function (response) {
          app.form = response.data

          app.setDialog('edit')

          app.$q.loading.hide()
        })
    },

    GetAllContact_us () {
      const app = this

      this.$q.loading.show()

      this.$axios.get(process.env.api + 'api/admin/contact_us/?page=' + app.paginationPage + '&search=' + app.search)
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
      this.GetAllContact_us()
    },
    paginationPage () {
      if (this.paginationPage === 0) {
        this.paginationPage = 1
      }
      this.GetAllContact_us()
    }
  },

  components: {
    Modal
  },

  mounted () {
    this.GetAllContact_us()
  }
}
</script>

<style scoped>
body {
  background-color: #f5f5f5 !important;
}
</style>
