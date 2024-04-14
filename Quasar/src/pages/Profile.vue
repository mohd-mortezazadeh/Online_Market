<template>
  <q-page class="q-pa-sm">
    <div class="row q-col-gutter-sm" style="margin: 10px 12px !important;">
      <div class="col-lg-12 col-md-12 col-xs-12 col-sm-12">
        <q-card class="bg-white text-black ">
          <q-card-section class="text-h6 ">
            <div class="text-h5 text-dark q-mb-md ">ویرایش اطلاعات حساب</div>
          </q-card-section>

          <q-card-section class="q-pa-sm">
            <q-form
              @submit="updateProfile()">
              <q-list class="row">
                <q-item class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
                  <q-item-section side>
                    <div class="field-label q-mb-lg text-grey-8"> تصویر پرفایل
                    </div>
                    <q-item-section class="q-mb-md" side>
                      <q-avatar size="150px">
                        <img :src="getimage(userDetails.image)">
                      </q-avatar>
                    </q-item-section>
                    <q-uploader :hide-upload-btn="true" ref="uploadFile"
                                :style="$q.screen.width <= 481 ? 'width: 100%' : ''"/>
                  </q-item-section>
                </q-item>

                <q-item class="col-lg-6 col-md-6 col-sm-12 col-xs-12">
                  <q-item-section>
                    <div class="field-label text-grey-8">نام کاربری <span class="text-red"
                                                                          style="font-size: 18px !important;">*</span>
                    </div>
                    <q-input dense v-model="userDetails.username" lazy-rules
                             :rules="[val => val.length > 0 || 'لطفا نام کاربری خود را وارد کنید']"/>

                  </q-item-section>
                </q-item>

                <q-item v-if="$store.state.shop.user.is_superuser" class="col-lg-6 col-md-6 col-sm-12 col-xs-12">
                  <q-item-section>
                    <div class="field-label text-grey-8 ">ایمیل <span class="text-red"
                                                                      style="font-size: 18px !important;">*</span>
                    </div>
                    <q-input dense v-model="userDetails.email" lazy-rules
                             type="email"
                             :rules="[val => val.length > 2 || 'لطفا ایمیل خود را وارد کنید']"/>
                  </q-item-section>
                </q-item>

                <q-item v-else class="col-lg-6 col-md-6 col-sm-12 col-xs-12">
                  <q-item-section>
                    <div class="field-label text-grey-8 ">ایمیل <span class="text-red"
                                                                      style="font-size: 18px !important;">*</span>
                    </div>
                    <q-input dense disable :value="userDetails.email"/>
                  </q-item-section>
                </q-item>

                <q-item class="col-lg-6 col-md-6 col-sm-12 col-xs-12">
                  <q-item-section>
                    <div class="field-label text-grey-8">نام</div>
                    <q-input dense v-model="userDetails.first_name"/>

                  </q-item-section>
                </q-item>

                <q-item class="col-lg-6 col-md-6 col-sm-12 col-xs-12">
                  <q-item-section>
                    <div class="field-label text-grey-8 ">نام خانوادگی
                    </div>
                    <q-input dense v-model="userDetails.last_name"/>
                  </q-item-section>
                </q-item>

                <q-item class="col-lg-6 col-md-6 col-sm-12 col-xs-12">
                  <q-item-section>
                    <div class="field-label text-grey-8 ">موبایل
                    </div>
                    <q-input dense v-model="userDetails.phoneNumber" lazy-rules
                             :rules="[val => val.length <= 11 || 'موبایل باید 11 رقم باشد']"/>
                  </q-item-section>
                </q-item>

              </q-list>
              <q-card-actions class="q-mt-lg" align="right">
                <q-btn class="text-capitalize bg-info text-white" type="submit">ذخیره اطلاعات</q-btn>
              </q-card-actions>
            </q-form>
          </q-card-section>

        </q-card>

        <q-card style="margin-top: 50px !important;" class="bg-white text-black ">
          <q-card-section class="text-h6 ">
            <div class="text-h5 text-dark q-mb-md ">تغییر رمز عبور</div>
          </q-card-section>

          <q-card-section class="q-pa-sm">
            <q-form
              @submit="ChangePassword()">
              <q-list class="row">

                <q-item class="col-lg-12 col-md-6 col-sm-12 col-xs-12">
                  <q-item-section>
                    <div class="field-label text-grey-8 "> رمز عبور قدیمی<span class="text-red"
                                                                               style="font-size: 18px !important;">*</span>
                    </div>

                    <q-input v-model="form.old_password" dense :type="isPwd ? 'password' : 'text'" lazy-rules
                             :rules="[val => val.length > 0 || 'لطفا رمز عبور قدیمی خود را وارد کنید']">
                      <template v-slot:append>
                        <q-icon
                          :name="isPwd ? 'visibility_off' : 'visibility'"
                          class="cursor-pointer"
                          @click="isPwd = !isPwd"
                        />
                      </template>
                    </q-input>

                  </q-item-section>
                </q-item>

                <q-item class="col-lg-6 col-md-6 col-sm-12 col-xs-12">
                  <q-item-section>
                    <div class="field-label text-grey-8 "> رمز عبور جدید<span class="text-red"
                                                                              style="font-size: 18px !important;">*</span>
                    </div>

                    <q-input v-model="form.password" dense :type="isPwd ? 'password' : 'text'" lazy-rules
                             :rules="[val => val.length > 0 || 'لطفا رمز عبور جدید خود را وارد کنید']">
                      <template v-slot:append>
                        <q-icon
                          :name="isPwd ? 'visibility_off' : 'visibility'"
                          class="cursor-pointer"
                          @click="isPwd = !isPwd"
                        />
                      </template>
                    </q-input>

                  </q-item-section>
                </q-item>

                <q-item class="col-lg-6 col-md-6 col-sm-12 col-xs-12">
                  <q-item-section>
                    <div class="field-label text-grey-8 "> تکرار رمز عبور جدید<span class="text-red"
                                                                                    style="font-size: 18px !important;">*</span>
                    </div>

                    <q-input v-model="form.password2" dense :type="isPwd ? 'password' : 'text'" lazy-rules
                             :rules="[val => val.length > 0 || 'لطفا تکرار رمز عبور جدید خود را وارد کنید' , val => val === form.password  || 'تکرار رمز عبور و رمز عبور مطابقت ندارد']">
                      <template v-slot:append>
                        <q-icon
                          :name="isPwd ? 'visibility_off' : 'visibility'"
                          class="cursor-pointer"
                          @click="isPwd = !isPwd"
                        />
                      </template>
                    </q-input>

                  </q-item-section>
                </q-item>

              </q-list>
              <q-card-actions class="q-mt-lg" align="right">
                <q-btn class="text-capitalize bg-info text-white" type="submit">تغییر رمز عبور</q-btn>
              </q-card-actions>
            </q-form>
          </q-card-section>
        </q-card>

      </div>
    </div>
  </q-page>
