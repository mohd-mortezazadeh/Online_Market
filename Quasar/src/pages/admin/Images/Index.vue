<template>
  <div class="q-pa-md">
    <div class="q-gutter-y-md">
      <q-card>
        <q-tabs
          align="left"
          v-model="tab"
          class="text-teal text-info"
        >
          <q-tab class="text-primary" name="categories_list" icon="mdi-format-list-text" label="عکس های محصولات"/>
        </q-tabs>
        <q-separator/>

        <q-tab-panels v-model="tab" animated>
          <q-tab-panel name="categories_list">
            <q-input style="width: 300px; float: left !important;"
                     dense v-model.lazy="search"
                     debounce="250"
                     filled type="search">
              <template v-slot:append>
                <q-icon name="search"/>
              </template>
            </q-input>

            <div class="q-pl-md q-gutter-sm">
              <q-btn color="primary" outline @click="setDialog('create')" icon="mdi-file-plus-outline" label="افزودن عکس محصول"/>
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
                    <q-td key="title">{{ props.row.product.title }}</q-td>
                     <q-td key="image">
                      <q-img
                        :src="ShowImage(props.row.image)"
                        spinner-color="white"
                        style="height: 80px; max-width: 60px"
                      />
                    </q-td>
                      <q-td key="created_at">{{ props.row.product.created_at | FormatDate }}</q-td>
                    <q-td key="setting">
                      <q-btn @click="EditImage(props.row.id , props.row.product)" style="color: #4facfe" rounded icon="mdi-square-edit-outline" label="ویرایش" size="md" flat
                             dense>
                        <q-tooltip>ویرایش</q-tooltip>
                      </q-btn>
                      |
                      <q-btn @click="DeleteImage(props.row.product.title , props.row.id)" style="color: red" rounded
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

        <Modal :showDialog.sync="showDialog" :form="form" :type="type" :product_list="product_list"></Modal>
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
      product_list: [],

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
          name: 'product',
          align: 'left',
          label: 'محصول',
          field: 'product',
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

      tab: 'categories_list',
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
    ShowImage (image) {
      return image.replace('http://localhost:8000/', process.env.api)
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

    DeleteImage (name, id) {
      const app = this
      this.$q.dialog({
        title: 'هشدار',
        message: 'آیا میخواهید این عکس از گالری محصول ' + ' ( ' + name + ' ) ' + 'حذف شود ؟ ',
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
        app.$axios.delete(process.env.api + 'api/admin/products/images/' + id)
          .then(function (response) {
            app.showNotif('عکس  مورد نظر با موفقیت حذف شد', 'mdi-checkbox-marked-circle-outline', 'green')
            app.GetAllImages()
            // app.GetParentList()
          })
          .catch(function () {
            app.showNotif('مشکلی به وجود آمده است')
          })
      })
    },

    EditImage (id, product) {
      const app = this

      this.$q.loading.show()
      this.$axios.get(process.env.api + 'api/admin/products/images/' + id + '/')
        .then(function (response) {
          app.form = response.data
          app.form.product = product
          app.setDialog('edit')

          app.$q.loading.hide()
        })
    },

    GetRelations () {
      const app = this

      for (const item in app.data) {
        if (app.data[item].product !== null) {
          this.$axios.get(process.env.api + 'api/admin/products/accepted/' + app.data[item].product)
            .then(function (response) {
              app.data[item].product = response.data
            })
        }
      }

      this.$q.loading.hide()
    },

    GetProductList () {
      const app = this

      this.$axios.get(process.env.api + 'api/admin/products/WithOutPagination/')
        .then(function (response) {
          app.product_list = response.data
        })
    },

    GetAllImages () {
      const app = this

      this.$q.loading.show()

      this.$axios.get(process.env.api + 'api/admin/products/images/?page=' + app.paginationPage + '&search=' + app.search)
        .then(function (response) {
          app.data = response.data.results
          app.lastPage = response.data.last_page
          app.GetRelations()
        })
    }
  },

  watch: {
    search () {
      this.GetAllImages()
    },
    paginationPage () {
      this.GetAllImages()
    }
  },

  components: {
    Modal
  },

  mounted () {
    this.GetAllImages()
    this.GetProductList()
  }
}
</script>

<style scoped>
body {
  background-color: #f5f5f5 !important;
}
</style>
