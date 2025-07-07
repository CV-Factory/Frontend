<svelte:head>
  <title>CVFactory</title>
  <link rel="canonical" href="https://cvfactory.dev/" />
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1" />
  <meta name="googlebot" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <link rel="stylesheet" href="/static/build/style.css" />

  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-177JQT5LCY"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag() { dataLayer.push(arguments); }
    gtag('js', new Date());
    gtag('config', 'G-177JQT5LCY', { send_page_view: true });
  </script>

  <!-- SEO Meta Tags -->
  <meta name="description" content="CVFactory를 사용하여 채용 공고와 나만의 스토리를 바탕으로 맞춤형 자기소개서를 쉽게 생성하세요." />
  <meta name="keywords" content="자기소개서, 자소서, 이력서, 생성, AI, 채용, 취업, CV, Resume, Generator, AI Resume, AI CV" />

  <!-- Open Graph Tags -->
  <meta property="og:title" content="CVFactory - AI 자기소개서 생성기" />
  <meta property="og:description" content="CVFactory를 사용하여 채용 공고와 나만의 스토리를 바탕으로 맞춤형 자기소개서를 쉽게 생성하세요." />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="https://cvfactory.dev" />
  <meta property="og:image" content="/static/logo.png" />

  <!-- Twitter Card Tags -->
  <meta name="twitter:card" content="summary" />
  <meta name="twitter:title" content="CVFactory - AI 자기소개서 생성기" />
  <meta name="twitter:description" content="CVFactory를 사용하여 채용 공고와 나만의 스토리를 바탕으로 맞춤형 자기소개서를 쉽게 생성하세요." />
  <meta name="twitter:image" content="/static/logo.png" />

  <!-- Favicons -->
  <link rel="apple-touch-icon" sizes="180x180" href="/static/favicon_io/apple-touch-icon.png" />
  <link rel="icon" type="image/png" sizes="32x32" href="/static/favicon_io/favicon-32x32.png" />
  <link rel="icon" type="image/png" sizes="16x16" href="/static/favicon_io/favicon-16x16.png" />
  <link rel="manifest" href="/static/favicon_io/site.webmanifest" />
  <link rel="icon" href="/static/favicon_io/favicon.ico" />
</svelte:head>

<script>
  import { onMount } from 'svelte';

  let jobUrl = '';
  let prompt = '';
  let generated = '';
  let loading = false;
  let statusMessage = '';

  async function generate() {
    loading = true;
    statusMessage = '생성 중...';
    try {
      // 예시: Cloudflare Worker BFF 호출
      const res = await fetch(`/api/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ job_url: jobUrl, prompt })
      });
      const data = await res.json();
      generated = data.result || '';
      statusMessage = '완료';
    } catch (e) {
      statusMessage = '오류 발생';
      console.error(e);
    } finally {
      loading = false;
    }
  }

  onMount(() => {
    // 기존 script.js 로직을 그대로 실행하고 싶다면 import 가능
  });
</script>

<header>
  <div class="header-title">CVFactory</div>
</header>

<main>
  <h1>생성할 채용 공고를 입력하세요!</h1>
  <div class="prompt-container">
    <div class="left-column">
      <div class="chat-box small-prompt">
        <textarea bind:value={jobUrl} placeholder="채용 공고 URL 입력" />
      </div>
      <div class="chat-box">
        <textarea bind:value={prompt} placeholder="경력/스토리 입력" />
      </div>
    </div>

    <div class="right-column">
      <div class="chat-box large-prompt">
        <textarea class="large-textarea" bind:value={generated} placeholder="생성된 자기소개서" />
        <div class="actions">
          <span class="status-message">{statusMessage}</span>
          <button class="black-btn" on:click={generate} disabled={loading}>
            {loading ? '생성 중...' : '생성하기'}
          </button>
        </div>
      </div>
    </div>
  </div>
</main>

<style>
  /* 필요한 경우에만 Svelte 전용 추가 스타일을 작성하세요 */
  header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 2rem;
  }
</style> 