<template>
  <q-dialog v-model="_dialog">
    <q-card style="width: 750px; max-width: 100vw;">
      <q-card-section class="row items-center q-pa-sm q-mb-sm">
        <div class="q-ml-sm-sm">افزودن دسته بندی</div>
        <q-space/>
        <q-btn class="q-mx-auto" icon="mdi-close" flat round size="sm" style="color: #888888; margin-right: 15px"
               v-close-popup/>
      </q-card-section>
      <q-card-section class="items-center">
        <q-form class="row"
                @submit="onSubmit">
          <div class="col-lg-12 col-xs-12 col-sm-4 col- col-md-4 q-pa-xs q-mb-md">
            <div class="field-label"> نام <span class="text-red"
                                                       style="font-size: 18px !important;"> * </span></div>
            <q-input v-model="form.name" lazy-rules
                     :rules="[val => val.length > 0 || 'لطفا نام را وارد کنید']"
                     dense />
          </div>

          <div class="col-lg-12 col-xs-12 col-sm-4 col-md-4 q-pa-xs q-mb-md">
            <q-checkbox keep-color v-model="isSlugSame" label="نامک (slug) با عنوان یکی شود" color="cyan" style="float: left !important;" />
             <div class="field-label"> نامک <span class="text-red"
                                                       style="font-size: 18px !important;"> * </span></div>
            <q-input v-model="form.slug" lazy-rules
                     :rules="[val => val.length > 0 || 'لطفا نامک (slug) را وارد کنید']"
                     dense style="margin-top: 6px !important;" />
          </div>

           <q-item class="col-lg-12 col-md-6 col-sm-12 col-xs-12">
            <q-select class="col-12" v-model="form.parent" map-options
                      lazy-rules
                      required
                      :options="parent_list" option-value="id"
                       option-label="name" label="والد*"/>
          </q-item>

          <q-card-actions class="bg-white text-teal">
            <q-btn flat label="انصراف" v-close-popup/>
            <q-btn flat :label="type === 'edit' ?  'ویرایش دسته بندی': 'ثبت دسته بندی'" type="submit"/>
          </q-card-actions>

        </q-form>
      </q-card-section>
    </q-card>
  </q-dialog>
</template>
<script>
export default {
  props: ['showDialog', 'form', 'type', 'parent_list'],

  data () {
    return {
      isSlugSame: false
    }
  },

  methods: {
    onSubmit () {
      const app = this

      // if (!this.form.parent) {
      //   this.form.parent = null
      // } else {
      //   this.form.parent = process.env.api + 'api/admin/categories/parent/' + this.form.parent.id + '/'
      // }

      if (!this.form.parent || this.form.parent.id === 0) {
        this.form.parent = null
      } else {
        this.form.parent = this.form.parent.id
      }

      const formData = new FormData()
      for (const item in this.form) {
        if (this.form[item] != null) {
          formData.append(item, this.form[item])
        }
      }

      this.form.parent = null

      this.$q.loading.show()

      if (this.type === 'create') {
        this.CreateCategory(app, formData)
      } else {
        this.UpdateCategory(app, formData)
      }
    },

    CreateCategory (app, formData) {
      this.$axios.post(process.env.api + 'api/admin/categories/', formData)
        .then(function () {
          app.showNotif('دسته بندی مورد نظر با موفقیت ثبت شد', 'mdi-checkbox-marked-circle-outline ', 'green')
          app._dialog = false
        })
        .finally(function () {
          app.$q.loading.hide()
          app.$parent.$parent.GetAllCategories()
          app.$parent.$parent.GetParentList()
        })
        .catch(function (error) {
          for (const item in error.response.data) {
            app.showNotif(item + ' : ' + error.response.data[item][0].replace('.', ''))
            break
          }
        })
    },

    UpdateCategory (app, formData) {
      this.$axios.put(process.env.api + 'api/admin/categories/' + app.form.id + '/', formData)
        .then(function () {
          app.showNotif('دسته بندی مورد نظر با موفقیت ویرایش شد', 'mdi-checkbox-marked-circle-outline ', 'green')
          app._dialog = false
        })
        .finally(function () {
          app.$q.loading.hide()
          app.$parent.$parent.GetAllCategories()
          app.$parent.$parent.GetParentList()
        })
        .catch(function (error) {
          for (const item in error.response.data) {
            app.showNotif(item + ' : ' + error.response.data[item][0].replace('.', ''))
            break
          }
        })
    },

    showNotif (message, icon = 'error', color = 'red') {
      this.$q.notify({
        message: message,
        icon: icon,
        color: color,
        position: 'bottom-right',
        progress: true
      })
    }
  },

  watch: {
    'form.name': function (value) {
      if (this.isSlugSame) {
        this.form.slug = value.replaceAll(' ', '-')
      }
    },

    'form.slug': function (value) {
      if (!this.isSlugSame) {
        this.form.slug = value.replaceAll(' ', '-')
      }
    },

    isSlugSame: function (value) {
      if (value) {
        this.form.slug = this.form.name.replaceAll(' ', '-')
      }
    }
  },

  computed: {
    _dialog: {
      get () {
        return this.showDialog
      },
      set (value) {
        this.$emit('update:showDialog', value)
      }
    }
  }
}
</script>
