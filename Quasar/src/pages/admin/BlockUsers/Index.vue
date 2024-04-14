<template>
  <div class="q-pa-md">
    <div class="q-gutter-y-md">
      <q-card>
        <q-tabs
          align="left"
          v-model="tab"
          class="text-teal text-info"
        >
          <q-tab class="text-primary" name="users_list" icon="mdi-format-list-text" label="کاربران بلاک شده"/>
        </q-tabs>
        <q-separator/>

        <q-tab-panels v-model="tab" animated>
          <q-tab-panel name="users_list">
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
                    <q-td key="name">{{ props.row.username }}</q-td>
                    <q-td key="first_name">{{ props.row.first_name }}</q-td>
                    <q-td key="last_name">{{ props.row.last_name }}</q-td>
                    <q-td key="email">{{ props.row.email }}</q-td>
                    <q-td key="phoneNumber">{{ props.row.phoneNumber }}</q-td>
                    <q-td key="is_superuser">
                      <q-badge outline :color="props.row.is_superuser ? 'secondary' : 'red'"
                               :label="ShowIsSuperuser(props.row.is_superuser)"/>
                    </q-td>
                    <q-td key="is_active">
                      <q-badge outline :color="props.row.is_active ? 'secondary' : 'red'"
                               :label="ShowIsActive(props.row.is_active)"/>
                    </q-td>
                    <q-td key="image">
                      <q-img
                        :src="ShowImage(props.row.image)"
                        spinner-color="white"
                        style="height: 90px; max-width: 120px"
                      />
                    </q-td>
                    <q-td key="date_joined">{{ props.row.date_joined | FormatDate }}</q-td>
                    <q-td key="setting">
                      <q-btn @click="EditUser(props.row.id , props.row.author , props.row.category , props.row.status)"
                             style="color: #4facfe" rounded
                             icon="mdi-square-edit-outline" label="ویرایش" size="md" flat
                             dense>
                        <q-tooltip>ویرایش</q-tooltip>
                      </q-btn>
                      |
                      <q-btn @click="DeleteUser(props.row.username , props.row.id)" style="color: red" rounded
                             icon="mdi-trash-can-outline" label="حذف" size="md" flat dense>
                        <q-tooltip>حذف</q-tooltip>
                      </q-btn>
                      |
                      <q-btn @click="UnBlockUser(props.row.username , props.row.id)" style="color: red" rounded
                             icon="mdi-trash-can-outline" label="رفع مسدودیت" size="md" flat dense>
                        <q-tooltip>رفع مسدودیت</q-tooltip>
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
          name: 'username',
          align: 'left',
          label: 'نام کاربری',
          field: 'username',
          sortable: true
        },
        {
          name: 'first_name',
          align: 'left',
          label: 'نام',
          field: 'first_name',
          sortable: true
        },
        {
          name: 'last_name',
          align: 'left',
          label: 'نام خانوادگی',
          field: 'last_name',
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
          name: 'phoneNumber',
          align: 'left',
          label: 'موبایل',
          field: 'phoneNumber',
          sortable: true
        },
        {
          name: 'is_superuser',
          align: 'left',
          label: 'آیا مدیر است',
          field: 'is_superuser',
          sortable: true
        },
        {
          name: 'is_active',
          align: 'left',
          label: 'آیا فعال است',
          field: 'is_active',
          sortable: true
        },
        {
          name: 'image',
          align: 'left',
          label: 'عکس',
          field: 'image',
          sortable: true
        },
        {
          name: 'date_joined',
          align: 'left',
          label: 'تاریخ عضویت',
          field: 'date_joined',
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

      tab: 'users_list',
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
      if (url) {
        return url.replace('http://localhost:8000/', process.env.api)
      }
      return 'https://i.pinimg.com/originals/51/f6/fb/51f6fb256629fc755b8870c801092942.png'
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

    DeleteUser (name, id) {
      const app = this
      this.$q.dialog({
        title: 'هشدار',
        message: 'آیا میخواهید کاربر ' + ' ( ' + name + ' ) ' + 'حذف شود ؟ ',
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
        app.$axios.delete(process.env.api + 'api/admin/users/blocks/list/' + id)
          .then(function (response) {
            app.showNotif('کاربر مورد نظر با موفقیت حذف شد', 'mdi-checkbox-marked-circle-outline', 'green')
            app.GetAllUsers()
          })
          .catch(function () {
            app.showNotif('مشکلی به وجود آمده است')
          })
      })
    },

    EditUser (id) {
      const app = this

      this.$q.loading.show()
      this.$axios.get(process.env.api + 'api/admin/users/blocks/list/' + id + '/')
        .then(function (response) {
          app.form = response.data

          app.setDialog('edit')
          app.$q.loading.hide()
        })
    },

    UnBlockUser (name, id) {
      const app = this
      this.$q.dialog({
        title: 'هشدار',
        message: 'آیا میخواهید کاربر ' + ' ( ' + name + ' ) ' + 'از مسدود شده ها خارج شود ؟ ',
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
        formData.append('type', 'unblock')

        app.$axios.post(process.env.api + 'api/admin/users/change/block_status/', formData)
          .then(function () {
            app.showNotif('کاربر مورد نظر با موفقیت از مسدود شده ها خارج شد', 'mdi-checkbox-marked-circle-outline', 'green')
            app.GetAllUsers()
          })
          .catch(function () {
            app.showNotif('مشکلی به وجود آمده است')
          })
      })
    },

    ShowIsSuperuser (isSuperuser) {
      if (isSuperuser) {
        return 'فعال'
      }
      return 'غیر فعال'
    },

    ShowIsActive (isActive) {
      if (isActive) {
        return 'فعال'
      }
      return 'غیر فعال'
    },

    GetAllUsers () {
      const app = this

      this.$q.loading.show()

      this.$axios.get(process.env.api + 'api/admin/users/blocks/list/?page=' + app.paginationPage + '&search=' + app.search)
        .then(function (response) {
          app.data = response.data.results
          app.lastPage = response.data.last_page
          app.$q.loading.hide()
        })
    }
  },

  components: {
    Modal
  },

  watch: {
    search () {
      this.GetAllUsers()
    },
    paginationPage () {
      this.GetAllUsers()
    }
  },

  mounted () {
    this.GetAllUsers()
  }
}
</script>

<style scoped>
body {
  background-color: #f5f5f5 !important;
}
</style>
