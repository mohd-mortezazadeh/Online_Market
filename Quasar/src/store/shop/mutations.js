import _ from 'lodash'

export function setUser (state, user) {
  state.user = _.cloneDeep(user)
}
