<script setup>

</script>

<template>
  <header class="header-nav">
    <div class="container">
      <a href="/">
        <div class="logo"><img src="@/assets/images/logo.png" class="logo_img"> 法小询v2.0</div>
      </a>
      <nav class="main-nav">
        <ul class="nav-list">
          <!-- <li><a href="#">元典刑事智库</a></li>
          <li><a href="#">法律计算</a></li> -->
        </ul>
      </nav>
      <div class="user-actions">
        <button class="action-button">注册</button>
        <button class="action-button">登录</button>
      </div>
    </div>
  </header>
</template>


<style scoped lang="scss">
.header-nav {
  position: fixed; // 固定位置，防止滚动时消失
  top: 0;
  left: 0;
  right: 0; // 设置右边界为0，使其宽度扩展至整个视口
  z-index: 1000; // 确保在页面上层显示

  .container {

    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    width: 100%; // 宽度设置为100%
    max-width: 100vw; // 最大宽度为视口宽度
    background-color: #89a8b2;
    border-bottom: 1px solid #89a8b2;
  }


  .logo {
    font-size: 2.0rem;
    font-weight: bold;
    color: white;

    .logo_img {
      width: 3rem;
      height: 3rem;
    }

  }

  .main-nav {
    display: flex;
    align-items: center;

    .nav-list {
      list-style: none;
      margin: 0;
      padding: 0;
      display: flex;

      li {
        margin-left: 1rem;

        a {
          text-decoration: none;
          color: white;
          transition: color 0.3s ease;

          &:hover {
            color: #007bff;
          }
        }
      }
    }
  }

  .user-actions {
    display: flex;
    align-items: center;

    .action-button {
      margin-left: 1rem;
      padding: 0.5rem 1rem;
      border: none;
      background-color: #89a8b2;
      color: white;
      cursor: pointer;
      border-radius: 4px;
      transition: background-color 0.3s ease;
      font-size: 1.3rem;
    }
  }
}
</style>
