<template>
  <q-dialog v-model="_dialog">
    <q-card style="width: 900px; max-width: 100vw;">
      <q-card-section class="row items-center q-pa-sm q-mb-sm">
        <div class="q-ml-sm-sm">افزودن مقاله</div>
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
            <div class="field-label"> تگ ها <span class="text-red"
                                                  style="font-size: 18px !important;"> ( </span> کلمات را با '،' از هم
              جدا کنید <span class="text-red"
                             style="font-size: 18px !important;"> ) </span><span class="text-red"
                                                                                 style="font-size: 18px !important;"> * </span>
            </div>
            <q-input v-model="form.tags"
                     dense/>
          </div>

          <div class="col-lg-12 col-xs-12 col-sm-4 col- col-md-4 q-pa-xs q-mb-md">
            <div class="field-label"> کلمات کلیدی <span class="text-red"
                                                        style="font-size: 18px !important;"> ( </span> کلمات را با '،'
              از هم جدا کنید <span class="text-red"
                                   style="font-size: 18px !important;"> ) </span><span class="text-red"
                                                                                       style="font-size: 18px !important;"> * </span>
            </div>
            <q-input v-model="form.keywords"
                     dense/>
          </div>

          <q-item class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
            <q-item-section>
              <div class="field-label"> متن کوتاه <span class="text-red"
                                                        style="font-size: 18px !important;"> * </span></div>
              <q-input style="margin-top: 6px !important; height: 100px" type="textarea"
                       dense
                       v-model="form.description"/>
            </q-item-section>
          </q-item>

          <div class="col-lg-12 col-xs-12 col-sm-4 col- col-md-4 q-pa-xs q-mb-md">
            <div class="field-label"> متن <span class="text-red"
                                                style="font-size: 18px !important;"> * </span></div>
            <q-editor
              height="250px"
              v-model="body"
              :definitions="{
        bold: {label: 'Bold', icon: null, tip: 'My bold tooltip'}
      }"
            />
          </div>

          <q-item class="col-lg-12 col-md-6 col-sm-12 col-xs-12">
            <!--            <div class="filed-label" style="color: black !important; margin-top: 6px !important;">استان </div>-->
            <q-select class="col-12" v-model="form.category" map-options :options="categories_list" option-value="id"
                      option-label="name" label="دسته بندی*"/>
          </q-item>

          <q-item class="col-lg-12 col-md-6 col-sm-12 col-xs-12">
            <!--            <div class="filed-label" style="color: black !important; margin-top: 6px !important;">استان </div>-->
            <q-select class="col-12" v-model="form.author" map-options :options="authors_list" option-value="id"
                      option-label="username" label="نویسنده*"/>
          </q-item>

          <q-item class="col-lg-12 col-md-6 col-sm-12 col-xs-12">
            <!--            <div class="filed-label" style="color: black !important; margin-top: 6px !important;">استان </div>-->
            <q-select class="col-12" v-model="form.status" map-options :options="status_list" option-value="value"
                      option-label="key" label="وضعیت*"/>
          </q-item>

          <q-item v-if="type === 'edit' && form.image" class="col-lg-6 col-md-12 col-sm-12 col-xs-12" style="float: left !important;">
              <q-img
                        :src="ShowImage(form.image)"
                        spinner-color="white"
                        style="height: 150px; max-width: 200px"
                      />
          </q-item>

          <q-item :class="[type === 'edit' && form.image ? 'col-lg-6' : 'col-lg-12' , 'col-md-12 col-sm-12 col-xs-12']">
            <q-item-section>
              <div class="field-label"> عکس <span class="text-red"
                                                  style="font-size: 18px !important;"> * </span></div>
              <q-uploader :hide-upload-btn="true" ref="uploadFile"
                          :style="$q.screen.width <= 481 ? 'width: 100%' : ''"/>
            </q-item-section>
          </q-item>

          <q-card-actions class="bg-white text-teal">
            <q-btn flat label="انصراف" v-close-popup/>
            <q-btn flat :label="type === 'edit' ?  'ویرایش مقاله': 'ثبت مقاله'" type="submit"/>
          </q-card-actions>

        </q-form>
      </q-card-section>
    </q-card>
  </q-dialog>
</template>
<script>
export default {
  props: ['showDialog', 'form', 'type', 'categories_list', 'authors_list'],

  data () {
    return {
      isSlugSame: false,
      status_list: [
        {
          key: 'پیش نویس',
          value: 0
        },
        {
          key: 'منتشر شده',
          value: 1
        },
        {
          key: 'پایان انتشار',
          value: 2
        }
      ],
      body: this.form.body !== undefined ? this.form.body : ''
    }
  },

  methods: {
    ShowImage (url) {
      if (url) {
        return url.replace('http://localhost:8000/', process.env.api)
      }
    },

    onSubmit () {
      const app = this

      if (!this.$refs.uploadFile.files[0]) {
        app.showNotif('لطفا عکس مقاله خود را وارد کنید !')
        return
      } else if (this.$refs.uploadFile.files[0] && this.$refs.uploadFile.files[0].size > 52428800) {
        app.showNotif('حجم عکس انتخاب شده نباید بیشتر از 50 مگابایت باشد !')
        return
      }

      this.form.body = this.body

      if (this.form.author && this.form.author.id !== undefined) {
        this.form.author = this.form.author.id
      }

      if (this.form.category && this.form.category.id !== undefined) {
        this.form.category = this.form.category.id
      }

      if (this.form.status && this.form.status.value !== undefined) {
        this.form.status = this.form.status.value
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
        this.CreateArticle(app, formData)
      } else {
        this.UpdateArticle(app, formData)
      }
    },

    CreateArticle (app, formData) {
      this.$axios.post(process.env.api + 'api/admin/articles/', formData)
        .then(function () {
          app.showNotif('مقاله مورد نظر با موفقیت ثبت شد', 'mdi-checkbox-marked-circle-outline ', 'green')
          app._dialog = false
          app.$parent.$parent.GetAllArticles()
          app.body = ''
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

    UpdateArticle (app, formData) {
      this.$axios.put(process.env.api + 'api/admin/articles/' + app.form.id + '/', formData)
        .then(function () {
          app.showNotif('مقاله مورد نظر با موفقیت ویرایش شد', 'mdi-checkbox-marked-circle-outline ', 'green')
          app._dialog = false
        })
        .finally(function () {
          app.$q.loading.hide()
          app.$parent.$parent.GetAllArticles()
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
        this.body = ''
      } else {
        if (this.form.body !== undefined) {
          this.body = this.form.body
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
