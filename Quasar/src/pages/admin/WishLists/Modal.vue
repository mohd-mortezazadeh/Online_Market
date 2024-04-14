<template>
  <q-dialog v-model="_dialog">
    <q-card style="width: 750px; max-width: 100vw;">
      <q-card-section class="row items-center q-pa-sm q-mb-sm">
        <div class="q-ml-sm-sm">افزودن علاقه مندی</div>
        <q-space/>
        <q-btn class="q-mx-auto" icon="mdi-close" flat round size="sm" style="color: #888888; margin-right: 15px"
               v-close-popup/>
      </q-card-section>
      <q-card-section class="items-center">
        <q-form class="row"
                @submit="onSubmit">
          <q-item class="col-lg-12 col-md-6 col-sm-12 col-xs-12">
            <q-select class="col-12" v-model="form.product" map-options
                      lazy-rules
                      required
                      :options="products_list" option-value="id"
                      option-label="title" label="محصول*"/>
          </q-item>

          <q-item class="col-lg-12 col-md-6 col-sm-12 col-xs-12">
            <q-select class="col-12" v-model="form.user" map-options
                      lazy-rules
                      required
                      :options="users_list" option-value="id"
                      option-label="username" label="کاربر*"/>
          </q-item>

          <q-card-actions class="bg-white text-teal">
            <q-btn flat label="انصراف" v-close-popup/>
            <q-btn flat :label="type === 'edit' ?  'ویرایش علاقه مندی': 'ثبت علاقه مندی'" type="submit"/>
          </q-card-actions>

        </q-form>
      </q-card-section>
    </q-card>
  </q-dialog>
</template>
<script>
export default {
  props: ['showDialog', 'form', 'type', 'users_list', 'products_list'],

  data () {
    return {
      isSlugSame: false
    }
  },

  methods: {
    onSubmit () {
      const app = this

      if (!this.form.product || this.form.product.id === 0) {
        app.showNotif('فیلد محصول الزامی است')
        return
      }

      if (!this.form.user || this.form.user.id === 0) {
        app.showNotif('فیلد کاربر الزامی است')
        return
      }

      if (!this.form.product || this.form.product.id === 0) {
        this.form.product_id = null
      } else {
        this.form.product_id = this.form.product.id
      }

      if (!this.form.user || this.form.user.id === 0) {
        this.form.user_id = null
      } else {
        this.form.user_id = this.form.user.id
      }

      const formData = new FormData()
      for (const item in this.form) {
        if (this.form[item] != null) {
          formData.append(item, this.form[item])
        }
      }

      this.$q.loading.show()

      if (this.type === 'create') {
        this.CreateWishList(app, formData)
      } else {
        this.UpdateWishList(app, formData)
      }
    },

    CreateWishList (app, formData) {
      this.$axios.post(process.env.api + 'api/admin/wishlists/', formData)
        .then(function () {
          app.showNotif('علاقه مندی مورد نظر با موفقیت ثبت شد', 'mdi-checkbox-marked-circle-outline ', 'green')
          app.$parent.$parent.GetAllWishLists()
          app.$parent.$parent.GetRequiredList()
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

    UpdateWishList (app, formData) {
      this.$axios.put(process.env.api + 'api/admin/wishlists/' + app.form.id + '/', formData)
        .then(function () {
          app.showNotif('علاقه مندی مورد نظر با موفقیت ویرایش شد', 'mdi-checkbox-marked-circle-outline ', 'green')
          app.$parent.$parent.GetAllWishLists()
          app.$parent.$parent.GetRequiredList()
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
