<template>
  <section class="hero is-primary is-fullheight" style="margin-top:-54px">
    <div class="hero-body">
      <div class="container">
        <div v-if="error" class="notification is-danger" style="margin-top:24px">
          <button class="delete"></button>
          {{error}}
        </div>
        <div class="card">
          <div class="card-header" style="padding:24px; justify-content: flex-end">
            <button class='button is-info' @click="showModal">Add new User</button>
          </div>
          <div class="card-content" style="min-height:500px">
            <div style="margin-bottom:24px">
              <div class="field">
                <div class="control">
                  <input type="email" v-model="q" @keyup="search" placeholder="type here to filter" class="input">
                </div>
              </div>
            </div>
            <table class="table is-striped is-bordered is-fullwidth">
              <thead>
                <tr>
                  <th>Email</th>
                  <th>Role</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(user, i) in users" :key="user.pk">
                  <td>{{user.email}}</td>
                  <td>{{user.role}}</td>
                  <td>
                    <button class="button is-primary" @click="openEditUser(i)">Edit</button>
                    <button class="button is-danger" @click="deleteUser(user.id)">Delete</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div class="card-footer" style="padding:24px; justify-content: flex-end">
            <div class="pagination-container">
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
          <p v-if="modal.editView" class="modal-card-title">Edit user details</p>
          <p v-else class="modal-card-title">Add a new user</p>
          <button class="delete" aria-label="close" @click="hideModal"></button>
        </header>
        <section class="modal-card-body">
          <div>
              <p v-if="modal.error" class="help is-danger">{{modal.error}}</p>
              <div class="field">
                <label for="" class="label">Email</label>
                <div class="control">
                  <input type="email" placeholder="e.g. bobsmith@gmail.com" class="input" required v-model="newUser.email">
                </div>
              </div>
              <div class="field">
                <label for="" class="label">Role</label>
                <div class="control">
                  <div class="select is-fullwidth" >
                    <select v-model="newUser.role">
                      <option value="user">User</option>
                      <option value="user_manager">User Manager</option>
                      <option value="admin">Admin</option>
                    </select>
                  </div>
                </div>
              </div>
              <div class="field">
                <label for="" class="label">Password</label>
                <div class="control">
                  <input type="password" placeholder="*******" class="input" required v-model="newUser.password">
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
</template>
<style scoped>
</style>
<script>
import { AuthAPIService } from '../utils/api.service';


export default {
  data(){
    return {
      users : [],
      q: "",
      error: null,
      newUser: {
        id: null,
        email: "",
        role: "",
        password: ""
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
    this.fetchUsers()
  },
  methods: {
    validateEmail() {
      console.log(this.newUser.email)
      if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,6})+$/.test(this.newUser.email)){
        return true
      }else{
        this.modal.error = "Please enter a valid email"
        return false
      }
    },
    validateNewUserForm(){
      return (this.newUser.email != "") && (this.newUser.password != "") && (this.newUser.role != "")
    },
    validateEditUserForm(){
      return (this.newUser.email != "") && (this.newUser.role != "")
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
    search(){
      this.pagination.current_page = 1
      this.fetchUsers()
    },
    isCurrent(page){
      return page == this.pagination.current_page
    },
    changePage(p){
      this.pagination.current_page = p
      this.fetchUsers()
    },
    modalSave(){
      if(this.modal.editView){
        this.editUser()
      }else{
        this.addUser()
      }
    },
    clearModalInputs(){
      this.newUser.email = ""
      this.newUser.role = ""
      this.newUser.password = ""
      this.newUser.id = null
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
    openEditUser(i){
      this.newUser.email = this.users[i].email
      this.newUser.role = this.users[i].role
      this.newUser.id = this.users[i].id
      this.modal.editView = true
      this.showModal()
    },
    deleteUser(i){
      AuthAPIService.delete("/users", {
        pk:i
      }).then(() => {
        this.fetchUsers()
      }).catch((error) => {
        this.handleGlobalError(error)
      })
    },
    addUser(){
      if(!this.validateEmail()){
        return
      }
      if(!this.validateNewUserForm()){
        this.modal.error = "Please fill all required fields" 
        return
      }
      var vself = this
      AuthAPIService.post('/users', {
        email: this.newUser.email,
        password: this.newUser.password,
        role: this.newUser.role
      }).then(() => {
        vself.hideModal()
        vself.fetchUsers()
      }).catch((error) => {
        vself.handleModalError(error)
      })
    },
    editUser(){
      if(!this.validateEmail()){
        return
      }
      if(!this.validateEditUserForm()){
        this.modal.error = "Please fill all required fields" 
        return
      }
      var vself = this
      AuthAPIService.put('/users', {
        email: this.newUser.email,
        pk: this.newUser.id,
        role: this.newUser.role,
        password: this.newUser.password
      }).then(() => {
        vself.hideModal()
        vself.fetchUsers()
      }).catch((error) => {
        vself.handleModalError(error)
      })
    },
    fetchUsers(){
      var vself = this
      AuthAPIService.get("/users", {
        q:vself.q,
        page:vself.pagination.current_page
      }, true).then(resp => {
        vself.users = resp.data.data.users
        vself.pagination.total_pages = resp.data.data.total_pages
      }).catch((error) => {
        this.handleGlobalError(error)
      })
    }
  },
  computed: {
    isLastPage(){
      return this.pagination.current_page == this.pagination.total_pages
    },
    isFirstPage(){
      return this.pagination.current_page == 1
    },
    pages(){
      var start = 1
      var stop = this.pagination.total_pages
      var pages = []
      for(var i=start; i<=stop; i++){
        pages.push(i)
      }
      return pages
    }
  }
}
</script>