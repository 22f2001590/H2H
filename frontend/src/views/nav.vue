<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary">
    <div class="container-fluid">
      <a class="navbar-brand" href="/">
        <img src="@/assets/logo.jpg" alt="Logo" width="30" height="30" class="d-inline-block align-text-top" />
        House2Home
      </a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <router-link class="nav-link" to="/customer_login">
              Login as: <strong>Customer</strong>
            </router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/professional_login">
              <strong>Professional</strong>
            </router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/admin_login">
              <strong>Administrator</strong>
            </router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>

</template>

<script>
export default {
  name: "Navbar",
};
</script>
