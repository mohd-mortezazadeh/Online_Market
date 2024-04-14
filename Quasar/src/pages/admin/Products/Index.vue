<template>
  <div class="q-pa-md">
    <div class="q-gutter-y-md">
      <q-card>
        <q-tabs
          align="left"
          v-model="tab"
          class="text-teal text-info"
        >
          <q-tab class="text-primary" name="products_list" icon="mdi-format-list-text" label="محصولات تایید شده"/>
          <q-tab class="text-primary" name="products_not_accepted_list" icon="mdi-format-list-text"
                 label="محصولات تایید نشده"/>
        </q-tabs>
        <q-separator/>

        <q-tab-panels v-model="tab" animated>
          <q-tab-panel name="products_list">
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
                     label="افزودن محصول"/>
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
                    <q-td key="price">{{ props.row.price }}</q-td>
                    <q-td key="count">{{ props.row.count }}</q-td>
                    <q-td key="type">
                      <q-badge outline :color="ShowTypeColor(props.row.type)"
                               :label="ShowType(props.row.type)"/>
                    </q-td>
                    <q-td key="user">{{ props.row.user.username }}</q-td>
                    <q-td key="category">{{ props.row.category.name }}</q-td>
                    <q-td key="viewCount">{{ props.row.viewCount }}</q-td>
                    <q-td key="likeCount">{{ props.row.likeCount }}</q-td>
                    <q-td key="original_image">
                      <q-img
                        :src="ShowImage(props.row.original_image)"
                        spinner-color="white"
                        style="height: 80px; max-width: 60px"
                      />
                    </q-td>
                    <q-td key="colors_list">{{ ShowColors(props.row.colors) }}</q-td>
                    <q-td key="sizes_list">{{ ShowSizes(props.row.sizes) }}</q-td>
                    <q-td key="created_at">{{ props.row.created_at | FormatDate }}</q-td>
                    <q-td key="setting">
                      <q-btn
                        @click="EditProduct(props.row.id , props.row.user , props.row.category , props.row.status)"
                        style="color: #4facfe" rounded
                        icon="mdi-square-edit-outline" label="ویرایش" size="md" flat
                        dense>
                        <q-tooltip>ویرایش</q-tooltip>
                      </q-btn>
                      |
                      <q-btn @click="DeleteProduct(props.row.title , props.row.id)" style="color: red" rounded
                             icon="mdi-trash-can-outline" label="حذف" size="md" flat dense>
                        <q-tooltip>حذف</q-tooltip>
                      </q-btn>
                      |
                      <q-btn @click="SetStatusFalse(props.row.title , props.row.id)" style="color: red" rounded
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

          <q-tab-panel name="products_not_accepted_list">
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
                    <q-td key="name">{{ props.row.title }}</q-td>
                    <q-td key="price">{{ props.row.price }}</q-td>
                    <q-td key="count">{{ props.row.count }}</q-td>
                    <q-td key="type">
                      <q-badge outline :color="ShowTypeColor(props.row.type)"
                               :label="ShowType(props.row.type)"/>
                    </q-td>
                    <q-td key="user">{{ props.row.user.username }}</q-td>
                    <q-td key="category">{{ props.row.category.name }}</q-td>
                    <q-td key="viewCount">{{ props.row.viewCount }}</q-td>
                    <q-td key="likeCount">{{ props.row.likeCount }}</q-td>
                    <q-td key="original_image">
                      <q-img
                        :src="ShowImage(props.row.original_image)"
                        spinner-color="white"
                        style="height: 80px; max-width: 60px"
                      />
                    </q-td>
                    <q-td key="colors_list">{{ ShowColors(props.row.colors) }}</q-td>
                    <q-td key="sizes_list">{{ ShowSizes(props.row.sizes) }}</q-td>
                    <q-td key="created_at">{{ props.row.created_at | FormatDate }}</q-td>
                    <q-td key="setting">
                      <q-btn
                        @click="EditProduct(props.row.id , props.row.user , props.row.category , props.row.status)"
                        style="color: #4facfe" rounded
                        icon="mdi-square-edit-outline" label="ویرایش" size="md" flat
                        dense>
                        <q-tooltip>ویرایش</q-tooltip>
                      </q-btn>
                      |
                      <q-btn @click="DeleteProduct(props.row.title , props.row.id)" style="color: red" rounded
                             icon="mdi-trash-can-outline" label="حذف" size="md" flat dense>
                        <q-tooltip>حذف</q-tooltip>
                      </q-btn>
                      |
                      <q-btn @click="SetStatusTrue(props.row.title , props.row.id)" style="color: green" rounded
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

        <Modal :showDialog.sync="showDialog" :form="form" :type="type" :categories_list="categories_list"
               :colors_list="colors_list"
               :sizes_lis="sizes_list"
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
      request_type: 'accepted',

      form: {},

      search: '',

      data: [],
      categories_list: [],
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
          name: 'price',
          align: 'left',
          label: 'قمیت',
          field: 'price',
          sortable: true
        },
        {
          name: 'count',
          align: 'left',
          label: 'موجودیت',
          field: 'count',
          sortable: true
        },
        {
          name: 'type',
          align: 'left',
          label: 'نوع',
          field: 'type',
          sortable: true
        },
        {
          name: 'user',
          align: 'left',
          label: 'فروشنده',
          field: 'user',
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
          name: 'viewCount',
          align: 'left',
          label: 'بازدید ها',
          field: 'viewCount',
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
          name: 'original_image',
          align: 'left',
          label: 'عکس اصلی',
          field: 'original_image',
          sortable: true
        },
        {
          name: 'colors_list',
          align: 'left',
          label: 'رنگ ها',
          field: 'colors',
          sortable: true
        },
        {
          name: 'sizes_list',
          align: 'left',
          label: 'سایز ها',
          field: 'sizes',
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

      tab: 'products_list',
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

    ShowType (type) {
      if (type === 'free') {
        return 'رایگان'
      } else if (type === 'special') {
        return 'اعضای ویژه'
      }

      return 'نقدی'
    },

    ShowTypeColor (type) {
      if (type === 'free') {
        return 'secondary'
      } else if (type === 'special') {
        return 'orange'
      }

      return 'red'
    },

    ShowColors (colors) {
      const NewColors = []
      for (const item in colors) {
        NewColors[item] = colors[item].name
      }
      return NewColors.join(' , ')
    },

    ShowSizes (sizes) {
      const NewSizes = []
      for (const item in sizes) {
        NewSizes[item] = sizes[item].title
      }
      return NewSizes.join(' , ')
    },

    SetStatusFalse (title, id) {
      const app = this

      this.$q.dialog({
        title: 'هشدار',
        message: 'آیا میخواهید وضعیت تایید محصول ' + ' ( ' + title + ' ) ' + 'نقض شود ؟ ',
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
        formData.append('type', 'reject')

        app.$axios.post(process.env.api + 'api/admin/products/change/accepted', formData)
          .then(function () {
            if (app.paginationPage === app.lastPage && app.data.length === 1) {
              app.paginationPage -= 1
            } else {
              app.GetAllAcceptedProducts()
            }
            app.showNotif('محصول مورد نظر با موفقیت از تایید شده ها حذف شد', 'mdi-checkbox-marked-circle-outline', 'green')
          })
      })
    },

    SetStatusTrue (title, id) {
      const app = this

      this.$q.dialog({
        title: 'هشدار',
        message: 'آیا میخواهید وضعیت تایید محصول ' + ' ( ' + title + ' ) ' + 'نقض شود ؟ ',
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

        app.$axios.post(process.env.api + 'api/admin/products/change/accepted', formData)
          .then(function () {
            if (app.paginationPage === app.lastPage && app.data.length === 1) {
              app.paginationPage -= 1
            } else {
              app.GetAllRejectedProducts()
            }
            app.showNotif('محصول مورد نظر با موفقیت از تایید شده ها حذف شد', 'mdi-checkbox-marked-circle-outline', 'green')
          })
      })
    },

    GetRequiredLists () {
      const app = this

      this.$axios.get(process.env.api + 'api/admin/categories/null/parent/')
        .then(function (response) {
          app.categories_list = response.data
        })

      this.$axios.get(process.env.api + 'api/admin/products/users/list/')
        .then(function (response) {
          app.users_list = response.data
        })

      this.$axios.get(process.env.api + 'api/admin/products/colors/all/WithOutPagination')
        .then(function (response) {
          app.colors_list = response.data
        })

      this.$axios.get(process.env.api + 'api/admin/products/sizes/all/WithOutPagination/')
        .then(function (response) {
          app.sizes_list = response.data
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

    DeleteProduct (name, id) {
      const app = this
      this.$q.dialog({
        title: 'هشدار',
        message: 'آیا میخواهید محصول ' + ' ( ' + name + ' ) ' + 'حذف شود ؟ ',
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
          app.$axios.delete(process.env.api + 'api/admin/products/accepted/' + id)
            .then(function () {
              app.showNotif('محصول مورد نظر با موفقیت حذف شد', 'mdi-checkbox-marked-circle-outline', 'green')

              if (app.paginationPage === app.lastPage && app.data.length === 1) {
                app.paginationPage -= 1
              } else {
                app.GetAllAcceptedProducts()
              }
            })
            .catch(function () {
              app.showNotif('مشکلی به وجود آمده است')
            })
        } else {
          app.$axios.delete(process.env.api + 'api/admin/products/rejected/' + id)
            .then(function () {
              app.showNotif('محصول مورد نظر با موفقیت حذف شد', 'mdi-checkbox-marked-circle-outline', 'green')

              if (app.paginationPage === app.lastPage && app.data.length === 1) {
                app.paginationPage -= 1
              } else {
                app.GetAllRejectedProducts()
              }
            })
            .catch(function () {
              app.showNotif('مشکلی به وجود آمده است')
            })
        }
      })
    },

    EditProduct (id, user, category, status, type) {
      const app = this

      this.$q.loading.show()
      if (this.request_type === 'accepted') {
        this.$axios.get(process.env.api + 'api/admin/products/accepted/' + id + '/')
          .then(function (response) {
            app.form = response.data
            app.form.author = user
            app.form.category = category
            app.status = status
            app.type = type

            app.setDialog('edit')

            app.$q.loading.hide()
          })
      } else {
        this.$axios.get(process.env.api + 'api/admin/products/rejected/' + id + '/')
          .then(function (response) {
            app.form = response.data
            app.form.author = user
            app.form.category = category
            app.status = status
            app.type = type

            app.setDialog('edit')

            app.$q.loading.hide()
          })
      }
    },

    GetAllAcceptedProducts () {
      const app = this

      this.$q.loading.show()

      this.$axios.get(process.env.api + 'api/admin/products/accepted/?page=' + app.paginationPage + '&search=' + app.search)
        .then(function (response) {
          app.data = response.data.results
          app.lastPage = response.data.last_page

          app.$q.loading.hide()
        })
    },

    GetAllRejectedProducts () {
      const app = this

      this.$q.loading.show()

      this.$axios.get(process.env.api + 'api/admin/products/rejected/?page=' + app.paginationPage + '&search=' + app.search)
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
      if (this.tab === 'products_not_accepted_list') {
        this.GetAllRejectedProducts()
      } else {
        this.GetAllAcceptedProducts()
      }
    },
    paginationPage () {
      if (this.paginationPage === 0) {
        this.paginationPage = 1
      }
      if (this.tab === 'products_not_accepted_list') {
        this.GetAllRejectedProducts()
      } else {
        this.GetAllAcceptedProducts()
      }
    },

    tab (value) {
      this.paginationPage = 1

      if (value === 'products_not_accepted_list') {
        this.request_type = 'rejected'
        this.GetAllRejectedProducts()
      } else {
        this.request_type = 'accepted'
        this.GetAllAcceptedProducts()
      }
    }
  },

  components: {
    Modal
  },

  mounted () {
    this.GetAllAcceptedProducts()
    this.GetRequiredLists()
  }
}
</script>

<style scoped>
body {
  background-color: #f5f5f5 !important;
}
</style>
