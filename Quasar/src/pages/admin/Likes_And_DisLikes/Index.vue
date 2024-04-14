<template>
  <div class="q-pa-md">
    <div class="q-gutter-y-md">
      <q-card>
        <q-tabs
          align="left"
          v-model="tab"
          class="text-teal text-info"
        >
          <q-tab class="text-primary" name="likes_list" icon="mdi-format-list-text"
                 label="لایک ها"/>
          <q-tab class="text-primary" name="dislikes_list" icon="mdi-format-list-text"
                 label="دیسلایک ها"/>
        </q-tabs>
        <q-separator/>

        <q-tab-panels v-model="tab" animated>
          <q-tab-panel name="likes_list">
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
                    <q-td key="title">{{ props.row.user.username }}</q-td>
                  <q-td key="content_type">{{ ShowContentType(props.row.content_type) }}</q-td>
                    <q-td key="created_at">{{ props.row.created_at | FormatDate }}</q-td>
                    <q-td key="setting">
                      <q-btn
                        @click="Edit_Like_And_DisLike(props.row.id , props.row.user)"
                        style="color: #4facfe" rounded
                        icon="mdi-square-edit-outline" label="ویرایش" size="md" flat
                        dense>
                        <q-tooltip>ویرایش</q-tooltip>
                      </q-btn>
                      |
                      <q-btn @click="Delete_Like_And_DisLike(props.row.id)" style="color: red" rounded
                             icon="mdi-trash-can-outline" label="حذف" size="md" flat dense>
                        <q-tooltip>حذف</q-tooltip>
                      </q-btn>
                      |
                      <q-btn
                        @click="SetTypeDisLike(props.row.id)"
                        style="color: red" rounded
                        icon="mdi-close-outline" label="تبدیل به دیسلایک" size="md" flat dense>
                        <q-tooltip>تبدیل به دیسلایک</q-tooltip>
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

          <q-tab-panel name="dislikes_list">
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
                    <q-td key="content_type">{{ ShowContentType(props.row.content_type) }}</q-td>
                    <q-td key="created_at">{{ props.row.created_at | FormatDate }}</q-td>
                    <q-td key="setting">
                      <q-btn
                        @click="Edit_Like_And_DisLike(props.row.id , props.row.user)"
                        style="color: #4facfe" rounded
                        icon="mdi-square-edit-outline" label="ویرایش" size="md" flat
                        dense>
                        <q-tooltip>ویرایش</q-tooltip>
                      </q-btn>
                      |
                      <q-btn @click="Delete_Like_And_DisLike(props.row.id)" style="color: red" rounded
                             icon="mdi-trash-can-outline" label="حذف" size="md" flat dense>
                        <q-tooltip>حذف</q-tooltip>
                      </q-btn>
                      |
                      <q-btn
                        @click="SetTypeLike(props.row.id)"
                        style="color: green" rounded
                        icon="mdi-shield-check-outline" label="تبدیل به لایک" size="md" flat dense>
                        <q-tooltip>تبدیل به لایک</q-tooltip>
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

        <Modal :showDialog.sync="showDialog" :form="form" :users_list="users_list" :request_type="request_type"></Modal>
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
      request_type: 'likes',

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
          name: 'content_type',
          align: 'left',
          label: 'نوع مدل',
          field: 'content_type',
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

      tab: 'likes_list',
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
    ShowContentType (contentType) {
      return contentType.app_label + ' | ' + contentType.model
    },

    GetRequiredLists () {
      const app = this

      this.$axios.get(process.env.api + 'api/admin/products/users/list/')
        .then(function (response) {
          app.users_list = response.data
        })
    },

    SetTypeLike (id) {
      const app = this

      this.$q.dialog({
        title: 'هشدار',
        message: 'آیا میخواهید وضعیت مورد انتخابی نقض شود؟',
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
        formData.append('type', 'like')

        app.$axios.post(process.env.api + 'api/admin/likes_dislikes/change/type/', formData)
          .then(function () {
            if (app.paginationPage === app.lastPage && app.data.length === 1) {
              app.paginationPage -= 1
            } else {
              app.GetAllDisLikes()
              app.GetRequiredLists()
            }
            app.showNotif('وضعیت مورد انتخابی با موفقیت نقض شد', 'mdi-checkbox-marked-circle-outline', 'green')
          })
      })
    },

    SetTypeDisLike (id) {
      const app = this

      this.$q.dialog({
        title: 'هشدار',
        message: 'آیا میخواهید وضعیت مورد انتخابی نقض شود؟',
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
        formData.append('type', 'dislike')

        app.$axios.post(process.env.api + 'api/admin/likes_dislikes/change/type/', formData)
          .then(function () {
            if (app.paginationPage === app.lastPage && app.data.length === 1) {
              app.paginationPage -= 1
            } else {
              app.GetAllLikes()
              app.GetRequiredLists()
            }
            app.showNotif('وضعیت مورد انتخابی با موفقیت نقض شد', 'mdi-checkbox-marked-circle-outline', 'green')
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

    Delete_Like_And_DisLike (id) {
      const app = this
      this.$q.dialog({
        title: 'هشدار',
        message: 'آیا میخواهید مورد انتخابی حذف شود؟',
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
        if (app.request_type === 'likes') {
          app.$axios.delete(process.env.api + 'api/admin/likes_dislikes/likes/' + id)
            .then(function () {
              app.showNotif('مورد انتخابی با موفقیت حذف شد', 'mdi-checkbox-marked-circle-outline', 'green')

              if (app.paginationPage === app.lastPage && app.data.length === 1) {
                app.paginationPage -= 1
              } else {
                app.GetAllLikes()
                app.GetRequiredLists()
              }
            })
            .catch(function () {
              app.showNotif('مشکلی به وجود آمده است')
            })
        } else {
          app.$axios.delete(process.env.api + 'api/admin/likes_dislikes/dislikes/' + id)
            .then(function () {
              app.showNotif('مورد انتخابی با موفقیت حذف شد', 'mdi-checkbox-marked-circle-outline', 'green')

              if (app.paginationPage === app.lastPage && app.data.length === 1) {
                app.paginationPage -= 1
              } else {
                app.GetAllDisLikes()
                app.GetRequiredLists()
              }
            })
            .catch(function () {
              app.showNotif('مشکلی به وجود آمده است')
            })
        }
      })
    },

    Edit_Like_And_DisLike (id, user) {
      const app = this

      this.$q.loading.show()
      if (this.request_type === 'likes') {
        this.$axios.get(process.env.api + 'api/admin/likes_dislikes/likes/' + id + '/')
          .then(function (response) {
            app.form = response.data
            app.form.user = user

            app.setDialog('edit')

            app.$q.loading.hide()
          })
      } else {
        this.$axios.get(process.env.api + 'api/admin/likes_dislikes/dislikes/' + id + '/')
          .then(function (response) {
            app.form = response.data

            app.setDialog('edit')

            app.$q.loading.hide()
          })
      }
    },

    GetAllLikes () {
      const app = this

      this.$q.loading.show()

      this.$axios.get(process.env.api + 'api/admin/likes_dislikes/likes/?page=' + app.paginationPage + '&search=' + app.search)
        .then(function (response) {
          app.data = response.data.results
          app.lastPage = response.data.last_page

          app.$q.loading.hide()
        })
    },

    GetAllDisLikes () {
      const app = this

      this.$q.loading.show()

      this.$axios.get(process.env.api + 'api/admin/likes_dislikes/dislikes/?page=' + app.paginationPage + '&search=' + app.search)
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
      if (this.tab === 'likes_list') {
        this.GetAllLikes()
      } else {
        this.GetAllDisLikes()
      }
    },
    paginationPage () {
      if (this.paginationPage === 0) {
        this.paginationPage = 1
      }
      if (this.tab === 'likes_list') {
        this.GetAllLikes()
      } else {
        this.GetAllDisLikes()
      }
    },

    tab (value) {
      this.paginationPage = 1

      if (value === 'likes_list') {
        this.request_type = 'likes'
        this.GetAllLikes()
      } else {
        this.request_type = 'dislikes'
        this.GetAllDisLikes()
      }
    }
  },

  components: {
    Modal
  },

  mounted () {
    this.GetAllLikes()
    this.GetRequiredLists()
  }
}
</script>

<style scoped>
body {
  background-color: #f5f5f5 !important;
}
</style>
