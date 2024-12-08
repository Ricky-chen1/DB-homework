<template>
  <div class="user-profile">
    <h1>User Profile</h1>
    <div class="user-info">
      <h2>Personal Information</h2>
      <p><strong>Name:</strong> {{ user.name }}</p>
      <p><strong>Email:</strong> {{ user.email }}</p>
      <!-- Add more user details as needed -->
      <button @click="editProfile">Edit Profile</button>
    </div>

    <div class="order-history">
      <h2>Order History</h2>
      <ul>
        <li v-for="order in orders" :key="order.id">
          {{ order.date }} - {{ order.bookTitle }} - {{ order.status }}
        </li>
      </ul>
    </div>

    <div class="wishlist">
      <h2>Wishlist</h2>
      <ul>
        <li v-for="book in wishlist" :key="book.id">
          {{ book.title }}
        </li>
      </ul>
    </div>

    <div class="settings">
      <h2>Settings</h2>
      <button @click="changePassword">Change Password</button>
      <!-- Add more settings options as needed -->
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';

export default defineComponent({
  name: 'UserProfile',
  setup() {
    const user = ref({
      name: 'John Doe',
      email: 'john.doe@example.com',
      // Add more user fields as needed
    });

    const orders = ref([
      { id: 1, date: '2023-01-01', bookTitle: 'Book A', status: 'Delivered' },
      { id: 2, date: '2023-02-15', bookTitle: 'Book B', status: 'Pending' },
      // Add more orders as needed
    ]);

    const wishlist = ref([
      { id: 1, title: 'Book C' },
      { id: 2, title: 'Book D' },
      // Add more wishlist items as needed
    ]);

    const editProfile = () => {
      // Logic to edit user profile
      console.log('Edit profile clicked');
    };

    const changePassword = () => {
      // Logic to change password
      console.log('Change password clicked');
    };

    return {
      user,
      orders,
      wishlist,
      editProfile,
      changePassword,
    };
  },
});
</script>

<style scoped>
.user-profile {
  padding: 20px;
}

.user-info, .order-history, .wishlist, .settings {
  margin-bottom: 20px;
}

h2 {
  margin-bottom: 10px;
}

button {
  margin-top: 10px;
}
</style>