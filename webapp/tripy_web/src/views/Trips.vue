<template>
  <div>
    <section class="hero is-primary is-fullheight" style="margin-top:-54px">
      <div class="hero-body">
        <div class="container">
          <div v-if="error" class="notification is-danger" style="margin-top:24px">
            <button class="delete"></button>
            {{error}}
          </div>
          <div class="card">
            <div class="card-header" style="padding:24px; justify-content: flex-end">
              <button class='button is-info' @click="showModal">Add new Trip</button>
              <button v-if="this.role == 'user'" class='button is-primary' @click="downloadTrips">Download Monthly Trips</button>
            </div>
            <div class="card-content" style="min-height:500px">
              <div style="margin-bottom:24px">
                <div class="field">
                  <div class="control">
                    <input type="email" v-model="q" @keyup="search" placeholder="type here to filter" class="input">
                  </div>
                </div>
              </div>
              <table id="content" class="table is-striped is-bordered is-fullwidth">
                <thead>
                  <tr>
                    <th v-if="role=='admin'">User</th>
                    <th>Destination</th>
                    <th>Start Date</th>
                    <th>End Date</th>
                    <th>Comment</th>
                    <th></th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(trip, i) in trips" :key="trip.pk">
                    <td v-if="role=='admin'">{{trip.user.email}}</td>
                    <td>{{trip.destination}}<p v-if="trip.days_left > 0" class="help is-info">{{trip.days_left}} days to go!</p></td>
                    <td>{{trip.start_date}}</td>
                    <td>{{trip.end_date}}</td>
                    <td>{{trip.comment}}</td>
                    <td>
                      <button class="button is-primary is-pulled-right" @click="openEditTrip(i)">Edit</button>
                      <button class="button is-danger is-pulled-right" @click="deleteTrip(trip.pk)">Delete</button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div class="card-footer" style="padding:24px; justify-content: flex-end">
              <div>
                <nav class="pagination is-small" role="navigation" aria-label="pagination">
                  <ul class="pagination-list">
                    <li v-if="!isFirstPage" @click="changePage(pagination.current_page - 1)"><a class="pagination-link" >Previous</a></li>
                    <li v-for="page in pages" :key="page" @click="changePage(page)"><a class="pagination-link" :class="{ 'is-current': isCurrent(page) }">{{page}}</a></li>
                    <li v-if="!isLastPage" @click="changePage(pagination.current_page + 1)"><a class="pagination-link" >Next</a></li>
                  </ul>
                </nav>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="modal" :class="{ 'is-active': modal.active }">
        <div class="modal-background"></div>
        <div class="modal-card">
          <header class="modal-card-head">
            <p v-if="modal.editView" class="modal-card-title">Edit Trip details</p>
            <p v-else class="modal-card-title">Add a new Trip</p>
            <button class="delete" aria-label="close" @click="hideModal"></button>
          </header>
          <section class="modal-card-body">
            <div>
                <p v-if="modal.error" class="help is-danger">{{modal.error}}</p>
                <div class="field" v-if="role=='admin'">
                  <label for="" class="label">User</label>
                  <div class="control">
                    <input type="text" placeholder="e.g. bobsmith@gmail.com" class="input" required v-model="newTrip.user.email" >

                  </div>
                </div>
                <div class="field">
                  <label for="" class="label">Destination</label>
                  <div class="control">
                    <input type="text" placeholder="e.g. bobsmith@gmail.com" class="input" required v-model="newTrip.destination">
                  </div>
                </div>
                
                <div class="field">
                  <label for="" class="label">Start Date</label>
                  <div class="control">
                    <input type="date" placeholder="e.g. bobsmith@gmail.com" class="input" required v-model="newTrip.start_date">

                  </div>
                </div>
                
                <div class="field">
                  <label for="" class="label">End Date</label>
                  <div class="control">
                    <input type="date" placeholder="e.g. bobsmith@gmail.com" class="input" required v-model="newTrip.end_date">

                  </div>
                </div>
                
                <div class="field">
                  <label for="" class="label">Comments</label>
                  <div class="control">
                    <textarea class="textarea" required v-model="newTrip.comment" rows=4></textarea>
                  </div>
                </div>
              </div>
          </section>
          <footer class="modal-card-foot">
            <button class="button is-success" @click="modalSave">Save changes</button>
            <button class="button" @click="hideModal">Cancel</button>
          </footer>
        </div>
      </div>
    </section>
  </div>
</template>
<script>
import { AuthAPIService } from '../utils/api.service';
import { PDFGenerator } from '../utils/pdf.service';


