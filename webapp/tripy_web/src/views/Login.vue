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
                <label for="" class="label">Password</label>
                <div class="control">
                  <input type="password" placeholder="*******" class="input" required v-model="password">
                  
                </div>
              </div>
              <div class="field">
                <button class="button is-success" @click="login">
                  Login
                </button>
              </div>
              <div class="field">
                <router-link :to="{ name: 'register'}">new user? click here to signup</router-link>
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
    validateLoginForm(){
      return (this.email != "") && (this.password != "")
    },
    login(){
      if(!this.validateEmail()){
        return
      }
      if(!this.validateLoginForm()){
        this.error = "Please fill all required fields"
        return
      }
      APIService.post('/users/login', {
        email:this.email,
        password:this.password
      }).then(resp => {
        if(resp.data.status == "success"){
          TokenService.saveToken(resp.data.data.token)
          this.$router.push('/users')
        } else {
          this.error = resp.data.message
        }
      }).catch(error=>{
        this.error = error.response.data.message
      })
    }
  }
}

</script>