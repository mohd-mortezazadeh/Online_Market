<template>
  <div class="q-pa-md">
    <div class="q-gutter-y-md">
      <q-card>
        <q-tabs
          align="left"
          v-model="tab"
          class="text-teal text-info"
        >
          <q-tab class="text-primary" name="categories_list" icon="mdi-format-list-text" label="دسته بندی ها"/>
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
              <q-btn color="primary" outline @click="setDialog('create')" icon="mdi-file-plus-outline" label="افزودن دسته بندی"/>
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
                    <q-td key="slug">{{ props.row.slug }}</q-td>
                    <q-td key="parent">{{ props.row.parent ? props.row.parent['name'] : '' }}</q-td>
                    <q-td key="setting">
                      <q-btn @click="EditCategory(props.row.id , props.row.parent)" style="color: #4facfe" rounded icon="mdi-square-edit-outline" label="ویرایش" size="md" flat
                             dense>
                        <q-tooltip>ویرایش</q-tooltip>
                      </q-btn>
                      |
                      <q-btn @click="DeleteCategory(props.row.name , props.row.id)" style="color: red" rounded
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

        <Modal :showDialog.sync="showDialog" :form="form" :type="type" :parent_list="parent_list"></Modal>
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
      parent_list: [],

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
          name: 'parent',
          align: 'left',
          label: 'والد',
          field: 'parent',
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
    GetParentList (selfID = 0) {
      const app = this

      this.$axios.get(process.env.api + 'api/admin/categories/parent_list/' + selfID)
        .then(function (response) {
          app.parent_list = response.data
          app.parent_list.unshift({ id: 0, name: 'هیچکدام' })
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

    DeleteCategory (name, id) {
      const app = this
      this.$q.dialog({
        title: 'هشدار',
        message: 'آیا میخواهید دسته بندی ' + ' ( ' + name + ' ) ' + 'حذف شود ؟ ',
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
        app.$axios.delete(process.env.api + 'api/admin/categories/' + id)
          .then(function (response) {
            app.showNotif('دسته بندی مورد نظر با موفقیت حذف شد', 'mdi-checkbox-marked-circle-outline', 'green')
            app.GetAllCategories()
            app.GetParentList()
          })
          .catch(function () {
            app.showNotif('مشکلی به وجود آمده است')
          })
      })
    },

    EditCategory (id, parentID) {
      const app = this

      this.$q.loading.show()
      this.$axios.get(process.env.api + 'api/admin/categories/' + id + '/')
        .then(function (response) {
          app.form = response.data
          app.form.parent = parentID
          app.setDialog('edit')

          app.GetParentList(id)

          app.$q.loading.hide()
        })
    },

    GetParentRelations () {
      const app = this

      for (const item in app.data) {
        if (app.data[item].parent !== null) {
          this.$axios.get(process.env.api + 'api/admin/categories/parent/' + app.data[item].parent)
            .then(function (response) {
              app.data[item].parent = response.data
            })
        }
      }

      this.$q.loading.hide()
    },

    GetAllCategories () {
      const app = this

      this.$q.loading.show()

      this.$axios.get(process.env.api + 'api/admin/categories/?page=' + app.paginationPage + '&search=' + app.search)
        .then(function (response) {
          app.data = response.data.results
          app.lastPage = response.data.last_page
          app.GetParentRelations()
        })
    }
  },

  watch: {
    search () {
      this.GetAllCategories()
    },
    paginationPage () {
      this.GetAllCategories()
    }
  },

  components: {
    Modal
  },

  mounted () {
    this.GetAllCategories()
    this.GetParentList()
  }
}
</script>

<style scoped>
body {
  background-color: #f5f5f5 !important;
}
</style>