export default {
  data(){
    return {
      error: null,
      trips: [],
      q: "",
      newTrip: {
        start_date: "",
        end_date: "",
        destination: "",
        comment: "",
        id: null,
        user: {
          email: "",
          id: null
        },
      },
      modal: {
        active: false,
        editView: false,
        error: null
      },
      pagination: {
        total_pages: 1,
        current_page: 1
      }
    }
  },
  mounted(){
    this.fetchTrips()
  },
  methods: {
    validateEmail() {
      if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,6})+$/.test(this.newTrip.user.email)){
        return true
      }else{
        this.modal.error = "Please enter a valid email"
        return false
      }
    },
    validateTripForm(){
      if((this.newTrip.destination == "") || (this.newTrip.start_date == "") || (this.newTrip.end_date == "") || (this.newTrip.comment == "")){
        this.modal.error = "Please fill all required fields"
        return false
      }
      if(this.newTrip.end_date < this.newTrip.start_date){
        this.modal.error = "End Date should be greater than start date"
        return false
      }
      return true
    },
    handleGlobalError(error){
      if(error.response){
        this.error = error.response.data.message
      }else{
        this.error = "Unable to connect to server"
      }
    },
    handleModalError(error){
      if(error.response){
        this.modal.error = error.response.data.message
      }else{
        this.modal.error = "Unable to connect to server"
      }
    },
    isCurrent(page){
      return page == this.pagination.current_page
    },
    downloadTrips(){
      AuthAPIService.get('/trips', { days: 30 }).then(resp=>{
        PDFGenerator.getTripsPdf(resp.data.data.trips)
      }).catch(error => {
        this.handleGlobalError(error)
      })
    },
    search(){
      this.pagination.current_page = 1
      this.fetchTrips()
    },
    changePage(p){
      this.pagination.current_page = p
      this.fetchTrips()
    },
    modalSave(){
      if(this.modal.editView){
        this.editTrip()
      }else{
        this.addTrip()
      }
    },
    clearModalInputs(){
      this.newTrip.destination = ""
      this.newTrip.start_date = ""
      this.newTrip.end_date = ""
      this.newTrip.id = null
      this.newTrip.comment = ""
      this.newTrip.user.email = ""
      this.newTrip.user.id = null
      this.modal.error = null
    },
    showModal(){
      this.modal.active = true
    },
    hideModal(){
      this.modal.active = false
      this.modal.editView = false
      this.clearModalInputs()
    },
    openEditTrip(i){
      this.newTrip.destination = this.trips[i].destination
      this.newTrip.start_date = this.trips[i].start_date
      this.newTrip.end_date = this.trips[i].end_date
      this.newTrip.id = this.trips[i].pk
      this.newTrip.comment = this.trips[i].comment
      this.modal.editView = true
      if(this.role == 'admin'){
        this.newTrip.user.email = this.trips[i].user.email
        this.newTrip.user.id = this.trips[i].user.pk
      }
      this.showModal()
    },
    deleteTrip(i){
      AuthAPIService.delete("/trips", {
        pk:i
      }).then(() => {
        this.fetchTrips()
      })
    },
    addTrip(){
      if(this.role == 'admin' && !this.validateEmail()){
        return
      }
      if(!this.validateTripForm()){
        return
      }
      var vself = this
      var data = {
        start_date: this.newTrip.start_date,
        end_date: this.newTrip.end_date,
        destination: this.newTrip.destination,
        comment: this.newTrip.comment
      }
      if(this.role == 'admin'){
        data.user_email = this.newTrip.user.email
      }
      AuthAPIService.post('/trips', data).then(() => {
        vself.hideModal()
        vself.fetchTrips()
      }).catch(error=>{
        this.handleModalError(error)
      })
    },
    editTrip(){
      if(this.role == 'admin' && !this.validateEmail()){
        return
      }
      if(!this.validateTripForm()){
        this.modal.error = "Please fill all required fields"
        return
      }
      var vself = this
      var data = {
        start_date: this.newTrip.start_date,
        end_date: this.newTrip.end_date,
        destination: this.newTrip.destination,
        comment: this.newTrip.comment,
        pk: this.newTrip.id
      }
      if(this.role == 'admin'){
        data.user_email = this.newTrip.user.email
      }
      AuthAPIService.put('/trips', data).then(() => {
        vself.hideModal()
        vself.fetchTrips()
      })
    },
    fetchTrips(){
      var vself = this
      AuthAPIService.get("/trips", {
        q:vself.q,
        page:vself.pagination.current_page
      }, true).then(resp => {
        vself.trips = resp.data.data.trips
        vself.pagination.total_pages = resp.data.data.total_pages
      })
    }
  },
  computed: {
    role(){
      return this.$store.state.role
    },
    isLastPage(){
      return this.pagination.current_page == this.pagination.total_pages
    },
    isFirstPage(){
      return this.pagination.current_page == 1
    },
    pages(){
      var start = Math.max(1, this.pagination.current_page - 2)
      var stop = Math.min(this.pagination.total_pages, this.pagination.current_page + 2)
      var pages = []
      for(var i=start; i<=stop; i++){
        pages.push(i)
      }
      return pages
    }
  }
}
</script>