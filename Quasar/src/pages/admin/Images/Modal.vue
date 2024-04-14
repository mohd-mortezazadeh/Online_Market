<template>
  <q-dialog v-model="_dialog">
    <q-card style="width: 750px; max-width: 100vw;">
      <q-card-section class="row items-center q-pa-sm q-mb-sm">
        <div class="q-ml-sm-sm">افزودن عکس محصول</div>
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
                      :options="product_list" option-value="id"
                      option-label="title" label="محصول*"/>
          </q-item>

          <q-item v-if="type === 'edit' && form.image" class="col-lg-6 col-md-12 col-sm-12 col-xs-12"
                  style="float: left !important;">
            <q-img
              :src="ShowImage(form.image)"
              spinner-color="white"
              style="height: 150px; max-width: 200px"
            />
          </q-item>

          <q-item
            :class="[type === 'edit' && form.image ? 'col-lg-6' : 'col-lg-12' , 'col-md-12 col-sm-12 col-xs-12']">
            <q-item-section>
              <div class="field-label"> عکس <span class="text-red"
                                                  style="font-size: 18px !important;"> * </span></div>
              <q-uploader :hide-upload-btn="true" ref="uploadFile"
                          :style="$q.screen.width <= 481 ? 'width: 100%' : ''"/>
            </q-item-section>
          </q-item>

          <q-card-actions class="bg-white text-teal">
            <q-btn flat label="انصراف" v-close-popup/>
            <q-btn flat :label="type === 'edit' ?  'ویرایش عکس محصول': 'ثبت عکس محصول'" type="submit"/>
          </q-card-actions>

        </q-form>
      </q-card-section>
    </q-card>
  </q-dialog>
</template>
<script>
export default {
  props: ['showDialog', 'form', 'type', 'product_list'],

  data () {
    return {
      isSlugSame: false
    }
  },

  methods: {
    ShowImage (image) {
      return image.replace('http://localhost:8000/', process.env.api)
    },

    onSubmit () {
      const app = this

      if (!this.form.product || this.form.product.id === 0) {
        app.showNotif('فیلد محصول الزامی است')
        return
      }

      if (this.type === 'create') {
        if (!this.$refs.uploadFile.files[0]) {
          app.showNotif('لطفا عکس محصول خود را وارد کنید !')
          return
        } else if (this.$refs.uploadFile.files[0] && this.$refs.uploadFile.files[0].size > 52428800) {
          app.showNotif('حجم عکس انتخاب شده نباید بیشتر از 50 مگابایت باشد !')
          return
        }
      }

      if (!this.form.product || this.form.product.id === 0) {
        this.form.product = null
      } else {
        this.form.product = this.form.product.id
      }

      if (this.$refs.uploadFile.files[0] === undefined) {
        delete this.form.image
      }

      const formData = new FormData()
      for (const item in this.form) {
        if (this.form[item] != null) {
          formData.append(item, this.form[item])
        }
      }

      if (this.$refs.uploadFile.files[0] !== undefined) {
        formData.append('image', this.$refs.uploadFile.files[0])
      }

      this.$q.loading.show()

      if (this.type === 'create') {
        this.CreateImage(app, formData)
      } else {
        this.UpdateImage(app, formData)
      }
    },

    CreateImage (app, formData) {
      this.$axios.post(process.env.api + 'api/admin/products/images/', formData)
        .then(function () {
          app.showNotif('عکس محصول مورد نظر با موفقیت ثبت شد', 'mdi-checkbox-marked-circle-outline ', 'green')
          app._dialog = false
        })
        .finally(function () {
          app.$q.loading.hide()
          app.$parent.$parent.GetAllImages()
          app.$parent.$parent.GetProductList()
        })
        .catch(function (error) {
          for (const item in error.response.data) {
            app.showNotif(item + ' : ' + error.response.data[item][0].replace('.', ''))
            break
          }
        })
    },

    UpdateImage (app, formData) {
      this.$axios.put(process.env.api + 'api/admin/products/images/' + app.form.id + '/', formData)
        .then(function () {
          app.showNotif('عکس محصول مورد نظر با موفقیت ویرایش شد', 'mdi-checkbox-marked-circle-outline ', 'green')
          app._dialog = false
        })
        .finally(function () {
          app.$q.loading.hide()
          app.$parent.$parent.GetAllImages()
          app.$parent.$parent.GetProductList()
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
