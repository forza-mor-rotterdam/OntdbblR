import { Controller } from '@hotwired/stimulus'

let selectOptions = null

export default class extends Controller {
  static targets = ['searchSelect']

  initialize() {
    let self = this
    selectOptions = []
    if (self.hasSearchSelectTarget) {
      const options = self.searchSelectTarget.querySelectorAll('option')
      for (const option in options) {
        selectOptions.push({ value: option.value, label: option.textContent })
      }
    }
  }

  connect() {}
  searchFieldChange(e) {
    let self = this
    if (!self.hasSearchSelectTarget) {
      return
    }
    self.searchSelectTarget.innerHTML = ''
    const re = new RegExp(e.target.value, 'gi')
    for (const selectOption in selectOptions) {
      let option = document.createElement('option')
      if (re.test(selectOption.label)) {
        // let newContent = selectOptions[i].label
        option.value = selectOption.value
        option.textContent = selectOption.label
        // option.innerHTML = newContent.replace(re, function(match) {
        //     return "<mark style='color:red;'>" + match + "</mark>";
        // })
        self.searchSelectTarget.appendChild(option)
      }
    }
  }
}
