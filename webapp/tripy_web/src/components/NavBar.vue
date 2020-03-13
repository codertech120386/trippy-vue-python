<template>
<nav class="navbar" role="navigation" aria-label="main navigation">
  <div class="navbar-brand">
    <router-link :to="{ name: 'home'}">
      <img src="../assets/logo.png" width="112" height="28">
    </router-link>

    <a role="button" class="navbar-burger burger" aria-label="menu" aria-expanded="false" data-target="navbarBasicExample">
      <span aria-hidden="true"></span>
      <span aria-hidden="true"></span>
      <span aria-hidden="true"></span>
    </a>
  </div>

  <div id="navbarBasicExample" class="navbar-menu">
    <div class="navbar-start">
      <router-link v-if="role == 'user' || role == 'admin'" :to="{ name: 'trips'}" class="navbar-item">
        Trips
      </router-link>

      <router-link v-if="role == 'user_manager' || role == 'admin'" :to="{ name: 'users'}" class="navbar-item">
        Users
      </router-link>

    </div>

    <div class="navbar-end">
      <div class="navbar-item">
        <div class="buttons">
          <a class="button is-light" @click="dologout">
            Log out
          </a>
        </div>
      </div>
    </div>
  </div>
</nav>
</template>
<script>
import { TokenService } from "../utils/token.service";

export default {
    computed:{
      role(){
        return this.$store.state.role
      }
    },
    name: 'NavBar',
    methods:{
        dologout(){
            TokenService.removeToken();
            this.$store.commit('set_role', null)
            this.$router.push('login');
        }
    }
}
</script>