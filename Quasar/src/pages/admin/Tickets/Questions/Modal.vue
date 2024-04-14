<template>
  <q-dialog v-model="_dialog">
    <q-card style="width: 750px; max-width: 100vw;">
      <q-card-section class="row items-center q-pa-sm q-mb-sm">
        <div class="q-ml-sm-sm">افزودن سوال تیکت</div>
        <q-space/>
        <q-btn class="q-mx-auto" icon="mdi-close" flat round size="sm" style="color: #888888; margin-right: 15px"
               v-close-popup/>
      </q-card-section>
      <q-card-section class="items-center">
        <q-form class="row"
                @submit="onSubmit">

          <div class="col-lg-12 col-xs-12 col-sm-4 col- col-md-4 q-pa-xs q-mb-md">
            <div class="field-label"> متن سوال <span class="text-red"
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
            <q-select class="col-12" v-model="form.ticket" map-options
                      :options="tickets_list" option-value="id"
                      option-label="title" label="تیکت*"/>
          </q-item>

          <q-card-actions class="bg-white text-teal">
            <q-btn flat label="انصراف" v-close-popup/>
            <q-btn flat :label="type === 'edit' ?  'ویرایش سوال': 'ثبت سوال'" type="submit"/>
          </q-card-actions>

        </q-form>
      </q-card-section>
    </q-card>
  </q-dialog>
</template>
<script>
export default {
  props: ['showDialog', 'form', 'type', 'tickets_list'],

  data () {
    return {
      text: this.form.text !== undefined ? this.form.text : ''
    }
  },

  methods: {
    onSubmit () {
      const app = this

      if (!this.text) {
        this.showNotif('لطفا متن سوال را وارد کنید')
        return
      } else {
        this.form.text = this.text
      }

      if (!this.form.ticket) {
        this.showNotif('لطفا تیکت مورد نظر را انتخاب کنید')
        return
      }

      if (!this.form.ticket || this.form.ticket.id === 0) {
        this.form.ticket = null
      } else {
        this.form.ticket = this.form.ticket.id
      }

      const formData = new FormData()
      for (const item in this.form) {
        if (this.form[item] != null) {
          formData.append(item, this.form[item])
        }
      }

      this.$q.loading.show()

      if (this.type === 'create') {
        this.CreateQuestion(app, formData)
      } else {
        this.UpdateQuestion(app, formData)
      }
    },

    CreateQuestion (app, formData) {
      this.$axios.post(process.env.api + 'api/admin/tickets/questions/', formData)
        .then(function () {
          app.showNotif('دسته بندی مورد نظر با موفقیت ثبت شد', 'mdi-checkbox-marked-circle-outline ', 'green')
          app._dialog = false
        })
        .finally(function () {
          app.$q.loading.hide()
          app.$parent.$parent.GetAllQuestions()
          app.$parent.$parent.GetTicketsList()
        })
        .catch(function (error) {
          for (const item in error.response.data) {
            app.showNotif(item + ' : ' + error.response.data[item][0].replace('.', ''))
            break
          }
        })
    },

    UpdateQuestion (app, formData) {
      this.$axios.put(process.env.api + 'api/admin/tickets/questions/' + app.form.id + '/', formData)
        .then(function () {
          app.showNotif('سوال مورد نظر با موفقیت ویرایش شد', 'mdi-checkbox-marked-circle-outline ', 'green')
          app._dialog = false
        })
        .finally(function () {
          app.$q.loading.hide()
          app.$parent.$parent.GetAllQuestions()
          app.$parent.$parent.GetTicketsList()
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
    showDialog: function (value) {
      if (!value) {
        this.text = ''
      } else {
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
