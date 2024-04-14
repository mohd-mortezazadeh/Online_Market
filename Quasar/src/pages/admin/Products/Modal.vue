<template>
  <q-dialog v-model="_dialog">
    <q-card style="width: 900px; max-width: 100vw;">
      <q-card-section class="row items-center q-pa-sm q-mb-sm">
        <div class="q-ml-sm-sm">افزودن محصول</div>
        <q-space/>
        <q-btn class="q-mx-auto" icon="mdi-close" flat round size="sm" style="color: #888888; margin-right: 15px"
               v-close-popup/>
      </q-card-section>
      <q-card-section class="items-center">
        <q-form class="row"
                @submit="onSubmit">
          <div class="col-lg-12 col-xs-12 col-sm-4 col- col-md-4 q-pa-xs q-mb-md">
            <div class="field-label"> عنوان <span class="text-red"
                                                  style="font-size: 18px !important;"> * </span></div>
            <q-input v-model="form.title"
                     dense/>
          </div>

          <div class="col-lg-12 col-xs-12 col-sm-4 col-md-4 q-pa-xs q-mb-md">
            <q-checkbox keep-color v-model="isSlugSame" label="نامک (slug) با عنوان یکی شود" color="cyan"
                        style="float: left !important;"/>
            <div class="field-label"> نامک <span class="text-red"
                                                 style="font-size: 18px !important;"> * </span></div>
            <q-input v-model="form.slug"
                     dense style="margin-top: 6px !important;"/>
          </div>

          <div class="col-lg-12 col-xs-12 col-sm-4 col- col-md-4 q-pa-xs q-mb-md">
            <div class="field-label"> قیمت <span class="text-red"
                                                 style="font-size: 18px !important;"> * </span></div>
            <q-input v-model="form.price"
                     dense/>
          </div>

          <div class="col-lg-12 col-xs-12 col-sm-4 col- col-md-4 q-pa-xs q-mb-md">
            <div class="field-label"> تگ ها <span class="text-red"
                                                  style="font-size: 18px !important;"> ( </span> کلمات را با '،' از هم
              جدا کنید <span class="text-red"
                             style="font-size: 18px !important;"> ) </span><span class="text-red"
                                                                                 style="font-size: 18px !important;"> * </span>
            </div>
            <q-input v-model="form.tags"
                     dense/>
          </div>

          <q-item class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
            <q-item-section>
              <div class="field-label"> متن کوتاه <span class="text-red"
                                                        style="font-size: 18px !important;"> * </span></div>
              <q-input style="margin-top: 6px !important; height: 100px" type="textarea"
                       dense
                       v-model="form.short_text"/>
            </q-item-section>
          </q-item>

          <div class="col-lg-12 col-xs-12 col-sm-4 col- col-md-4 q-pa-xs q-mb-md">
            <div class="field-label"> متن <span class="text-red"
                                                style="font-size: 18px !important;"> * </span></div>
            <q-editor
              height="250px"
              v-model="text"
              :definitions="{
        bold: {label: 'Bold', icon: null, tip: 'My bold tooltip'}
      }"
            />
          </div>

          <q-item class="col-lg-12 col-md-6 col-sm-12 col-xs-12">
            <q-select class="col-12" v-model="form.category" map-options :options="categories_list" option-value="id"
                      option-label="name" label="دسته بندی*"/>
          </q-item>

          <q-item class="col-lg-12 col-md-6 col-sm-12 col-xs-12">
            <q-select class="col-12" v-model="form.user" map-options :options="users_list" option-value="id"
                      option-label="username" label="فروشنده*"/>
          </q-item>

          <q-item class="col-lg-12 col-md-6 col-sm-12 col-xs-12">
            <q-select
              map-options
              class="col-12"
              v-model="colors"
              multiple
              :options="colors_list"
              option-label="name"
              option-value="id"
              use-chips
              stack-label
              label="رنگ ها (میتوانید چند نقش را انتخاب کنید)*"
            />
          </q-item>

          <q-item class="col-lg-12 col-md-6 col-sm-12 col-xs-12">
            <q-select
              map-options
              class="col-12"
              v-model="sizes"
              multiple
              :options="sizes_lis"
              option-label="title"
              option-value="id"
              use-chips
              stack-label
              label="سایز ها (میتوانید چند نقش را انتخاب کنید)*"
            />
          </q-item>

          <q-item class="col-lg-12 col-md-6 col-sm-12 col-xs-12">
            <q-select class="col-12" v-model="form.status" map-options :options="status_list" option-value="value"
                      option-label="key" label="وضعیت تایید*"/>
          </q-item>

          <q-item class="col-lg-12 col-md-6 col-sm-12 col-xs-12">
            <q-select class="col-12" v-model="form.type" map-options :options="type_list" option-value="value"
                      option-label="key" label="نوع*"/>
          </q-item>

          <q-item v-if="type === 'edit' && form.original_image" class="col-lg-6 col-md-12 col-sm-12 col-xs-12"
                  style="float: left !important; margin-top: 35px !important; margin-bottom: 30px">

            <q-img
              :src="ShowImage(form.original_image)"
              spinner-color="white"
              style="height: 170px; max-width: 200px"
            />
          </q-item>

          <q-item
            :class="[type === 'edit' && form.original_image ? 'col-lg-6' : 'col-lg-12' , 'col-md-12 col-sm-12 col-xs-12']">
            <q-item-section>
              <div class="field-label"> عکس <span class="text-red"
                                                  style="font-size: 18px !important;"> * </span></div>
              <q-uploader :hide-upload-btn="true" ref="uploadFile"
                          :style="$q.screen.width <= 481 ? 'width: 100%' : ''"/>
            </q-item-section>
          </q-item>

          <q-item
            class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
            <q-item-section>
              <div class="field-label"> سایر عکس ها محصول <span class="text-red"
                                                                style="font-size: 13px !important;">
                (اختیاری) <span v-if="type === 'edit'">({{
                  this.form.images.length
                }} عدد تاکنون آپلود کرده اید)</span> </span></div>

              <q-uploader :hide-upload-btn="true" ref="other_images"
                          multiple
                          batch
                          :style="$q.screen.width <= 481 ? 'width: 100%' : ''"/>
            </q-item-section>
          </q-item>

          <q-card-actions class="bg-white text-teal">
            <q-btn flat label="انصراف" v-close-popup/>
            <q-btn flat :label="type === 'edit' ?  'ویرایش محصول': 'ثبت محصول'" type="submit"/>
          </q-card-actions>

        </q-form>
      </q-card-section>
    </q-card>
  </q-dialog>