</template>

<script>
export default {
  name: 'UserProfile',
  data () {
    return {
      isPwd: true,

      form: {
        old_password: '',
        password: '',
        password2: ''
      },
      userDetails: []
    }
  },
  methods: {
    updateProfile () {
      const app = this

      if (this.$refs.uploadFile.files[0] && this.$refs.uploadFile.files[0].size > 52428800) {
        app.showNotif('حجم عکس انتخاب شده نباید بیشتر از 50 مگابایت باشد !')
        return
      }

      if (this.$refs.uploadFile.files[0] === undefined) {
        delete this.userDetails.image
      }

      if (this.userDetails.password) {
        delete this.userDetails.password
      }

      const formData = new FormData()
      for (const item in this.userDetails) {
        if (this.userDetails[item] != null) {
          formData.append(item, this.userDetails[item])
        }
      }

      if (this.$refs.uploadFile.files[0] !== undefined) {
        formData.append('image', this.$refs.uploadFile.files[0])
      }

      this.$q.loading.show()

      this.$axios.post(process.env.api + 'api/auth/profile/update/', formData)
        .then(function () {
          if (app.$refs.uploadFile.files[0]) {
            app.$refs.uploadFile.files[0] = undefined
          }
          app.loadData()
          app.showNotif('اطلاعات شما با موفقیت ویرایش شد', 'mdi-checkbox-marked-circle-outline ', 'green')
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

    ChangePassword () {
      const app = this

      this.$q.loading.show()

      this.$axios.put(process.env.api + 'api/auth/password/change/' + app.userDetails.id + '/', app.form)
        .then(function () {
          app.loadData()
          app.showNotif('رمز عبور شما با موفقیت تغییر کرد', 'mdi-checkbox-marked-circle-outline ', 'green')
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

    loadData: function () {
      const app = this
      this.$q.loading.show()
      this.$axios.get(process.env.api + 'api/auth/profile/').then(function (response) {
        app.userDetails = response.data.user

        for (const item in app.userDetails) {
          if (app.userDetails[item] === null) {
            app.userDetails[item] = ''
          }
        }

        app.$q.loading.hide()
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
    },

    getimage (image) {
      if (image) {
        return process.env.api + image.replace('/', '')
      }
      return 'https://i.pinimg.com/originals/51/f6/fb/51f6fb256629fc755b8870c801092942.png'
    }
  },

  mounted () {
    this.loadData()
  }
}
</script>

<style scoped>
body {
  background-color: #f5f5f5 !important;
}
</style>
