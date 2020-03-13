<template>
  <section class="hero is-primary is-fullheight">
    <div class="hero-body">
      <div class="container">
        <div class="columns is-centered">
          <div class="column is-5-tablet is-4-desktop is-3-widescreen">
            <div class="box">
              <p v-if="error" class="help is-danger">{{error}}</p>
              <div class="field">
                <label for="" class="label">Email</label>
                <div class="control">
                  <input type="email" placeholder="e.g. bobsmith@gmail.com" class="input" required v-model="email">
                </div>
              </div>
              <div class="field">
                <label for="" class="label">Role</label>
                <div class="control">
                  <div class="select is-fullwidth">
                    <select v-model="role">
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
                  <input type="password" placeholder="*******" class="input" required v-model="password">
                </div>
              </div>
              <div class="field">
                <label for="" class="label">Confirm Password</label>
                <div class="control">
                  <input type="password" placeholder="*******" class="input" required v-model="rePassword">
                </div>
              </div>
              <div class="field">
                <button class="button is-success" @click="register">
                  Signup 
                </button>
              </div>
              <div class="field">
                <router-link :to="{ name: 'login'}">already a user? click here to login</router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
</section>
</template>
<script>
import { APIService } from '../utils/api.service';
import { TokenService } from '../utils/token.service';

export default {
  data(){
    return {
      email: "",
      password: "",
      rePassword: "",
      role: "",
      error: null
    }
  },
  methods:{
    validateEmail() {
      if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,6})+$/.test(this.email)){
        return true
      }else{
        this.error = "Please enter a valid email"
        return false
      }
    },
    validateRegistrationForm(){
      
      if((this.email == "") || (this.password == "") || (this.role == "") || (this.rePassword == "")){
        this.error = "Please fill all required fields"
        return false
      }
      if(this.password != this.rePassword){
        this.error = "The passwords do not match"
        return false
      }
      return true
    },
    register(){
      if(!this.validateEmail()){
        return
      }
      if(!this.validateRegistrationForm()){
        return
      }
      APIService.post('/users/register', {
        email:this.email,
        password:this.password,
        role:this.role
      }).then(resp => {
        if(resp.data.status == "success"){
          TokenService.saveToken(resp.data.data.token)
          this.$router.push('/users')
        }else{
          this.error = resp.data.message
        }
      }).catch(error=>{
        this.error = error.response.data.message
      })
    }
  }
}

</script>