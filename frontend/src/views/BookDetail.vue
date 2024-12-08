<template>
  <div class="book-detail">
    <div class="container">
      <div v-if="book" class="book-card">
        <img :src="book.image" alt="Book Cover" class="book-cover" v-if="book.image" />
        <div class="book-info">
          <h1 class="book-title">{{ book.title }}</h1>
          <p class="book-author"><strong>Author:</strong> {{ book.author }}</p>
          <p class="book-price"><strong>Price:</strong> ${{ book.price }}</p>
          <p class="book-description"><strong>Description:</strong> {{ book.description }}</p>
        </div>
      </div>
      <div v-else class="loading-message">
        Loading book details...
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';

const book = ref(null);
const route = useRoute();

const fetchBookDetail = async () => {
  try {
    const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/books/${route.params.id}/`);
    book.value = response.data.book;
  } catch (error) {
    console.error('Failed to fetch book details:', error);
  }
};

onMounted(() => {
  fetchBookDetail();
});
</script>

<style scoped>
.book-detail {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f4f4f9;
  padding: 20px;
}

.container {
  max-width: 800px;
  width: 100%;
  background: white;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
  padding: 20px;
}

.book-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.book-cover {
  width: 200px;
  height: auto;
  border-radius: 10px;
  margin-bottom: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.book-info {
  font-family: 'Arial', sans-serif;
  line-height: 1.6;
}

.book-title {
  font-size: 1.8rem;
  margin-bottom: 10px;
  color: #333;
}

.book-author,
.book-price {
  font-size: 1rem;
  margin-bottom: 5px;
  color: #555;
}

.book-description {
  font-size: 0.95rem;
  color: #666;
  margin-top: 15px;
}

.loading-message {
  text-align: center;
  font-size: 1.2rem;
  color: #777;
}
</style>
