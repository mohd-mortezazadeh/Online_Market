<template>
  <div class="q-pa-md">
    <div class="q-gutter-y-md">
      <q-card>
        <q-tabs
          align="left"
          v-model="tab"
          class="text-teal text-info"
        >
          <q-tab class="text-primary" name="articles_list" icon="mdi-format-list-text" label="مقالات"/>
        </q-tabs>
        <q-separator/>

        <q-tab-panels v-model="tab" animated>
          <q-tab-panel name="articles_list">
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
                     label="افزودن مقاله"/>
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
                    <q-td key="name">{{ props.row.title }}</q-td>
                    <q-td key="slug">{{ props.row.slug }}</q-td>
                    <q-td key="author">{{ props.row.author ? props.row.author['username'] : '' }}</q-td>
                    <q-td key="category">{{ props.row.category ? props.row.category['name'] : '' }}</q-td>
                    <q-td key="status">{{ ShowStatus(props.row.status) }}</q-td>
                    <q-td key="likeCount">{{ props.row.likeCount }}</q-td>
                    <q-td key="image">
                      <q-img
                        :src="ShowImage(props.row.image)"
                        spinner-color="white"
                        style="height: 90px; max-width: 120px"
                      />
                    </q-td>
                    <q-td key="setting">
                      <q-btn
                        @click="EditArticle(props.row.id , props.row.author , props.row.category , props.row.status)"
                        style="color: #4facfe" rounded
                        icon="mdi-square-edit-outline" label="ویرایش" size="md" flat
                        dense>
                        <q-tooltip>ویرایش</q-tooltip>
                      </q-btn>
                      |
                      <q-btn @click="DeleteArticle(props.row.title , props.row.id)" style="color: red" rounded
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

        <Modal :showDialog.sync="showDialog" :form="form" :type="type" :categories_list="categories_list"
               :authors_list="authors_list"></Modal>
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
      categories_list: [],
      authors_list: [],

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
          name: 'name',
          align: 'left',
          label: 'نام',
          field: 'name',
          sortable: true
        },
        {
          name: 'slug',
          align: 'left',
          label: 'نامک',
          field: 'slug',
          sortable: true
        },
        {
          name: 'author',
          align: 'left',
          label: 'نویسنده',
          field: 'author',
          sortable: true
        },
        {
          name: 'category',
          align: 'left',
          label: 'دسته بندی',
          field: 'category',
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
          name: 'likeCount',
          align: 'left',
          label: 'لایک ها',
          field: 'likeCount',
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
          name: 'setting',
          align: 'left',
          label: 'عملیات',
          field: 'setting',
          sortable: true
        }
      ],

      tab: 'articles_list',
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

    ShowStatus (status) {
      if (status === 0) {
        return 'پیش نویس'
      } else if (status === 1) {
        return 'منتشر شده'
      }

      return 'پایان انتشار'
    },

    GetAllCategories () {
      const app = this

      this.$axios.get(process.env.api + 'api/admin/categories/null/parent/')
        .then(function (response) {
          app.categories_list = response.data
        })
    },

    GetAllAuthors () {
      const app = this

      this.$axios.get(process.env.api + 'api/admin/articles/authors/list/')
        .then(function (response) {
          app.authors_list = response.data
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

    DeleteArticle (name, id) {
      const app = this
      this.$q.dialog({
        title: 'هشدار',
        message: 'آیا میخواهید مقاله ' + ' ( ' + name + ' ) ' + 'حذف شود ؟ ',
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
        app.$axios.delete(process.env.api + 'api/admin/articles/' + id)
          .then(function (response) {
            app.showNotif('مقاله مورد نظر با موفقیت حذف شد', 'mdi-checkbox-marked-circle-outline', 'green')
            app.GetAllArticles()
          })
          .catch(function () {
            app.showNotif('مشکلی به وجود آمده است')
          })
      })
    },

    EditArticle (id, author, category, status) {
      const app = this

      this.$q.loading.show()
      this.$axios.get(process.env.api + 'api/admin/articles/' + id + '/')
        .then(function (response) {
          app.form = response.data
          app.form.author = author
          app.form.category = category
          app.status = status

          app.setDialog('edit')

          app.$q.loading.hide()
        })
    },

    GetRelations () {
      const app = this

      for (const item in app.data) {
        if (app.data[item].author !== null) {
          this.$axios.get(process.env.api + 'api/admin/articles/author/' + app.data[item].author)
            .then(function (response) {
              app.data[item].author = response.data
            })
        }

        if (app.data[item].category !== null) {
          this.$axios.get(process.env.api + 'api/admin/categories/parent/' + app.data[item].category)
            .then(function (response) {
              app.data[item].category = response.data
            })
        }
      }

      this.$q.loading.hide()
    },

    GetAllArticles () {
      const app = this

      this.$q.loading.show()

      this.$axios.get(process.env.api + 'api/admin/articles/?page=' + app.paginationPage + '&search=' + app.search)
        .then(function (response) {
          app.data = response.data.results
          app.lastPage = response.data.last_page
          app.GetRelations()
        })
    },

    CheckPermission () {
      this.$q.loading.show()

      const data = {
        roles: ['author']
      }

      this.$axios.post(process.env.api + 'api/admin/acl/check/roles/', data)
        .then(function (response) {
        })
        .catch(function () {
          window.location.href = '/'
        })
    }
  },

  watch: {
    search () {
      this.GetAllArticles()
    },
    paginationPage () {
      this.GetAllArticles()
    }
  },

  components: {
    Modal
  },

  mounted () {
    this.CheckPermission()
    this.GetAllArticles()
    this.GetAllCategories()
    this.GetAllAuthors()
  }
}
</script>

<style scoped>
body {
  background-color: #f5f5f5 !important;
}
</style>
