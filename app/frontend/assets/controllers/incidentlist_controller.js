import { Controller } from '@hotwired/stimulus'
import L from 'leaflet'

let showSortingContainer = false
let sortDirectionReversed = false
let currentPosition = null
const orderOptions = ['Datum', 'Adres', 'Afstand', 'Postcode']
let activeOrder = orderOptions[0]
// const url =
//   'https://service.pdok.nl/brt/achtergrondkaart/wmts/v2_0/{layerName}/{crs}/{z}/{x}/{y}.{format}'

export default class extends Controller {
  static outlets = ['kaart']
  static targets = ['sorting', 'toggleMapView', 'taakAfstand', 'taakItem', 'taakItemLijst']

  initialize() {
    let self = this
    self.element[self.identifier] = self
    self.element.addEventListener('orderChangeEvent', function (e) {
      self.sorterenOp(e.detail.order)
      self.saveSortedList(e.detail.order)
    })

    if (self.hasSortingTarget && showSortingContainer === true) {
      self.sortingTarget.classList.remove('hidden-vertical')
      self.sortingTarget.classList.add('show-vertical')
    }
    self.setStyleOrder(activeOrder)
    let kaartMarkers = []
    for (const taakItem in self.taakItemTargets) {
      if (taakItem.dataset.geometrie != '') {
        kaartMarkers.push({
          geometrie: JSON.parse(taakItem.dataset.geometrie),
          adres: taakItem.dataset.adres,
          afbeeldingUrl: taakItem.dataset.afbeeldingUrl,
          taakId: taakItem.dataset.id,
          titel: taakItem.dataset.titel,
        })
      }
    }
    self.kaartOutlet.plotMarkers(kaartMarkers)

    self.element.addEventListener('markerSelectedEvent', function (e) {
      self.selecteerTaakItem(e.detail.taakId)
    })
    self.element.addEventListener('markerDeselectedEvent', function (e) {
      self.deselecteerTaakItem(e.detail.taakId)
    })
    window.addEventListener('positionChangeEvent', function (e) {
      console.log('positionChangeEvent')
      console.log(e.detail)
      self.positionWatchSuccess(e.detail.position)
    })
    self.element.addEventListener('kaartModusChangeEvent', function (e) {
      self.kaartOutlet.kaartModusChangeHandler(e.detail.kaartModus, e.detail.requestType)
    })
    let childControllerConnectedEvent = new CustomEvent('childControllerConnectedEvent', {
      bubbles: true,
      cancelable: false,
      detail: {
        controller: self,
      },
    })

    window.dispatchEvent(childControllerConnectedEvent)
  }
  connect() {}
  taakAfstandTargetConnected(element) {
    const markerLocation = new L.LatLng(element.dataset.latitude, element.dataset.longitude)
    element.textContent = Math.round(markerLocation.distanceTo(currentPosition))
  }
  selecteerTaakItem(taakId) {
    let self = this
    for (const taakItem of self.taakItemTargets) {
      if (taakItem.dataset.id == taakId) {
        taakItem.classList.add('selected')
        taakItem.scrollIntoView({
          behavior: 'smooth',
          block: 'end',
          inline: 'nearest',
        })
      } else {
        taakItem.classList.remove('selected')
      }
    }
  }
  deselecteerTaakItem() {
    let self = this
    for (const taakItem in self.taakItemTargets) {
      taakItem.classList.remove('selected')
    }
  }
  positionWatchSuccess(position) {
    let self = this
    console.log('positionWatchSuccess')
    currentPosition = [position.coords.latitude, position.coords.longitude]
    if (self.hasKaartOutlet) {
      self.kaartOutlet.positionChangeEvent(position)
    }
    if (self.hasTaakAfstandTarget) {
      for (const taakAfstand in self.taakAfstandTargets) {
        const markerLocation = new L.LatLng(
          taakAfstand.dataset.latitude,
          taakAfstand.dataset.longitude
        )
        const afstand = Math.round(markerLocation.distanceTo(currentPosition))
        taakAfstand.textContent = afstand
        const listItem = taakAfstand.closest('.list-item')

        if (listItem) {
          listItem.dataset.orderAfstand = afstand
          if (activeOrder == 'Afstand') {
            listItem.style.order = parseInt(afstand)
          }
        }
      }
    }
  }
  selectTaakMarker(e) {
    let self = this
    self.kaartOutlet.selectTaakMarker(e.params.taakId)
  }
  setStyleOrder(order) {
    let self = this
    for (const taakItem of self.taakItemTargets) {
      taakItem.style.order = taakItem.dataset[`order${order}`]
    }
  }
  sorterenOp(order) {
    let self = this
    console.log('order', order)
    let selectedOrder = order.split('-')[0]
    if (selectedOrder != activeOrder) {
      self.setStyleOrder(selectedOrder)
    }
    activeOrder = selectedOrder
    self.taakItemLijstTarget.classList[order.split('-').length > 1 ? 'remove' : 'add']('reverse')
    self.taakItemLijstTarget.scrollTop = 0
  }

  saveSortedList(order) {
    let initialSortedList = Array.from(document.querySelectorAll('.list-item'))

    let newSortedList = initialSortedList.map((taakItem) => {
      return Number(taakItem.getAttribute('data-id'))
    })

    if (order.split('-').length < 2) {
      newSortedList.reverse()
    }
    sessionStorage.setItem('taakIdList', newSortedList)
  }

  disconnect() {
    console.log('disconnect')
  }

  toggleMapView() {
    this.element.classList.toggle('showMap')
  }
  onGroup(e) {
    console.log('onGroup', e.target.checked)
    const frame = document.getElementById('incidents_list')
    const url = `${frame.dataset.src}?grouped-by=${e.target.checked}`
    frame.setAttribute('src', url)
  }

  onToggleSortingContainer() {
    let self = this
    self.sortingTarget.classList.toggle('hidden-vertical')
    self.sortingTarget.classList.toggle('show-vertical')
    showSortingContainer = !showSortingContainer
    sortDirectionReversed = sortDirectionReversed === undefined ? false : true
  }

  onSort(e) {
    const frame = document.getElementById('incidents_list')
    const url = `${frame.dataset.src}?sort-by=${e.target.value}`
    frame.setAttribute('src', url)
  }
}