</template>
<script>
export default {
  props: ['showDialog', 'form', 'type', 'categories_list', 'users_list', 'colors_list', 'sizes_lis', 'request_type'],

  data () {
    return {
      all_files: [],
      colors: [],
      sizes: [],
      isSlugSame: false,
      status_list: [
        {
          key: 'تایید شده',
          value: true
        },
        {
          key: 'تایید نشده',
          value: false
        }
      ],
      type_list: [
        {
          key: 'رایگان',
          value: 'free'
        },
        {
          key: 'اعضای ویژه',
          value: 'special'
        },
        {
          key: 'نقدی',
          value: 'cash'
        }
      ],

      text: this.form.text !== undefined ? this.form.text : ''
    }
  },

  methods: {
    ShowImage (url) {
      if (url) {
        return url.replace('http://localhost:8000/', process.env.api)
      }
    },

    UploadOtherImages (app, productID) {
      const form = new FormData()
      if (app.$refs.other_images.files.length > 0) {
        for (var i = 0; i < app.$refs.other_images.files.length; i++) {
          const file = app.$refs.other_images.files[i]

          form.append('files[' + i + ']', file)
        }

        form.append('product', productID)

        app.$axios.post(process.env.api + 'api/admin/products/images/create/multiple/', form)
          .then(function (response) {
          })
      }
    },

    onSubmit () {
      const app = this

      if (this.form.price && isNaN(parseInt(this.form.price))) {
        app.showNotif('قیمت باید به صورت عددی وارد شود!')
        return
      }

      if (!this.colors || this.colors.length === 0) {
        app.showNotif('لطفا رنگ ها را انتخاب کنید')
        return
      }

      if (!this.sizes || this.sizes.length === 0) {
        app.showNotif('لطفا سایز ها را انتخاب کنید')
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

      this.form.text = this.text

      if (this.form.user && this.form.user.id !== undefined) {
        this.form.user_id = this.form.user.id
      }

      if (this.form.category && this.form.category.id !== undefined) {
        this.form.category_id = this.form.category.id
      }

      if (this.form.status && this.form.status.value !== undefined) {
        this.form.status = this.form.status.value
      }

      if (this.form.type && this.form.type.value !== undefined) {
        this.form.type = this.form.type.value
      }

      if (this.$refs.uploadFile.files[0] === undefined) {
        delete this.form.original_image
      }

      for (const item in this.colors) {
        if (this.colors[item] !== undefined) {
          this.colors[item] = this.colors[item].id
        }
      }

      for (const item in this.sizes) {
        if (this.sizes[item] !== undefined) {
          this.sizes[item] = this.sizes[item].id
        }
      }

      const formData = new FormData()
      for (const item in this.form) {
        if (this.form[item] != null) {
          formData.append(item, this.form[item])
        }
      }

      for (const item in this.colors) {
        formData.append('color_id', this.colors[item])
      }

      for (const item in this.sizes) {
        formData.append('size_id', this.sizes[item])
      }

      if (this.$refs.uploadFile.files[0] !== undefined) {
        formData.append('original_image', this.$refs.uploadFile.files[0])
      }

      this.$q.loading.show()

      if (this.type === 'create') {
        this.CreateProduct(app, formData)
      } else {
        this.UpdateProduct(app, formData)
      }
    },

    CreateProduct (app, formData) {
      this.$axios.post(process.env.api + 'api/admin/products/accepted/', formData)
        .then(function (response) {
          app.UploadOtherImages(app, response.data.id)

          app.showNotif('محصول مورد نظر با موفقیت ثبت شد', 'mdi-checkbox-marked-circle-outline ', 'green')
          app._dialog = false
          app.$parent.$parent.GetAllAcceptedProducts()
          app.text = ''
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

    UpdateProduct (app, formData) {
      if (this.request_type === 'accepted') {
        this.$axios.put(process.env.api + 'api/admin/products/accepted/' + app.form.id + '/', formData)
          .then(function (response) {
            app.UploadOtherImages(app, response.data.id)

            app.showNotif('محصول مورد نظر با موفقیت ویرایش شد', 'mdi-checkbox-marked-circle-outline ', 'green')
            app._dialog = false
          })
          .finally(function () {
            app.$q.loading.hide()
            app.$parent.$parent.GetAllAcceptedProducts()
          })
          .catch(function (error) {
            for (const item in error.response.data) {
              app.showNotif(item + ' : ' + error.response.data[item][0].replace('.', ''))
              break
            }
          })
      } else {
        this.$axios.put(process.env.api + 'api/admin/products/rejected/' + app.form.id + '/', formData)
          .then(function () {
            app.showNotif('محصول مورد نظر با موفقیت ویرایش شد', 'mdi-checkbox-marked-circle-outline ', 'green')
            app._dialog = false
          })
          .finally(function () {
            app.$q.loading.hide()
            app.$parent.$parent.GetAllRejectedProducts()
          })
          .catch(function (error) {
            for (const item in error.response.data) {
              app.showNotif(item + ' : ' + error.response.data[item][0].replace('.', ''))
              break
            }
          })
      }
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
    'form.title': function (value) {
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
        this.form.slug = this.form.title.replaceAll(' ', '-')
      }
    },

    showDialog: function (value) {
      if (!value) {
        this.text = ''
        this.colors = []
        this.sizes = []
      } else {
        if (this.form.colors && this.form.colors.length > 0) {
          for (const item in this.form.colors) {
            if (this.form.colors[item]) {
              this.colors[item] = this.form.colors[item]
            }
          }
        }
        if (this.form.sizes && this.form.sizes.length > 0) {
          for (const item in this.form.sizes) {
            if (this.form.sizes[item]) {
              this.sizes[item] = this.form.sizes[item]
            }
          }
        }

        if (this.form.text !== undefined) {
          this.text = this.form.text
        }
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
