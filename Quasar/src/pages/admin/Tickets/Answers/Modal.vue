<template>
  <q-dialog v-model="_dialog">
    <q-card style="width: 750px; max-width: 100vw;">
      <q-card-section class="row items-center q-pa-sm q-mb-sm">
        <div class="q-ml-sm-sm">افزودن پاسخ تیکت</div>
        <q-space/>
        <q-btn class="q-mx-auto" icon="mdi-close" flat round size="sm" style="color: #888888; margin-right: 15px"
               v-close-popup/>
      </q-card-section>
      <q-card-section class="items-center">
        <q-form class="row"
                @submit="onSubmit">

          <div class="col-lg-12 col-xs-12 col-sm-4 col- col-md-4 q-pa-xs q-mb-md">
            <div class="field-label"> متن پاسخ <span class="text-red"
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

          <q-item class="col-lg-12 col-md-6 col-sm-12 col-xs-12">
            <q-select class="col-12" v-model="question" map-options
                      :options="question_list" option-value="id"
                      option-label="text" label="پاسخ*"/>
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
      text: '',
      is_first_time: true,
      question: null,
      question_list: []
    }
  },

  methods: {
    GetQuestionsList (ticketID) {
      const app = this

      this.$q.loading.show()

      this.$axios.get(process.env.api + 'api/admin/tickets/all/questions/?ticket=' + ticketID)
        .then(function (response) {
          app.question_list = response.data
          app.$q.loading.hide()
        })
    },

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

      if (!this.question) {
        this.showNotif('لطفا سوال مورد نظر را انتخاب کنید')
        return
      }

      if (!this.form.ticket || this.form.ticket.id === 0) {
        this.form.ticket = null
      } else {
        this.form.ticket = this.form.ticket.id
      }

      if (!this.question || this.question.id === 0) {
        this.form.question = null
      } else {
        this.form.question = this.question.id
      }

      const formData = new FormData()
      for (const item in this.form) {
        if (this.form[item] != null) {
          formData.append(item, this.form[item])
        }
      }

      this.$q.loading.show()

      if (this.type === 'create') {
        this.CreateAnswer(app, formData)
      } else {
        this.UpdateAnswer(app, formData)
      }
    },

    CreateAnswer (app, formData) {
      this.$axios.post(process.env.api + 'api/admin/tickets/answers/', formData)
        .then(function () {
          app.showNotif('دسته بندی مورد نظر با موفقیت ثبت شد', 'mdi-checkbox-marked-circle-outline ', 'green')
          app._dialog = false
        })
        .finally(function () {
          app.$q.loading.hide()
          app.$parent.$parent.GetAllAnswers()
          app.$parent.$parent.GetTicketsList()
        })
        .catch(function (error) {
          for (const item in error.response.data) {
            app.showNotif(item + ' : ' + error.response.data[item][0].replace('.', ''))
            break
          }
        })
    },

    UpdateAnswer (app, formData) {
      this.$axios.put(process.env.api + 'api/admin/tickets/answers/' + app.form.id + '/', formData)
        .then(function () {
          app.showNotif('پاسخ مورد نظر با موفقیت ویرایش شد', 'mdi-checkbox-marked-circle-outline ', 'green')
          app._dialog = false
        })
        .finally(function () {
          app.$q.loading.hide()
          app.$parent.$parent.GetAllAnswers()
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
    'form.ticket': function (value) {
      if (value !== undefined && value !== '' && value !== null && typeof value !== 'number') {
        if (!this.is_first_time) {
          this.question = null
        }
        this.GetQuestionsList(value.id)
      } else {
        this.question_list = []
      }
    },
    _dialog: function (value) {
      if (value === true && this.type === 'edit' && this.form.ticket !== null) {
        this.question = this.form.question
        this.GetQuestionsList(this.form.ticket.id)
      }
      this.is_first_time = false
    },
    showDialog: function (value) {
      if (!value) {
        this.text = ''
        this.question_list = []
        this.question = null
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
