<template>
  <q-dialog v-model="_dialog">
    <q-card style="width: 750px; max-width: 100vw;">
      <q-card-section class="row items-center q-pa-sm q-mb-sm">
        <div class="q-ml-sm-sm">افزودن سایز</div>
        <q-space/>
        <q-btn class="q-mx-auto" icon="mdi-close" flat round size="sm" style="color: #888888; margin-right: 15px"
               v-close-popup/>
      </q-card-section>
      <q-card-section class="items-center">
        <q-form class="row"
                @submit="onSubmit">
          <div class="col-lg-12 col-xs-12 col-sm-4 col- col-md-4 q-pa-xs q-mb-md">
            <div class="field-label"> عنوان سایز <span class="text-red"
                                                style="font-size: 18px !important;"> * </span></div>
            <q-input v-model="form.title"
                     dense/>
          </div>

          <q-card-actions class="bg-white text-teal">
            <q-btn flat label="انصراف" v-close-popup/>
            <q-btn flat :label="type === 'edit' ?  'ویرایش سایز': 'ثبت سایز'" type="submit"/>
          </q-card-actions>

        </q-form>
      </q-card-section>
    </q-card>
  </q-dialog>
</template>
<script>
export default {
  props: ['showDialog', 'form', 'type'],

  data () {
    return {
      isSlugSame: false
    }
  },

  methods: {
    onSubmit () {
      const app = this

      if (!this.form.title || this.form.title === '') {
        this.showNotif('فیلد عنوان سایز الزامی است')
        return
      }

      const formData = new FormData()
      for (const item in this.form) {
        if (this.form[item] != null) {
          formData.append(item, this.form[item])
        }
      }

      this.$q.loading.show()

      if (this.type === 'create') {
        this.CreateSize(app, formData)
      } else {
        this.UpdateSize(app, formData)
      }
    },

    CreateSize (app, formData) {
      this.$axios.post(process.env.api + 'api/admin/products/sizes/', formData)
        .then(function () {
          app.showNotif('سایز مورد نظر با موفقیت ثبت شد', 'mdi-checkbox-marked-circle-outline ', 'green')
          app.$parent.$parent.GetAllSizes()
          app._dialog = false
        })
        .finally(function () {
        })
        .catch(function (error) {
          for (const item in error.response.data) {
            app.showNotif(item + ' : ' + error.response.data[item][0].replace('.', ''))
            break
          }
        })
    },

    UpdateSize (app, formData) {
      this.$axios.put(process.env.api + 'api/admin/products/sizes/' + app.form.id + '/', formData)
        .then(function () {
          app.showNotif('سایز مورد نظر با موفقیت ویرایش شد', 'mdi-checkbox-marked-circle-outline ', 'green')
          app.$parent.$parent.GetAllSizes()
          app._dialog = false
        })
        .finally(function () {
          app.$q.loading.hide()
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
