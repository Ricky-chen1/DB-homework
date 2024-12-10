<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";
import { useRouter } from "vue-router";

// 跳转到交易页面
const router = useRouter();
const goToTradePage = () => {
  router.push("/booklist");
};

// 自动播放
let interval: ReturnType<typeof setInterval>;
onMounted(() => {
  interval = setInterval(next, 3000);
});
onUnmounted(() => {
  clearInterval(interval);
});

// 轮播图索引
const currentIndex = ref(0);
// 图片数据和逻辑
const images = [
  new URL('@/assets/images1.svg', import.meta.url).href,
  new URL('@/assets/images2.svg', import.meta.url).href,
  new URL('@/assets/images3.svg', import.meta.url).href,
];

// 自动切换下一张图
const next = () => {
  currentIndex.value = (currentIndex.value + 1) % images.length;
};

// 切换到上一张图
const prev = () => {
  currentIndex.value = (currentIndex.value - 1 + images.length) % images.length;
};

// 客户评论数据
const testimonials = [
  {
    name: "Emily White",
    feedback: "This platform helped me save money and declutter my shelves. Highly recommended!",
  },
  {
    name: "John Smith",
    feedback: "Great way to buy books at a fraction of the cost. The process is seamless and secure.",
  },
  {
    name: "Sophia Lee",
    feedback: "I love how easy it is to sell and buy books here. It’s eco-friendly and efficient!",
  },
];
</script>

<template>
  <div class="home-page">
    <!-- 轮播图 -->
    <div class="carousel">
      <div class="carousel-content">
        <h1 class="carousel-title">Affordable Reads, Sustainable Choices</h1>
        <p class="carousel-subtitle">Buy and Sell Second-hand Books Easily</p>
        <button class="start-button" @click="goToTradePage">开始浏览</button>
      </div>
      <img class="carousel-image" :src="images[currentIndex]" alt="Book Image" />
      <div class="carousel-controls">
        <button @click="prev" class="prev-btn"><i class="icon-left"></i></button>
        <button @click="next" class="next-btn"><i class="icon-right"></i></button>
      </div>
      <ul class="carousel-indicators">
        <li 
          v-for="(image, index) in images"
          :key="index"
          :class="{ active: index === currentIndex }"
          @click="currentIndex = index"
        ></li>
      </ul>
    </div>

    <!-- 简介模块 -->
    <section class="intro-section">
      <h2>Why Choose Us?</h2>
      <p>Join our community to buy and sell books at affordable prices while contributing to a sustainable future.</p>
    </section>

    <!-- 特色模块 -->
    <section class="features-section">
      <div class="feature-card">
        <img src="../assets/icon1.svg" alt="Easy Transactions" />
        <h3>Easy Transactions</h3>
        <p>Secure and hassle-free buying and selling of books.</p>
      </div>
      <div class="feature-card">
        <img src="../assets/icon2.svg" alt="Wide Selection" />
        <h3>Wide Selection</h3>
        <p>Browse a diverse range of books from various genres and categories.</p>
      </div>
      <div class="feature-card">
        <img src="../assets/icon3.svg" alt="Eco-Friendly" />
        <h3>Eco-Friendly</h3>
        <p>Promote sustainability by reusing books and reducing waste.</p>
      </div>
    </section>

    <!-- 客户评论 -->
    <section class="testimonials-section">
      <h2>What Our Users Say</h2>
      <div class="testimonials">
        <div 
          v-for="(testimonial, index) in testimonials" 
          :key="index" 
          class="testimonial-card"
        >
          <p class="testimonial-feedback">{{ testimonial.feedback }}</p>
          <p class="testimonial-name">- {{ testimonial.name }}</p>
        </div>
      </div>
    </section>

    <!-- 项目展示 -->
    <section class="how-it-works-section">
      <div class="how-it-works-bg">
        <h1>How It Works</h1>
        <p>List, Buy, and Exchange Books with Ease.</p>
      </div>
    </section>

    <!-- 页脚 -->
    <footer class="footer">
      <h3>&copy; 2024 BookTrade. All rights reserved.</h3>
    </footer>
  </div>
</template>

<style scoped>
.home-page {
  background-color: #f4f4f9;
  padding: 20px 0;
}

.carousel {
  position: relative;
  background-color: #007bff;
  color: white;
  padding: 50px 20px;
  text-align: center;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.carousel-content {
  max-width: 800px;
  margin: 0 auto;
}

.carousel-title {
  font-size: 2.5rem;
  font-weight: bold;
}

.carousel-subtitle {
  font-size: 1.25rem;
  margin: 10px 0;
}

.start-button {
  background-color: #ff6f61;
  color: white;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
  margin-top: 20px;
}

.carousel-image {
  width: 100%;
  height: auto;
  max-height: 500px;
  object-fit: cover;
  border-radius: 10px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
}

.carousel-controls {
  position: absolute;
  top: 50%;
  left: 20px;
  right: 20px;
  display: flex;
  justify-content: space-between;
  transform: translateY(-50%);
}

.prev-btn,
.next-btn {
  background-color: rgba(0, 0, 0, 0.5);
  color: white;
  border: none;
  padding: 10px;
  border-radius: 50%;
  cursor: pointer;
}

.carousel-indicators {
  display: flex;
  justify-content: center;
  margin-top: 10px;
}

.carousel-indicators li {
  width: 10px;
  height: 10px;
  background-color: white;
  border-radius: 50%;
  margin: 0 5px;
  cursor: pointer;
}

.carousel-indicators li.active {
  background-color: #ff6f61;
}

.intro-section,
.features-section,
.testimonials-section,
.how-it-works-section {
  text-align: center;
  margin: 40px 0;
}

.features-section {
  display: flex;
  justify-content: space-around;
  flex-wrap: wrap;
}

.feature-card {
  width: 250px;
  background: white;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  margin: 10px;
  text-align: center;
}

.feature-card img {
  width: 60px;
  height: 60px;
  margin-bottom: 10px;
}

.testimonials {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
}

.testimonial-card {
  background: white;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
  margin: 15px;
  width: 250px;
  text-align: center;
}

.testimonial-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin-bottom: 15px;
}

.testimonial-feedback {
  font-size: 1rem;
  margin-bottom: 10px;
}

.testimonial-name {
  font-size: 1rem;
  color: #007bff;
}

.footer {
  background-color: #333;
  color: white;
  text-align: center;
  padding: 20px;
}

.footer h3 {
  margin: 0;
  font-size: 1rem;
}
</style>
